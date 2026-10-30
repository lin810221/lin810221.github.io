"""A deterministic simulated model plus a real bounded tool executor; no API calls."""
import argparse
import json
from agent_core import run_agent, simulated_model, multiply
from live_agents import native_agent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["offline","openai","gemini","claude"], default="offline")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--question", default="請使用 multiply 工具計算 6 乘 7。")
    args = parser.parse_args()
    if args.provider == "offline":
        if args.live:
            parser.error("--live requires an online provider")
        result = run_agent(simulated_model, args.question, {"multiply":multiply})
        print(result["status"], result["answer"])
        print("固定模擬模型，只示範 6*7 的協定。")
    else:
        print(json.dumps(native_agent(args.provider,args.question,live=args.live),ensure_ascii=False,indent=2))
