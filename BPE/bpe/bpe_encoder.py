from collections import Counter, defaultdict

class BpeEncoderException(Exception):
    pass

class BpeEncoder:

    def __init__(self) -> None:
        self._seq = None
        self._dict = defaultdict()

    def _byte_seq(self, text:str, encoding: str="utf-8") -> None:
        self._seq = list(bytes(text, encoding))
        self._dict = defaultdict()

    def _find_pair(self, pair: tuple) -> list:
        if len(pair) > len(self._seq):
            return None
        
        indices: list = []
        for i in range(len(self._seq) - 1):
            if pair == (self._seq[i], self._seq[i + 1]):
                indices.append(i)
        return indices

    def _replace_pair_with_key(self, key: int, indices: list) -> None:
        for idx in indices[::-1]:
            self._seq[idx] = key
            self._seq = self._seq[:idx + 1] + self._seq[idx + 2:]
            
    def encode_from_file(self, filename: str, encoding:str="utf-8") -> tuple:
        with open(filename, 'r', encoding=encoding) as file:
            return self.encode(file.read())
            
    def encode(self, text:str) -> tuple:
        self._byte_seq(text)
        
        i: int = 0
        new_key: int = 256 # since byte is only 0..255
        byte_dict = Counter(self._seq)
        keys: list = list(byte_dict.keys())
        
        while i < len(keys):
            j: int = 0
            while j < len(keys):
                pair = (keys[i], keys[j])
                pair_indices = self._find_pair(pair)
                pair_occurrence_number = len(pair_indices)
                
                if pair_occurrence_number > 1:
                    self._replace_pair_with_key(new_key, pair_indices)
                    
                    byte_dict[pair[0]] -= pair_occurrence_number
                    byte_dict[pair[1]] -= pair_occurrence_number
                    
                    self._dict[new_key] = pair
                    byte_dict[new_key] = pair_occurrence_number
                    
                    keys = list(byte_dict.keys())
                    
                    new_key += 1
                j += 1
            i += 1
        return (self._seq, self._dict) 
    
    def save(self, filename:str, encoding: str="utf-8") -> None:
        with open(filename, 'w', encoding=encoding) as file:
            file.write(f"{self._seq}\n\n{self._dict}")
    