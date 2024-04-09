
class MTF:
        
    #def __init__(self,in_str : str) -> None:
        #self.alphabet = [x for x in set(in_str)]
    
    def encode(self,in_str:str,alphabet:list):
        out_lst = []
        alph = alphabet[:]
        for char in in_str:
            index = alph.index(char)
            out_lst.append(index)
            alph.remove(char)
            alph.insert(0,char)
        return out_lst


    def decode(self,in_str:str, alphabet :list)-> str:
        out_list = []
        out_alphabet = alphabet
        
        for num in in_str:
            char = out_alphabet[ord(num)]
            out_list.append(char)
            out_alphabet.remove(char)
            out_alphabet.insert(0,char)
        
        return "".join(out_list)
    
    

#print(MTF.encode(MTF,'abaacabad'))