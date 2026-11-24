"""Original offline teaching experiment; keep lm_core.py with this file."""
from lm_core import ByteTokenizer,print_json

def main():
    text='學AI🙂';tok=ByteTokenizer();ids=tok.encode(text)
    print_json({'text':text,'codepoints':len(text),'UTF8_bytes':list(text.encode()),
        'token_ids':ids,'decoded':tok.decode(ids),'special_ids':[tok.pad_id,tok.bos_id,tok.eos_id]})

if __name__=='__main__':main()
