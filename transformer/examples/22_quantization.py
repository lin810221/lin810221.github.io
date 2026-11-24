"""Original offline teaching experiment; keep lm_core.py with this file."""
import torch
from lm_core import print_json

def main():
    weights=torch.tensor([[-.8,-.3,.1,.7],[.02,-.01,.03,-.02]])
    scale=weights.abs().amax(-1,keepdim=True).clamp_min(1e-12)/127
    integers=torch.round(weights/scale).clamp(-127,127).to(torch.int8)
    restored=integers.float()*scale
    print_json({'symmetric_per_row_int8':integers.tolist(),'scale':scale.flatten().tolist(),
        'max_abs_error':float((restored-weights).abs().max()),
        'note':'dequantized reference; no optimized int8 inference/latency claim'})

if __name__=='__main__':main()
