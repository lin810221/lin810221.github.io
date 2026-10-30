"""Disjoint synthetic splits; validation selects best weights, test is separate."""
import json
from course_core import experiment

def main(argv=None):
    del argv
    run = experiment()
    result = {"initial_validation": run["initial_validation"], "final_validation": run["final_validation"],
              "test_of_best_validation_model": run["test"], "epochs": len(run["history"]), "data": "synthetic only"}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
