"""Original offline teaching experiment; keep lm_core.py with this file."""
import math
from lm_core import print_json

def main():
    groups=[{'tokens':2,'nll_mean':1.},{'tokens':8,'nll_mean':3.}]
    total=sum(g['tokens'] for g in groups)
    correct=sum(g['tokens']*g['nll_mean'] for g in groups)/total
    wrong=sum(g['nll_mean'] for g in groups)/len(groups)
    print_json({'target_tokens':total,'weighted_nll':correct,'perplexity':math.exp(correct),
        'wrong_mean_batch_nll':wrong,'wrong_mean_batch_ppl':sum(math.exp(g['nll_mean']) for g in groups)/len(groups),
        'comparison_requires':'same tokenizer, text normalization, context and target masking'})

if __name__=='__main__':main()
