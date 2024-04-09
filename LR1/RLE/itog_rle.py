import pickle
class RLE:
    def encode(self,in_str,delim = '^') -> str:
        it = 0
        counter = 1
        out_lst = []
        while it < len(in_str)-1:
            if in_str[it] == in_str[it+1]:
                counter +=1
                it +=1
            else:
                if counter == 1:
                    
                    j = it
                    out_lst.append(delim + chr(counter))
                    while j < len(in_str)-1 and in_str[j] != in_str[j+1]:
                        out_lst.append(in_str[j])
                        j+=1
                    
                    if not (j< len(in_str)-1):
                        out_lst.append(in_str[j])
                    
                    it = j
                else:
                    while counter > 255:
                        out_lst.append(delim + chr(255) + in_str[it])
                        counter-=255
                    
                    out_lst.append(delim + chr(counter) + in_str[it])
                    counter = 1
                    it+=1
        if it < len(in_str)-1 or counter > 1:
            while counter > 255:
                out_lst.append(delim + chr(255) + in_str[it])
                counter -=255
            out_lst.append(delim + chr(counter) + in_str[it])
        return "".join(out_lst)
    
    def decode(self,encoded_str,DELIM) -> str:
        it = 1
        out_lst = []
        coded_lst = []
        while it < len(encoded_str):
            amount = ord(encoded_str[it])
            it+=1
            while it < len(encoded_str) and encoded_str[it] != DELIM:
                coded_lst.append(encoded_str[it])
                it+=1
            out_lst.append("".join(coded_lst)*amount)
            coded_lst.clear()
            it+=1
        return "".join(out_lst)
    
    def encode_file(self, in_filename_format, out_filename_format,DELIM = '^'):
        ''' Encode function. Automaticly adds DELIM to end of file
        '''
        with open(in_filename_format,'r',encoding='utf-8') as read_f:
            in_str = read_f.read() + DELIM

            data_lst = [DELIM,self.encode(in_str,DELIM)]
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return
    
    def decode_file(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            DELIM,encoded_str = data_lst
            
            decoded_str = self.decode(encoded_str,DELIM)
        
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(decoded_str)
                
    def encode_file_bin(self, in_filename_format, out_filename_format,DELIM = '^'):
        ''' Encode function. Automaticly adds DELIM to end of file
        '''
        with open(in_filename_format,'rb') as read_f:
            
            bin_str = read_f.read()# + DELIM

            in_lst = []
            
            for byte in bin_str:
                in_lst.append(chr(byte))    

            in_str = "".join(in_lst)
            data_lst = [DELIM,self.encode(in_str,DELIM)]
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return
    def decode_file_bin(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            DELIM,encoded_str = data_lst
            
            decoded_str = self.decode(encoded_str,DELIM)
            
            decoded_bin_lst = bytearray()
            for char in decoded_str:
                decoded_bin_lst.append(ord(char))
                
            with open(out_filename_format,'wb') as write_f:
                write_f.write(decoded_bin_lst)
    
    
    
    
if __name__ == '__main__':
    
    # code_file = r"RLE\wb.raw"
    # com_file = r"RLE\wb_com.txt"
    # decom_file = r"RLE\wb_decom.txt"
    # rle = RLE()
    
    # rle.encode_file_bin(code_file,com_file,'^')
    # rle.decode_file_bin(com_file,decom_file)
    
    # with open(code_file,'rb') as file1:
    #     str1 = file1.read()
    # with open(decom_file,'rb') as file2:
    #     str2 = file2.read()
    
    code_file = r"RLE\war_and_peace.ru.txt"
    com_file = r"RLE\war_com.txt"
    decom_file = r"RLE\war_decom.txt"
    rle = RLE()
    
    rle.encode_file(code_file,com_file,'^')
    rle.decode_file(com_file,decom_file)
    
    with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
        str1 = file1.read()
    with open(code_file,'r',encoding='utf-8',newline='\x0A') as file2:
        str2 = file2.read()
    
    
    
        
    print(str1==str2)



