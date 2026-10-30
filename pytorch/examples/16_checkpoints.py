"""A real weights_only checkpoint roundtrip inside a temporary directory."""
import json
from pathlib import Path
import tempfile
import torch
from course_core import Config, experiment, load_checkpoint, predict, save_checkpoint

def main(argv=None):
    del argv
    run = experiment(Config(epochs=2))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/"checkpoint.pt"
        save_checkpoint(path, run["checkpoint"])
        restored = load_checkpoint(path)
        equal = all(torch.equal(value, restored["model"][key]) for key,value in run["checkpoint"]["model"].items())
        result = {"model_state_equal": equal, "saved_epoch": restored["epoch"],
                  "prediction": predict(restored, [[0., 0., 0., 0.]])}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
