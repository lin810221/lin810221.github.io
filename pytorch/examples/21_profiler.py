"""Profile a small CPU forward/backward; no trace files are written by default."""
import json
import torch
from torch import nn
from course_core import setup

def main(argv=None):
    del argv
    setup()
    model = nn.Linear(4,3)
    x = torch.randn(8,4)
    with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],record_shapes=True) as profile:
        with torch.profiler.record_function("teaching_step"):
            model(x).square().mean().backward()
    events = profile.key_averages()
    result = {"event_count": len(events), "has_teaching_step": any(event.key=="teaching_step" for event in events),
              "device": "cpu", "scope": "Instrumentation example, not a speed benchmark"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
