"""Offline executable teaching example; run from this directory."""
from vision_core import toy_ap,print_json

def main():
    truths={'a':[[0,0,10,10]],'b':[[0,0,10,10]]}
    predictions=[{'image':'a','box':[0,0,10,10],'score':.9},
                 {'image':'a','box':[0,0,10,10],'score':.8},
                 {'image':'b','box':[0,0,10,10],'score':.7}]
    print_json(toy_ap(predictions,truths)) # AP=5/6; duplicate is false positive.

if __name__=='__main__': main()
