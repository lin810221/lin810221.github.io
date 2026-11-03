"""Domain, security, real SDK, stdio and loopback HTTP acceptance tests.

No provider APIs or public network calls. Transport tests launch only the
fictional local server and require permission to create local subprocess pipes.
"""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory
import asyncio
import json
import os
import socket
import subprocess
import sys
import time
import unittest
import jwt
from jsonschema import Draft202012Validator
from mcp import Client, StdioServerParameters
from mcp.server import MCPServer
from mcp.types import ElicitResult, TextResourceContents
from auth_verifier import CourseTokenVerifier, DEMO_KEY, fixture_token, token_principal
from capstone_server import build_capstone
from demo_server import build_server
from integration_core import (ALICE, BOB, REVIEWER, Principal, WorkflowStore, audit_event,
                              cache_key, endpoint_policy, safe_file, search_notes)

HERE = Path(__file__).resolve().parent


def exception_leaves(error):
    if isinstance(error, BaseExceptionGroup):
        return [leaf for child in error.exceptions for leaf in exception_leaves(child)]
    return [error]


class AsyncCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        asyncio.get_running_loop().set_debug(False)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.now = 1000.0
        self.store = WorkflowStore(Path(self.temp.name) / "test.sqlite", lambda: self.now)
        self.preview = self.store.preview(ALICE, "T1")["preview_id"]

    def approved(self):
        self.store.review(REVIEWER, self.preview, True)

    def test_pending_cannot_commit(self):
        with self.assertRaises(PermissionError): self.store.commit(ALICE, self.preview, "k")
        self.assertEqual(self.store.ticket(ALICE, "T1")["status"], "open")

    def test_approved_commit_has_one_effect(self):
        self.approved()
        result = self.store.commit(ALICE, self.preview, "k")
        self.assertEqual(result, {"ticket_id": "T1", "status": "closed", "version": 2})
        self.assertEqual(len(self.store.audit()), 1)

    def test_replay_returns_original_receipt(self):
        self.approved()
        first = self.store.commit(ALICE, self.preview, "k")
        self.assertEqual(first, self.store.commit(ALICE, self.preview, "k"))
        self.assertEqual(self.store.ticket(ALICE, "T1")["version"], 2)

    def test_different_key_cannot_reuse_consumed_preview(self):
        self.approved(); self.store.commit(ALICE, self.preview, "k")
        with self.assertRaises(PermissionError): self.store.commit(ALICE, self.preview, "other")

    def test_same_key_different_preview_conflicts(self):
        other = self.store.preview(ALICE, "T1")["preview_id"]
        self.approved(); self.store.commit(ALICE, self.preview, "k")
        with self.assertRaises(ValueError): self.store.commit(ALICE, other, "k")

    def test_other_tenant_cannot_commit(self):
        self.approved()
        with self.assertRaises(PermissionError): self.store.commit(BOB, self.preview, "k")

    def test_other_subject_cannot_commit(self):
        self.approved()
        with self.assertRaises(PermissionError):
            self.store.commit(Principal("alpha", "eve", ALICE.scopes), self.preview, "k")

    def test_other_issuer_cannot_commit(self):
        self.approved()
        with self.assertRaises(PermissionError):
            self.store.commit(Principal("alpha", "alice", ALICE.scopes, "https://other.invalid"), self.preview, "k")

    def test_permission_revocation_blocks_replay(self):
        self.approved(); self.store.commit(ALICE, self.preview, "k")
        with self.assertRaises(PermissionError):
            self.store.commit(Principal("alpha", "alice", frozenset()), self.preview, "k")

    def test_expired_approval_cannot_commit(self):
        self.approved(); self.now += 301
        with self.assertRaises(PermissionError): self.store.commit(ALICE, self.preview, "k")

    def test_expired_preview_cannot_be_reviewed(self):
        self.now += 301
        with self.assertRaises(ValueError): self.approved()

    def test_denied_cannot_commit(self):
        self.store.review(REVIEWER, self.preview, False)
        with self.assertRaises(PermissionError): self.store.commit(ALICE, self.preview, "k")

    def test_review_requires_separate_permission(self):
        with self.assertRaises(PermissionError): self.store.review(ALICE, self.preview, True)

    def test_review_requires_separate_person(self):
        same = Principal("alpha", "alice", ALICE.scopes | {"tickets:review"})
        with self.assertRaises(PermissionError): self.store.review(same, self.preview, True)

    def test_review_is_tenant_bound(self):
        with self.assertRaises(PermissionError):
            self.store.review(Principal("beta", "reviewer", REVIEWER.scopes), self.preview, True)

    def test_stale_preview_does_not_overwrite_new_version(self):
        self.approved()
        with closing(self.store.connect()) as conn:
            conn.execute("UPDATE tickets SET version=2 WHERE tenant='alpha' AND id='T1'")
        with self.assertRaises(ValueError): self.store.commit(ALICE, self.preview, "k")
        self.assertEqual(self.store.audit(), [])

    def test_payload_tampering_rejected(self):
        self.approved()
        with closing(self.store.connect()) as conn:
            conn.execute("UPDATE previews SET payload='{}' WHERE id=?", (self.preview,))
        with self.assertRaises(ValueError): self.store.commit(ALICE, self.preview, "k")

    def test_crash_rolls_back_effect_receipt_and_audit(self):
        self.approved()
        with self.assertRaises(RuntimeError):
            self.store.commit(ALICE, self.preview, "k", fail_before_receipt=True)
        self.assertEqual(self.store.ticket(ALICE, "T1")["version"], 1)
        self.assertEqual(self.store.audit(), [])
        self.assertEqual(self.store.commit(ALICE, self.preview, "k")["version"], 2)

    def test_concurrent_replay_has_one_effect(self):
        self.approved()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.store.commit(ALICE, self.preview, "same"), range(2)))
        self.assertEqual(results[0], results[1]); self.assertEqual(len(self.store.audit()), 1)

    def test_beta_ticket_unchanged(self):
        self.approved(); self.store.commit(ALICE, self.preview, "k")
        self.assertEqual(self.store.ticket(BOB, "T1")["status"], "open")


class PolicyTests(unittest.TestCase):
    def test_search_is_tenant_scoped(self):
        self.assertEqual(search_notes(ALICE, "beta"), [])
        self.assertEqual(search_notes(BOB, "beta")[0]["id"], "N3")

    def test_missing_scope_denied(self):
        with self.assertRaises(PermissionError): search_notes(Principal("alpha", "eve", frozenset()), "MCP")

    def test_invalid_limits_denied(self):
        for value in (0, 11, True, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError): search_notes(ALICE, "MCP", value)

    def test_empty_query_denied(self):
        with self.assertRaises(ValueError): search_notes(ALICE, "   ")

    def test_cache_principal_and_revision_isolation(self):
        keys = {cache_key(p, rev, "search", {"q": "MCP"}) for p in (ALICE, BOB) for rev in ("1", "2")}
        self.assertEqual(len(keys), 4)

    def test_cache_scope_isolation(self):
        limited = Principal("alpha", "alice", frozenset({"notes:read"}))
        self.assertNotEqual(cache_key(ALICE, "1", "x", {}), cache_key(limited, "1", "x", {}))

    def test_endpoint_policy_rejects_unsafe_origins(self):
        for url in ("http://tools.invalid/mcp", "https://evil.invalid/mcp", "https://user:pass@tools.invalid/mcp", "https://tools.invalid:8443/mcp"):
            with self.subTest(url=url), self.assertRaises(ValueError): endpoint_policy(url, {"tools.invalid"}, ["93.184.216.34"])

    def test_endpoint_policy_rejects_private_and_mixed_dns(self):
        for values in ([], ["127.0.0.1"], ["169.254.169.254"], ["93.184.216.34", "::1"]):
            with self.subTest(values=values), self.assertRaises(ValueError): endpoint_policy("https://tools.invalid/mcp", {"tools.invalid"}, values)

    def test_endpoint_approved_public_snapshot(self):
        self.assertEqual(endpoint_policy("https://tools.invalid/mcp", {"tools.invalid"}, ["93.184.216.34"]), "https://tools.invalid/mcp")

    def test_audit_drops_secrets_and_content(self):
        event = audit_event(tool="search", status="ok", token="secret", arguments={"x": "private"})
        self.assertEqual(event, {"tool": "search", "status": "ok"})

    def test_file_traversal_absolute_suffix_and_size(self):
        with TemporaryDirectory() as folder:
            root = Path(folder) / "docs"; root.mkdir()
            (root / "safe.txt").write_text("fixture", encoding="utf-8")
            (root / "secret.json").write_text("{}", encoding="utf-8")
            (Path(folder) / "outside.txt").write_text("outside", encoding="utf-8")
            self.assertEqual(safe_file(root, "safe.txt"), "fixture")
            for value in ("../outside.txt", str((root / "safe.txt").resolve()), "secret.json"):
                with self.subTest(value=value), self.assertRaises(PermissionError): safe_file(root, value)
            with self.assertRaises(ValueError): safe_file(root, "safe.txt", 3)

    def test_sql_injection_is_data(self):
        with TemporaryDirectory() as folder:
            store = WorkflowStore(Path(folder) / "fixture.sqlite")
            query = import_module("28_sql_readonly").query_status
            self.assertEqual(query(store.path, "alpha", "open"), [("T1", "open")])
            self.assertEqual(query(store.path, "alpha", "open' OR 1=1 --"), [])

    def test_retry_write_without_idempotency_has_one_attempt(self):
        schedule = import_module("25_retries_deadlines").retry_schedule
        self.assertEqual(len(schedule(read_only=False, has_idempotency=False, total_budget=5, attempt_timeout=1)), 1)

    def test_retry_total_time_bound(self):
        schedule = import_module("25_retries_deadlines").retry_schedule
        rows = schedule(read_only=True, has_idempotency=False, total_budget=2.5, attempt_timeout=1)
        self.assertLessEqual(sum(row["timeout"] for row in rows), 2.5)

    def test_wire_correlation_rejects_wrong_id(self):
        wire = import_module("03_wire_messages")
        with self.assertRaises(ValueError): wire.match_response(wire.request(), {"jsonrpc": "2.0", "id": 2, "result": {}})

    def test_provider_configs_are_allowlisted_without_secrets(self):
        configs = import_module("18_provider_configs").configurations()
        self.assertEqual(configs["openai_responses"]["tools"][0]["require_approval"], "always")
        self.assertFalse(configs["gemini_cli"]["mcpServers"]["course_notes"]["trust"])


class TokenTests(AsyncCase):
    async def test_valid_identity(self):
        token = await CourseTokenVerifier().verify_token(fixture_token())
        self.assertEqual(token_principal(token).subject, "alice")
        self.assertNotEqual(token.subject, token.client_id)

    async def test_invalid_claims_rejected(self):
        for overrides in ({"aud": "other"}, {"iss": "other"}, {"exp": 1}, {"tenant": ""}, {"scope": ["notes:read"]}):
            with self.subTest(overrides=overrides):
                self.assertIsNone(await CourseTokenVerifier().verify_token(fixture_token(**overrides)))

    async def test_wrong_signature_rejected(self):
        claims = jwt.decode(fixture_token(), DEMO_KEY, algorithms=["HS256"], options={"verify_aud": False})
        bad = jwt.encode(claims, "a-different-public-fixture-key-123456789", algorithm="HS256")
        self.assertIsNone(await CourseTokenVerifier().verify_token(bad))

    async def test_unsigned_token_rejected(self):
        bad = jwt.encode({"sub": "alice"}, key="", algorithm="none")
        self.assertIsNone(await CourseTokenVerifier().verify_token(bad))


class SDKTests(AsyncCase):
    async def test_modern_discovery_and_output_schema(self):
        async with Client(build_server()) as client:
            self.assertEqual(client.protocol_version, "2026-07-28")
            tool = next(t for t in (await client.list_tools()).tools if t.name == "search_notes")
            result = await client.call_tool("search_notes", {"query": "MCP", "limit": 1})
            self.assertFalse(result.is_error)
            Draft202012Validator(tool.output_schema).validate(result.structured_content)

    async def test_legacy_compatibility(self):
        async with Client(build_server(), mode="legacy") as client:
            self.assertEqual(client.protocol_version, "2025-11-25")
            self.assertFalse((await client.call_tool("search_notes", {"query": "MCP"})).is_error)

    async def test_invalid_input_is_error(self):
        async with Client(build_server()) as client:
            for limit in (0, 11, True, "2"):
                self.assertTrue((await client.call_tool("search_notes", {"query": "MCP", "limit": limit})).is_error)

    async def test_empty_search_is_success(self):
        async with Client(build_server()) as client:
            result = await client.call_tool("search_notes", {"query": "no-matches"})
            self.assertFalse(result.is_error); self.assertEqual(result.structured_content["matches"], [])

    async def test_unknown_tool_is_error(self):
        async with Client(build_server()) as client:
            self.assertTrue((await client.call_tool("unknown", {})).is_error)

    async def test_resource_templates_and_read(self):
        async with Client(build_server()) as client:
            self.assertEqual((await client.list_resources()).resources, [])
            self.assertEqual(len((await client.list_resource_templates()).resource_templates), 1)
            result = await client.read_resource("notes://guide/mcp")
            self.assertIsInstance(result.contents[0], TextResourceContents)

    async def test_prompt_render_is_not_generation(self):
        async with Client(build_server()) as client:
            result = await client.get_prompt("explain", {"topic": "MCP"})
            self.assertIn("MCP", result.messages[0].content.text)

    async def test_mrtr_accept_and_hidden_parameter(self):
        async def answer(ctx, params): return ElicitResult(action="accept", content={"language": "zh-TW"})
        async with Client(import_module("15_elicitation").build_server(), elicitation_callback=answer) as client:
            self.assertNotIn("preference", (await client.list_tools()).tools[0].input_schema["properties"])
            result = await client.call_tool("prepare", {"topic": "MCP"})
            self.assertFalse(result.is_error); self.assertIn("zh-TW", result.content[0].text)

    async def test_mrtr_decline_does_not_prepare(self):
        async def answer(ctx, params): return ElicitResult(action="decline")
        async with Client(import_module("15_elicitation").build_server(), elicitation_callback=answer) as client:
            self.assertTrue((await client.call_tool("prepare", {"topic": "MCP"})).is_error)

    async def test_agent_allowlist_and_budget(self):
        run = import_module("17_agent_loop").run_agent
        # Exceptions may be grouped by the async context manager on exit.
        with self.assertRaises(Exception) as blocked:
            await run([{"name": "unknown", "arguments": {}}])
        self.assertTrue(any(isinstance(error, PermissionError) for error in exception_leaves(blocked.exception)))
        with self.assertRaises(Exception) as exhausted:
            await run([{"name": "search_notes", "arguments": {"query": "MCP"}}] * 3, max_calls=2)
        self.assertTrue(any(isinstance(error, RuntimeError) and "budget" in str(error) for error in exception_leaves(exhausted.exception)))

    async def test_concurrency_is_bounded_and_cleaned(self):
        report = await import_module("26_bounded_concurrency").run_batch(8, 2)
        self.assertEqual(report["peak"], 2); self.assertEqual(report["active_after"], 0)

    async def test_capstone_contract_hides_identity_and_review(self):
        with TemporaryDirectory() as folder:
            async with Client(build_capstone(WorkflowStore(Path(folder) / "test.sqlite"))) as client:
                tools = (await client.list_tools()).tools
                self.assertEqual({t.name for t in tools}, {"find_notes", "get_ticket", "preview_close_ticket", "close_ticket"})
                for tool in tools:
                    self.assertNotIn("tenant", tool.input_schema.get("properties", {}))
                    self.assertNotIn("approved", tool.input_schema.get("properties", {}))
                    self.assertIsNotNone(tool.output_schema)

    async def test_capstone_complete_and_delivery(self):
        with TemporaryDirectory() as folder:
            report = await import_module("30_delivery_report").deliver(Path(folder))
            self.assertEqual(report["audit_count"], 1)
            self.assertTrue((Path(folder) / "acceptance.json").is_file())


class AdapterTests(AsyncCase):
    async def test_upstream_schema_and_limits(self):
        import httpx2
        from upstream_adapter import fetch_status
        for status, content_type, data, succeeds in (
            (200, "application/json", b'{"service":"notes","status":"ok"}', True),
            (200, "text/html", b"not-json", False),
            (200, "application/json", b'{"service":"notes","status":"unknown"}', False),
            (429, "application/json", b'{}', False),
            (200, "application/json", b' ' * 5000, False),
        ):
            async def reply(request): return httpx2.Response(status, headers={"content-type": content_type}, content=data)
            async with httpx2.AsyncClient(transport=httpx2.MockTransport(reply), base_url="https://upstream.example.invalid") as http:
                if succeeds: self.assertEqual((await fetch_status(http)).status, "ok")
                else:
                    with self.assertRaises(ValueError): await fetch_status(http)

    async def test_protected_http_identity_and_scope(self):
        import httpx2
        from mcp.client.streamable_http import streamable_http_client
        from protected_server import build_protected_server
        with TemporaryDirectory() as folder:
            server = build_protected_server(WorkflowStore(Path(folder) / "protected.sqlite"))
            app = server.streamable_http_app(stateless_http=True, json_response=True)
            async with app.router.lifespan_context(app):
                async with httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://127.0.0.1:8765") as http:
                    self.assertEqual((await http.post("/mcp", json={})).status_code, 401)
                    http.headers["Authorization"] = "Bearer " + fixture_token(scope="notes:read")
                    async with Client(streamable_http_client("http://127.0.0.1:8765/mcp", http_client=http)) as client:
                        self.assertFalse((await client.call_tool("find_notes", {"query": "MCP"})).is_error)
                        self.assertTrue((await client.call_tool("get_ticket", {"ticket_id": "T1"})).is_error)


class TransportTests(AsyncCase):
    async def test_real_stdio_subprocess(self):
        params = StdioServerParameters(command=sys.executable, args=[str(HERE / "01_first_server.py"), "--serve"],
                                       cwd=str(HERE), env={"PYTHONUTF8": "1"})
        async with Client(params, read_timeout_seconds=10) as client:
            result = await client.call_tool("search_notes", {"query": "MCP"})
            self.assertFalse(result.is_error)

    async def test_real_http_and_origin_rejection(self):
        import httpx2
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
        with TemporaryDirectory() as folder, open(Path(folder) / "server.log", "wb") as log:
            process = subprocess.Popen([sys.executable, str(HERE / "05_http_server.py"), "--serve", "--port", str(port)],
                cwd=HERE, env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            try:
                for _ in range(150):
                    if process.poll() is not None: self.fail("Local server exited before readiness")
                    try:
                        reader, writer = await asyncio.open_connection("127.0.0.1", port)
                        writer.close(); await writer.wait_closed(); break
                    except OSError: await asyncio.sleep(0.1)
                else: self.fail("Local server did not become ready")
                url = f"http://127.0.0.1:{port}/mcp"
                async with Client(url, read_timeout_seconds=10) as client:
                    self.assertEqual(client.protocol_version, "2026-07-28")
                    self.assertFalse((await client.call_tool("search_notes", {"query": "MCP"})).is_error)
                async with httpx2.AsyncClient(trust_env=False) as http:
                    response = await http.post(url, headers={"Origin": "https://untrusted.example.invalid"}, json={})
                    self.assertEqual(response.status_code, 403)
            finally:
                process.terminate()
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
