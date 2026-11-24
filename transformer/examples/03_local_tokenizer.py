"""Original offline teaching experiment; keep lm_core.py with this file."""
from tokenizers import Tokenizer,models,pre_tokenizers,decoders,trainers
from lm_core import print_json

def build_tokenizer():
    tokenizer=Tokenizer(models.BPE())
    tokenizer.pre_tokenizer=pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder=decoders.ByteLevel()
    trainer=trainers.BpeTrainer(vocab_size=300,min_frequency=1,show_progress=False,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),special_tokens=['<pad>','<bos>','<eos>'])
    tokenizer.train_from_iterator(['red bird moves.','blue bird rests.','學習語言模型🙂'],trainer)
    return tokenizer

def main():
    tokenizer=build_tokenizer();text='新的文字🙂';encoded=tokenizer.encode(text)
    assert tokenizer.decode(encoded.ids)==text
    print_json({'vocab':tokenizer.get_vocab_size(),'ids':encoded.ids,'tokens':encoded.tokens,
                'round_trip':tokenizer.decode(encoded.ids),'downloads':False})

if __name__=='__main__':main()
