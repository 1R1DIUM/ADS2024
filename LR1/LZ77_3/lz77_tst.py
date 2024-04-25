import pickle

class IMAGE_METHODS:
    @staticmethod
    def img_to_str(bin_str):
        in_lst = []
        for byte in bin_str:
            in_lst.append(chr(byte))    

        in_str = "".join(in_lst)
        return in_str
    @staticmethod
    def str_to_byteArray(in_str):
        decoded_bin_lst = bytearray()
        for char in in_str:
            decoded_bin_lst.append(ord(char))
        return decoded_bin_lst





class LZ77:
    def encode_LZ77(self,in_str,buffer_size):
        result = []
        i =0
        buf_left_pos = 0
        buf_right_pos = 0
        
        buffer = in_str[buf_left_pos: buf_right_pos]
        lookahead_buffer = in_str[0:buffer_size]
        while i < len(in_str):
            lenght,pos = self.longest_match(buffer,lookahead_buffer)
            plus = 0
            if lenght <= 2:
                result.append(in_str[i])
                plus = 1
            else:
                result.append((i-buf_left_pos-pos,lenght))
                plus = lenght
            
            if len(buffer) > buffer_size:
                buf_left_pos+= plus
            buf_right_pos += plus
            i+= plus
            
            buffer = in_str[buf_left_pos: buf_right_pos]
            lookahead_buffer = in_str[i:i+buffer_size]
            if(len(buffer)> buffer_size):
                buf_left_pos += (len(buffer)-buffer_size)
                buffer = in_str[buf_left_pos: buf_right_pos]

        return result
    
    
    
    def longest_match(self,buffer, lookahead_buffer):
        max_len = 0
        max_pos = -1

        while 1:
            curr_len = max_len+1
            if curr_len > len(lookahead_buffer):
                break
            curr_pos = buffer.find(lookahead_buffer[0:curr_len])
            if curr_pos == -1:
                break
            max_pos = curr_pos
            max_len = curr_len
        

        return max_len,max_pos

    def decode_LZ77(self,coded_lst) -> str:
        decoded_lst = []
        Pos = 0
        for value in coded_lst:
            if isinstance(value,str):
                decoded_lst.append(value)
                Pos+=1 
            else:
                (Shift,PrefixLenght) = value
                preifxPos = Pos-Shift
                decoded_substr = "".join(decoded_lst[preifxPos:preifxPos+PrefixLenght])
                for sym in decoded_substr:
                    decoded_lst.append(sym)
                Pos = Pos+PrefixLenght
        decoded_str = "".join(decoded_lst)
        return decoded_str
    
    def encode_file(self,input_filename_format,output_filename_format,buffer_size):
        with open(input_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            in_str = read_f.read()
            encoded_lst = self.encode_LZ77(in_str,buffer_size)
            with open (output_filename_format,'wb') as write_f:
                pickle.dump(encoded_lst,write_f)
            
    def decode_file(self,input_filename_format,output_filename_format):
        with open(input_filename_format,'rb') as read_f:
            encoded_lst = pickle.load(read_f)
            decoded_str = self.decode_LZ77(encoded_lst)
            with open(output_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(decoded_str)
                
    def encode_file_bin(self,input_filename_format,output_filename_format,buffer_size):
        with open(input_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            encoded_lst = self.encode_LZ77(in_str,buffer_size)
            with open (output_filename_format,'wb') as write_f:
                pickle.dump(encoded_lst,write_f)
    
    def decode_file_bin(self,input_filename_format,output_filename_format):
        with open(input_filename_format,'rb') as read_f:
            encoded_lst = pickle.load(read_f)
            decoded_str = self.decode_LZ77(encoded_lst)
            ba = IMAGE_METHODS.str_to_byteArray(decoded_str)
            with open(output_filename_format,'wb',) as write_f:
                write_f.write(ba)
    


if __name__ == '__main__':
    # code_file = 'enwik7.txt'
    # com_file = 'enwik7_com.txt'
    # decom_file = 'enwik7_decom.txt'
    
    # lz = LZ77()
    # lz.encode_file(code_file,com_file,32768)
    # lz.decode_file(com_file,decom_file)
    
    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #         str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #         str2 = file2.read()
            
    # print(str1==str2)
    code_file = 'grey.raw'
    com_file = 'grey_com.txt'
    decom_file = 'grey_decom.raw'
    
    lz = LZ77()
    lz.encode_file_bin(code_file,com_file,32768)
    lz.decode_file_bin(com_file,decom_file)
    
    with open(code_file,'rb') as file1:
        str1 = file1.read()
    with open(decom_file,'rb') as file2:
        str2 = file2.read()
    print(str1==str2)
    


