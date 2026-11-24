"""Original offline teaching experiment; keep lm_core.py with this file."""
from lm_core import kv_bytes,print_json

def main():
    common={'batch':2,'layers':32,'length':4096,'head_dim':128,'bytes_per_element':2}
    result={name:kv_bytes(kv_heads=heads,**common)/2**30 for name,heads in [('MHA',32),('GQA',8),('MQA',1)]}
    print_json({'pure_KV_GiB':result,'excludes':['weights','activations','workspace','allocator','paging metadata']})

if __name__=='__main__':main()
