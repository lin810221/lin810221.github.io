"""Offline behavior tests. Only stdlib unittest; provider calls are mocked."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import provider_requests as api
import live_agents
from agent_core import Decision, ToolCall, run_agent, simulated_model, multiply
from approval_store import ApprovalStore
from contracts import validate_answer
from memory_store import MemoryStore


def load_numbered(name):
    import importlib.util
    module_name = "llm_tutorial_" + name
    spec = importlib.util.spec_from_file_location(module_name, Path(__file__).parent / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RequestTests(unittest.TestCase):
    def test_provider_budgets_have_correct_locations(self):
        bodies = {provider: api.request_for(provider,"model","question",4096) for provider in api.PROVIDERS}
        self.assertEqual(bodies["openai"]["max_output_tokens"],4096)
        self.assertEqual(bodies["gemini"]["generation_config"]["max_output_tokens"],4096)
        self.assertEqual(bodies["claude"]["max_tokens"],4096)
        self.assertNotIn("temperature",bodies["openai"])

    def test_invalid_budgets_are_rejected(self):
        for value in (0,-1,True,"100"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                api.request_for("openai","model","question",value)

    def test_dry_run_never_uses_network_or_key(self):
        for provider in api.PROVIDERS:
            with self.subTest(provider=provider), patch.dict(os.environ,{},clear=True), patch.object(sys,"argv",["demo"]), patch.object(api.urllib.request,"urlopen") as network, contextlib.redirect_stdout(io.StringIO()) as output:
                api.run_cli(provider)
                network.assert_not_called()
                self.assertIn("DRY RUN",output.getvalue())

    def test_missing_key_fails_before_network(self):
        with patch.dict(os.environ,{},clear=True), patch.object(api.urllib.request,"urlopen") as network:
            with self.assertRaises(ValueError):
                api.call_live("openai",api.request_for("openai","model","question"))
            network.assert_not_called()

    def test_live_transport_can_be_tested_without_real_request(self):
        fixture = {"status":"completed","output":[{"type":"message","content":[{"type":"output_text","text":"hello"}]}]}
        stream = io.BytesIO(json.dumps(fixture).encode())
        with patch.dict(os.environ,{"OPENAI_API_KEY":"unit-test-only"}), patch.object(api.urllib.request,"urlopen",return_value=stream) as network:
            reply = api.call_live("openai",api.request_for("openai","model","question"),timeout=12)
            self.assertEqual(reply.text,"hello")
            self.assertEqual(network.call_args.kwargs["timeout"],12)

    def test_schema_conversion_does_not_mutate_original_request(self):
        for provider in api.PROVIDERS:
            body = api.request_for(provider,"model","question")
            original = json.loads(json.dumps(body))
            changed = api.with_schema(provider,body,{"type":"object"})
            self.assertEqual(body,original)
            self.assertNotEqual(changed,body)

    def test_openai_text_skips_reasoning_and_tools(self):
        data = {"status":"completed","output":[{"type":"reasoning","summary":[]},{"type":"message","content":[{"type":"output_text","text":"answer"}]}]}
        self.assertEqual(api.parse_reply("openai",data).text,"answer")
        data["output"].append({"type":"function_call","arguments":"{}"})
        self.assertEqual(api.parse_reply("openai",data).status,"requires_tools")
        data["status"] = "incomplete"
        self.assertEqual(api.parse_reply("openai",data).status,"incomplete")

    def test_openai_refusal_is_explicit(self):
        data = {"status":"completed","output":[{"type":"message","content":[{"type":"refusal","refusal":"no"}]}]}
        self.assertEqual(api.parse_reply("openai",data).status,"refused")

    def test_gemini_steps_only_extract_visible_text(self):
        data = {"status":"completed","steps":[{"type":"thought","content":[{"type":"text","text":"hidden"}]},{"type":"model_output","content":[{"type":"text","text":"visible"}]}]}
        self.assertEqual(api.parse_reply("gemini",data).text,"visible")
        data["steps"].append({"type":"function_call","name":"x"})
        self.assertEqual(api.parse_reply("gemini",data).status,"requires_tools")

    def test_claude_blocks_and_stop_reason(self):
        data = {"content":[{"type":"thinking","thinking":"hidden"},{"type":"text","text":"visible"}],"stop_reason":"end_turn","stop_details":None}
        self.assertEqual(api.parse_reply("claude",data).text,"visible")
        data["stop_reason"] = "max_tokens"
        self.assertEqual(api.parse_reply("claude",data).status,"incomplete")
        data["stop_reason"] = "tool_use"
        self.assertEqual(api.parse_reply("claude",data).status,"requires_tools")


class SamplingAndContractTests(unittest.TestCase):
    def test_sampling_distribution_and_top_p(self):
        distribution = load_numbered("04_sampling").distribution
        self.assertAlmostEqual(sum(distribution([2,1,0],0.7,0.9)),1)
        self.assertEqual(distribution([2,1,0],0),[1,0,0])
        self.assertEqual(distribution([2,1,0],1,0.1),[1,0,0])
        self.assertGreater(distribution([2,1,0],0.3)[0],distribution([2,1,0],1.5)[0])

    def test_sampling_invalid_values(self):
        distribution = load_numbered("04_sampling").distribution
        for logits,temp,top_p in [([],1,1),([1],-1,1),([1],1,0),([float('nan')],1,1)]:
            with self.assertRaises(ValueError):
                distribution(logits,temp,top_p)

    def test_contract_validates_sources_and_shape(self):
        valid = validate_answer('{"answer":"ok [D1]","sources":["D1"]}',{"D1"})
        self.assertEqual(valid.sources,("D1",))
        for data in [
            {"answer":"ok","sources":["D9"]},{"answer":"ok","sources":["D1","D1"]},
            {"answer":"","sources":["D1"]},{"answer":"ok","sources":[]},
            {"answer":"ok [D9]","sources":["D1"]},{"answer":"ok","sources":["D1"],"extra":1},
        ]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                validate_answer(json.dumps(data),{"D1"})

    def test_event_normalizers_do_not_display_tool_arguments(self):
        module = load_numbered("07_events")
        self.assertIsNone(module.normalize_event("openai",{"type":"response.function_call_arguments.delta","delta":"secret"}))
        self.assertIsNone(module.normalize_event("claude",{"type":"content_block_delta","delta":{"type":"input_json_delta","partial_json":"{}"}}))
        self.assertEqual(module.normalize_event("gemini",{"event_type":"step.delta","delta":{"type":"text","text":"hello"}}),{"kind":"text","text":"hello"})

    def test_hypothetical_cost_counts_cached_input_once(self):
        module = load_numbered("09_cost")
        self.assertEqual(str(module.estimate(10000,6000,1000,"2","0.5","8")),"0.019")
        with self.assertRaises(ValueError):
            module.estimate(1,2,0,"1","1","1")


class AgentTests(unittest.TestCase):
    def test_bounded_agent_completes(self):
        result = run_agent(simulated_model,"6*7",{"multiply":multiply})
        self.assertEqual(result["status"],"completed")
        self.assertIn("42",result["answer"])

    def test_unknown_tool_cannot_execute(self):
        calls = iter([Decision(calls=(ToolCall("1","delete_all",{}),)),Decision(text="stopped")])
        result = run_agent(lambda history: next(calls),"test",{})
        self.assertEqual(result["history"][-1]["result"],{"error":"unknown_tool"})

    def test_invalid_tool_arguments_are_rejected(self):
        for args in ({"a":True,"b":2},{"a":1,"b":2,"extra":3}):
            with self.assertRaises(ValueError):
                multiply(args)

    def test_call_budget_stops_before_execution(self):
        result = run_agent(simulated_model,"test",{"multiply":multiply},max_calls=0)
        self.assertEqual(result["status"],"budget_exceeded")

    def test_turn_budget_stops_repeated_calls(self):
        model = lambda history: Decision(calls=(ToolCall("same","multiply",{"a":2,"b":3}),))
        result = run_agent(model,"test",{"multiply":multiply},max_turns=3)
        self.assertEqual(result["status"],"budget_exceeded")

    def test_duplicate_call_id_executes_pure_tool_once(self):
        counter = []
        def tool(args):
            counter.append(1)
            return 42
        sequence = iter([Decision(calls=(ToolCall("same","test",{}),)),Decision(calls=(ToolCall("same","test",{}),)),Decision(text="done")])
        run_agent(lambda h: next(sequence),"test",{"test":tool})
        self.assertEqual(len(counter),1)

    def test_reused_id_with_different_arguments_is_rejected(self):
        sequence = iter([Decision(calls=(ToolCall("same","multiply",{"a":1,"b":2}),)),Decision(calls=(ToolCall("same","multiply",{"a":3,"b":4}),))])
        with self.assertRaises(ValueError):
            run_agent(lambda h: next(sequence),"test",{"multiply":multiply})


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "demo.sqlite"

    def tearDown(self):
        self.folder.cleanup()

    def test_memory_survives_reopen_and_isolates_owner(self):
        with MemoryStore(self.path) as store:
            store.append("alice","same","A")
            store.append("bob","same","B")
            store.set_preference("alice","locale","zh-TW")
        with MemoryStore(self.path) as store:
            self.assertEqual(store.history("alice","same"),["A"])
            self.assertEqual(store.history("bob","same"),["B"])
            self.assertEqual(store.preference("alice","locale"),"zh-TW")
            self.assertEqual(store.history("alice' OR 1=1 --","same"),[])

    def test_proposal_is_not_published_before_approval(self):
        with ApprovalStore(self.path) as store:
            proposal = store.propose("alice","answer",["D1"])
            self.assertEqual(proposal["status"],"pending")
            self.assertEqual(store.publication_count(),0)

    def test_duplicate_approval_publishes_once(self):
        with ApprovalStore(self.path) as store:
            proposal = store.propose("alice","answer",["D1"])
            for _ in range(2):
                store.resolve("alice",proposal["id"],proposal["digest"],True)
            self.assertEqual(store.publication_count(),1)

    def test_rejection_never_publishes(self):
        with ApprovalStore(self.path) as store:
            proposal = store.propose("alice","answer",["D1"])
            self.assertEqual(store.resolve("alice",proposal["id"],proposal["digest"],False)["status"],"rejected")
            self.assertEqual(store.publication_count(),0)

    def test_stale_digest_and_other_owner_are_rejected(self):
        with ApprovalStore(self.path) as store:
            proposal = store.propose("alice","answer",["D1"])
            with self.assertRaises(ValueError):
                store.resolve("alice",proposal["id"],"stale",True)
            with self.assertRaises(KeyError):
                store.resolve("bob",proposal["id"],proposal["digest"],True)
            self.assertEqual(store.publication_count(),0)

    def test_decision_survives_reopen_and_cannot_be_reversed(self):
        with ApprovalStore(self.path) as store:
            proposal = store.propose("alice","answer",["D1"])
            store.resolve("alice",proposal["id"],proposal["digest"],True)
        with ApprovalStore(self.path) as store:
            self.assertEqual(store.get("alice",proposal["id"])["status"],"approved")
            with self.assertRaises(ValueError):
                store.resolve("alice",proposal["id"],proposal["digest"],False)


class CapstoneTests(unittest.TestCase):
    def test_unknown_question_refuses_without_model(self):
        module = load_numbered("12_capstone")
        with patch.object(module,"call_live") as network:
            self.assertEqual(module.prepare("推薦午餐","openai",True)["status"],"insufficient_evidence")
            network.assert_not_called()

    def test_online_provider_is_dry_run_by_default(self):
        module = load_numbered("12_capstone")
        with patch.object(module,"call_live") as network:
            result = module.prepare("Agent 工具","gemini")
            self.assertEqual(result["status"],"dry_run")
            self.assertIn("response_format",result["request"])
            network.assert_not_called()

    def test_incomplete_model_response_is_not_published(self):
        module = load_numbered("12_capstone")
        with patch.dict(os.environ,{"OPENAI_MODEL":"unit-test-model"}), patch.object(module,"call_live",return_value=api.Reply("partial","incomplete",{})):
            with self.assertRaises(ValueError):
                module.prepare("Agent 工具","openai",True)

    def test_mocked_model_draft_is_validated(self):
        module = load_numbered("12_capstone")
        reply = api.Reply('{"answer":"Agent 使用工具。[D1]","sources":["D1"]}',"completed",{})
        with patch.dict(os.environ,{"OPENAI_MODEL":"unit-test-model"}), patch.object(module,"call_live",return_value=reply):
            self.assertEqual(module.prepare("Agent 工具","openai",True)["sources"],["D1"])


class NativeAgentTests(unittest.TestCase):
    def test_native_dry_runs_never_call_api(self):
        with patch.object(live_agents,"call_raw") as network:
            for provider in api.PROVIDERS:
                self.assertEqual(live_agents.native_agent(provider,"6*7")["status"],"dry_run")
            network.assert_not_called()

    def test_openai_native_loop_preserves_reasoning_and_call_id(self):
        first = {"status":"completed","output":[{"type":"reasoning","id":"r1","summary":[]},{"type":"function_call","name":"multiply","call_id":"c1","arguments":"{\"a\":6,\"b\":7}"}]}
        final = {"status":"completed","output":[{"type":"message","content":[{"type":"output_text","text":"42"}]}]}
        with patch.dict(os.environ,{"OPENAI_MODEL":"test"}), patch.object(live_agents,"call_raw",side_effect=[first,final]) as network:
            self.assertEqual(live_agents.native_agent("openai","6*7",True)["answer"],"42")
            history = network.call_args_list[1].args[1]["input"]
            self.assertEqual(history[1]["type"],"reasoning")
            self.assertEqual(history[-1]["call_id"],"c1")

    def test_gemini_native_loop_preserves_thought_step(self):
        first = {"status":"requires_action","steps":[{"type":"thought","signature":"opaque"},{"type":"function_call","id":"g1","name":"multiply","arguments":{"a":6,"b":7}}]}
        final = {"status":"completed","steps":[{"type":"model_output","content":[{"type":"text","text":"42"}]}]}
        with patch.dict(os.environ,{"GEMINI_MODEL":"test"}), patch.object(live_agents,"call_raw",side_effect=[first,final]) as network:
            self.assertEqual(live_agents.native_agent("gemini","6*7",True)["answer"],"42")
            body = network.call_args_list[1].args[1]
            self.assertFalse(body["store"])
            self.assertEqual(body["input"][1]["signature"],"opaque")
            self.assertEqual(body["input"][-1]["call_id"],"g1")

    def test_claude_native_loop_preserves_blocks_and_matches_tool_use_id(self):
        first = {"stop_reason":"tool_use","content":[{"type":"thinking","thinking":"summary","signature":"opaque"},{"type":"tool_use","id":"t1","name":"multiply","input":{"a":6,"b":7}}]}
        final = {"stop_reason":"end_turn","content":[{"type":"text","text":"42"}]}
        with patch.dict(os.environ,{"ANTHROPIC_MODEL":"test"}), patch.object(live_agents,"call_raw",side_effect=[first,final]) as network:
            self.assertEqual(live_agents.native_agent("claude","6*7",True)["answer"],"42")
            history = network.call_args_list[1].args[1]["messages"]
            self.assertEqual(history[1]["content"][0]["signature"],"opaque")
            self.assertEqual(history[-1]["content"][0]["tool_use_id"],"t1")


if __name__ == "__main__":
    unittest.main()
