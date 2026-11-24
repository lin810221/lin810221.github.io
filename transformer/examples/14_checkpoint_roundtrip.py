"""Original offline teaching experiment; keep lm_core.py with this file."""
from tempfile import TemporaryDirectory
import torch
from lm_core import TinyGPT,save_artifact,load_artifact,seed_everything,print_json

def main():
    seed_everything();model=TinyGPT().eval();ids=torch.tensor([[1,10,11]])
    with TemporaryDirectory() as folder:
        manifest=save_artifact(model,folder);restored=load_artifact(folder)
        with torch.inference_mode():error=float((model(ids)['logits']-restored(ids)['logits']).abs().max())
    print_json({'max_logit_error':error,'sha256':manifest['sha256'],
        'tied_after_load':restored.head.weight is restored.embedding.weight,
        'not_exact_training_resume':'optimizer/RNG/data-order are not saved by this inference artifact'})

if __name__=='__main__':main()
