"""Original offline teaching experiment; keep lm_core.py with this file."""
from lm_core import TinyBPE,print_json

def main():
    tokenizer=TinyBPE().fit(['banana bandana','banana banana','學習AI'],steps=12)
    text='banana🙂';ids=tokenizer.encode(text)
    print_json({'merges':[{'pair':pair,'id':i,'bytes':list(tokenizer.pieces[i])} for pair,i in tokenizer.merges],
        'encoded':ids,'original_bytes':len(text.encode()),'decoded':tokenizer.decode(ids)})

if __name__=='__main__':main()
