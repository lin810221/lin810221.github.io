"""Variable-length token lists become padded tensors and an explicit mask."""
import json
from course_core import collate_sequences

def main(argv=None):
    del argv
    padded, mask, labels = collate_sequences([([1, 2], 0), ([3, 4, 5], 1), ([6], 0)])
    result = {"tokens": padded.tolist(), "mask": mask.tolist(), "labels": labels.tolist()}
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
