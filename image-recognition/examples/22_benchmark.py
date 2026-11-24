"""Offline executable teaching example; run from this directory."""
from time import perf_counter
import statistics
import torch
from vision_core import TinyClassifier,seed_everything,print_json

def main():
    seed_everything();model=TinyClassifier().eval();x=torch.zeros(1,3,24,24)
    with torch.inference_mode():
        for _ in range(10):model(x)
        samples=[]
        for _ in range(50):
            start=perf_counter();model(x);samples.append((perf_counter()-start)*1000)
    print_json({'scope':'CPU model forward only; no decode/queue/transfer',
        'warmup':10,'repeats':50,'median_ms':statistics.median(samples),
        'p95_ms':sorted(samples)[47],'threads':torch.get_num_threads()})

if __name__=='__main__': main()
