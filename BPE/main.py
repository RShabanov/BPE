from bpe import BpeDecoder, BpeEncoder
from sys import stdin

if __name__ == "__main__":
    input_text = stdin.read()
    
    encoder = BpeEncoder()
    seq, encoder_dict = encoder.encode(input_text)
    
    encoder.save("encoded-file.txt")
    
    print(BpeDecoder().decode(seq, encoder_dict))