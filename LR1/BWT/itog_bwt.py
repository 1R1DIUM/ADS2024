import pickle
import sufarray
class BWT:
    def __init__(self) -> None:
        self.encoded_str = ''

    def encode(self,in_str):
        sArray = sufarray.SufArray(in_str)
        suffix_array = sArray.get_array()
        index = suffix_array.index(0)
        encoded_data = []
        for j in suffix_array:
            i = j-1
            if i < 0:
                i += len(suffix_array)
            encoded_data.append(in_str[i])
        return index, "".join(encoded_data)
    
    def decode(self,index, encoded_str) -> str:

        shifts = [(encoded_str[i],i) for i in range(len(encoded_str))]
        shifts.sort()
        new_indixes = list(zip(*shifts))[1]
        decoded = []
        ind = index
        for _ in range(len(encoded_str)-1):
            ind = new_indixes[ind]
            decoded.append(encoded_str[ind])
        return "".join(decoded)
    
    def encode_file(self, in_filename_format, out_filename_format,DELIM = '$'):
        ''' Encode function. Automaticly adds DELIM to end of file
        '''
        with open(in_filename_format,'r',encoding='utf-8') as read_f:
            in_str = read_f.read() + DELIM
            index, encoded_str = self.encode(in_str)
            self.encoded_str = encoded_str
            data_lst = [index,self.encoded_str]
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return

        
        
    def decode_file(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            index,encoded_str = data_lst
            
            decoded_str = self.decode(index,encoded_str)
            
            with open(out_filename_format,'w',encoding='utf-8', newline='\x0A') as write_f:
                write_f.write(decoded_str[0:-1])
    
bwt = BWT()
#bwt.encode_file("war_and_peace.test.txt",'war_bwt.txt')


# with open('war_bwt.txt','rb') as read_b:
#     lst = pickle.load(read_b)
#     pass

# with open('war_and_peace.ru.txt','r',encoding='utf-8') as read_f:
#     str1 = read_f.read()
    
# print(len(str1) == len(lst[2]))

#bwt.decode_file('war_bwt.txt','war_bwt_decoded.txt')

# with open('war_and_peace.test.txt','r',encoding='utf-8') as f1:
#     str1 = f1.read()
# with open('war_bwt_decoded.txt','r',encoding='utf-8') as f2:
#     str2 = f2.read()


ind, enc = bwt.encode("abrakadabra$")
print(bwt.decode(ind,enc))
