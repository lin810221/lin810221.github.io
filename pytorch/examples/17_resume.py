"""Compare continuous CPU training with an epoch-boundary save/load resume."""
import json
from pathlib import Path
import tempfile
import torch
from course_core import Config, experiment, load_checkpoint, save_checkpoint

def main(argv=None):
    del argv
    config = Config(epochs=4)
    continuous = experiment(config)
    partial = experiment(config, stop_after=2)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/"resume.pt"
        save_checkpoint(path, partial["checkpoint"])
        resumed = experiment(config, resume=load_checkpoint(path))
    error = max((value-resumed["checkpoint"]["model"][key]).abs().max().item()
                for key,value in continuous["checkpoint"]["model"].items())
    result = {"maximum_parameter_difference": error, "epochs": len(resumed["history"]),
              "scope": "CPU, same config, full epoch boundary, workers=0"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
