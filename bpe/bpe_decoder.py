from collections import defaultdict

class BpeDecoderException(Exception):
    pass
    
class BpeDecoder:
    
    def __init__(self) -> None:
        pass
    
    def _get_key_chain(self, key: int, encoder_dict: defaultdict) -> list:
        if key in encoder_dict:
            pair = encoder_dict[key]
            return self._get_key_chain(pair[0], encoder_dict) + self._get_key_chain(pair[1], encoder_dict)
        return [key]
    
    def _find_key(self, key: int, seq: list) -> list:
        indices: list = []
        for idx in range(len(seq)):
            if seq[idx] == key:
                indices.append(idx)
        return indices
    
    def _to_bytearray(self, seq: list) -> bytearray:
        FIRST_UTF8_BYTE: int = 0b1100_0000
        SECOND_UTF8_BYTE: int = 0b1000_0000
        byte_seq = bytearray()

        i = 0
        while i < len(seq):
            if seq[i] & FIRST_UTF8_BYTE:
                if seq[i + 1] & SECOND_UTF8_BYTE:
                    byte_seq.extend(bytearray(seq[i:i + 2]))
                    i += 1
                else:
                    raise BpeDecoderException("Bad UTF-8 code sequence")
            else:
                byte_seq.extend(bytearray([seq[i]]))    
            i += 1  
        return byte_seq              
    
    def decode(self, seq: list, encoder_dict: defaultdict, filename: str=None, encoding="utf-8") -> str:
        for key in sorted(encoder_dict.keys(), reverse=True):
            key_chain = self._get_key_chain(key, encoder_dict)
            
            if len(key_chain) > 1:
                for idx in sorted(self._find_key(key, seq), reverse=True):
                    seq = seq[:idx] + key_chain + seq[idx + 1:]
        
        byte_seq = self._to_bytearray(seq)
        
        decoded_seq = bytearray.decode(byte_seq, encoding)
        
        if filename is not None:
            with open(filename, 'w') as file:
                file.write(decoded_seq)
        
        return decoded_seq