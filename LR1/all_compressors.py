from queue import PriorityQueue
from bitarray import bitarray
import pickle


class Huffman:
    class Node():
        def __init__(self,char,freq) -> None:
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
            
        def __lt__(self,other : 'Huffman.Node'):
            return self.freq < other.freq
    
    def __init__(self) -> None:
        self.huffCodesDict :dict = {}
        self.huffCodesList : list = []
        
    def build_huff_tree(self,alph_and_freq = list[str,int]):
        q = PriorityQueue()
        for char in alph_and_freq:
            node = self.Node(char[0], char[1])
            q.put(node)

        while q.qsize() > 1:
            node1 = q.get()
            node2 = q.get()
            node = self.Node(node1.char + node2.char, node1.freq + node2.freq)
            node.left = node1
            node.right = node2
            q.put(node)
        node = q.get()
        return node
    
    def get_huff_codes(self,node : 'Node', start_code :str = ''):
        if node is None:
            return

        if (node.left is None) and (node.right is None):
            try:
                self.huffCodesList[self.huffCodesList.index(node.char)] = start_code
            except ValueError:
                self.huffCodesList.append([node.char,start_code])
            
        self.get_huff_codes(node.left, start_code + "0")
        self.get_huff_codes(node.right, start_code + "1")
        
    def getSorted_alph_freq(self,in_str :str):
        afList = []
        set_alphabet = sorted(set(in_str))
        for symbol in set_alphabet:
            curr_amount = in_str.count(symbol)
            afList.append((symbol,curr_amount))
        return sorted(afList, key= lambda x:[(x[1],x[0])])
    
    def toCanonicalHuffCodes(self):
        self.huffCodesList[0][1] = '0'*len(self.huffCodesList[0][1])
        for i in range(1, len(self.huffCodesList)):
            oldlen = len(self.huffCodesList[i][1]) 
            dif_len = len(self.huffCodesList[i][1]) - len(self.huffCodesList[i-1][1])
            self.huffCodesList[i][1] = bin(int(self.huffCodesList[i-1][1],2)+1)[2:].zfill(oldlen-dif_len) 
            
            while len(self.huffCodesList[i][1]) < oldlen:
                self.huffCodesList[i][1] +='0'
    
    def bit_str_to_chars(self,bit_str):

        out_lst =[]
        last_len = 0
        for i in range(0,len(bit_str),8):
            slice = bit_str[i:i+8]
            if len(slice) < 8:
                last_len = len(slice)
            out_lst.append(chr(int(bit_str[i:i+8],2)))
        str =  "".join(out_lst)
        
    
        return str,last_len
    
    def bit_str_to_bytes(self,bit_str):
        out_lst = []
        last_len = 0
        for i in range(0,len(bit_str),8):
            slice = bit_str[i:i+8]
            if len(slice) < 8:
                last_len = len(slice)
            out_lst.append((int(bit_str[i:i+8],2)))
        ba = bytearray(out_lst)
        
        return ba,last_len
        
    def sort_huff_code(self):
        self.huffCodesList.sort(key = lambda x:[[len(x[1]),x[0]]])
    
    def encode(self, in_str,alph_freq_list : list): 
        node = self.build_huff_tree(alph_freq_list)
        self.get_huff_codes(node)
        self.sort_huff_code()
        self.toCanonicalHuffCodes()

        for chr_ind in range(len(self.huffCodesList)):
            self.huffCodesDict[self.huffCodesList[chr_ind][0]] = bitarray(self.huffCodesList[chr_ind][1])
        
        encoded = bitarray()
        bitarray.encode(encoded,self.huffCodesDict,in_str)
        
        encoded_str,last_len = self.bit_str_to_bytes(encoded.to01())
        
        return encoded_str,last_len 
    
    def encode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format,'r',encoding='utf-8') as read_f:
            
            in_str = read_f.read()
            
            alph_freq_list = self.getSorted_alph_freq(in_str)
            byte_str,last_len = self.encode(in_str,alph_freq_list)
            
            
            with open(out_filename_format,'wb')as write_f:
                pickle.dump(self.huffCodesDict,write_f)
            
                write_f.write(b'\n')
                write_f.write(byte_str)
                
                last = bytearray()
                last.append(last_len)
                write_f.write(bytearray(last))
    
    def encode_file_bin(self,in_filename_format,out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            
            bin_str = read_f.read()
            in_lst = []
            
            for byte in bin_str:
                in_lst.append(chr(byte))
            in_str = "".join(in_lst)

            alph_freq_list = self.getSorted_alph_freq(in_str)
            byte_str,last_len = self.encode(in_str,alph_freq_list)
            
            
            with open(out_filename_format,'wb')as write_f:
                pickle.dump(self.huffCodesDict,write_f)
            
                write_f.write(b'\n')
                write_f.write(byte_str)
                
                last = bytearray()
                last.append(last_len)
                write_f.write(bytearray(last))
    
    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open(in_filename_format, 'rb') as read_f:
            huff_dict = pickle.load(read_f)

            read_f.readline()
            encoded_text_pos = read_f.tell()
            
            with open(out_filename_format,'wb') as write_f:
                read_f.seek(0,2) #? to end of file
                file_size = read_f.tell() -encoded_text_pos - 1
                
                read_f.seek(-1,2)
                last_len = int.from_bytes(read_f.read(1))
                read_f.seek(encoded_text_pos)
                
                bit_lst = []
                encoded_data = read_f.read()
                for symbol_ind in range(len(encoded_data)-1):
                    symbol = encoded_data[symbol_ind]
                    bit_symbol = bin(symbol)[2:]
                    if symbol_ind == len(encoded_data)-2:   
                        bit_symbol = bit_symbol.zfill(last_len)
                    else:
                        bit_symbol = bit_symbol.zfill(8)
                    bit_lst.append(bit_symbol)
                
                
                encoded_bit_str = "".join(bit_lst)
                decoded_bit_str = bitarray(encoded_bit_str)
                decoded_list = decoded_bit_str.decode(huff_dict)
                decoded_str = "".join(decoded_list)
                
                decoded_bin_lst = bytearray()
                for char in decoded_str:
                    decoded_bin_lst.append(ord(char))
                
                write_f.write(decoded_bin_lst)
    
    def decode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format, 'rb') as read_f:
            huff_dict = pickle.load(read_f)
        
            
            read_f.readline()
            encoded_text_pos = read_f.tell()
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                read_f.seek(0,2) #? to end of file

                
                read_f.seek(-1,2)
                last_len = int.from_bytes(read_f.read(1))
                read_f.seek(encoded_text_pos)
                
                bit_lst = []
                encoded_data = read_f.read()
                for symbol_ind in range(len(encoded_data)-1):
                    symbol = encoded_data[symbol_ind]
                    bit_symbol = bin(symbol)[2:]
                    if symbol_ind == len(encoded_data)-2:   
                        bit_symbol = bit_symbol.zfill(last_len)
                    else:
                        bit_symbol = bit_symbol.zfill(8)
                    bit_lst.append(bit_symbol)
                
                
                encoded_bit_str = "".join(bit_lst)
                decoded_bit_str = bitarray(encoded_bit_str)
                decoded_list = decoded_bit_str.decode(huff_dict)
                decoded_str = "".join(decoded_list)
                write_f.write(decoded_str.replace('\n','\x0A'))

import math
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



class AC:
    @staticmethod
    def getSorted_alph_freq(in_str :str):
        afList = []
        set_alphabet = sorted(set(in_str))
        for symbol in set_alphabet:
            curr_amount = in_str.count(symbol)
            afList.append((symbol,curr_amount))
        return sorted(afList, key= lambda x:[(x[1],x[0])])
    
    
    def encode(self,in_str) ->bytearray:

        alphabet_list = []
        cum_sum = 0
        cum_list = [0]
        TOTAL_CUM = 0

        alph_freq_lst= self.getSorted_alph_freq(in_str)

        #!total cumulitive frequency
        for i in range(len(alph_freq_lst)):
            cum_sum+=alph_freq_lst[i][1]
            alphabet_list.append(alph_freq_lst[i][0])
            TOTAL_CUM += alph_freq_lst[i][1]
            cum_list.append(cum_sum)

        alph_indexes = [i for i in range(len(alph_freq_lst))]
        alphabet_dict = dict(zip(alphabet_list,alph_indexes))


        bitlen = 2+ math.ceil(math.log2(TOTAL_CUM))
        max_len = 2**bitlen


        left = 0
        right = max_len-1

        bit_stream = []
        underflow_count = 0

        for char in in_str:
            lenght =right -left + 1

            left_freq = cum_list[alphabet_dict[char]]/TOTAL_CUM
            righ_freq = cum_list[alphabet_dict[char]+1]/TOTAL_CUM
            left,right = left + math.floor(lenght*left_freq), left + math.floor(lenght*righ_freq) -1

            while left >= max_len/2 or right <= max_len/2 or (
                max_len/4 <= left < max_len/2 < right <= 3*max_len/4):

                if left >= max_len/2 or right <= max_len/2:

                    at = bin(left)[2:].zfill(bitlen)
                    same_bit = bin(left)[2:].zfill(bitlen)[0]


                    left = int(bin(left)[2:].zfill(bitlen)[1:] + '0',2)   #? shift left by 1; LSB = 0
                    right = int(bin(right)[2:].zfill(bitlen)[1:] + '1',2) #? shift left by 1; LSB = 1

                    bit_stream.append(same_bit)
                    for _ in range(underflow_count):
                        bit_stream.append(str(int(not int(same_bit))))


                    underflow_count = 0

                if (max_len/4 <= left < max_len/2 < right <= 3*max_len/4):
                    underflow_count+=1

                    binary = bin(left)[2:].zfill(bitlen)[1:]
                    left = int(str(int(not int(binary[0]))) + binary[1:] + '0',2)  #? shift left by 1; inverse MSB; LSB = 0
                    binary = bin(right)[2:].zfill(bitlen)[1:]
                    right = int(str(int(not int(binary[0]))) + binary[1:] + '1',2) #? shift left by 1; inverse MSB; LSB = 1
                    pass

        if left <= max_len/4:
            bit_stream.append('0')
            for _ in range(underflow_count+1):
                        bit_stream.append('1')
        else:
            bit_stream.append('1')
            for _ in range(underflow_count+1):
                        bit_stream.append('0')

        bytes_len = len(bit_stream)//8 + 1

        for _ in range(bytes_len*8-len(bit_stream)):
            bit_stream.append('0')


        bit_str = "".join(bit_stream)

        out_lst = []
        for i in range(0,len(bit_str),8):
            out_lst.append((int(bit_str[i:i+8],2)))

        ba = bytearray(out_lst)





        print('encoded')

        return ba

    def decode(self,bytes, alph_freq_lst : list,len_str:int) -> str:

        bit_stream_lst  = []
        for symbol_ind in range(len(bytes)):
            symbol = bytes[symbol_ind]
            bit_symbol = bin(symbol)[2:].zfill(8)
            for k in range(0,8):
                bit_stream_lst.append(bit_symbol[k])

        bit_stream_str = "".join(bit_stream_lst)


        alphabet_list = []
        cum_sum = 0
        cum_list = [0]
        TOTAL_CUM = 0 #!total cumulitive frequency



        for i in range(len(alph_freq_lst)):
            cum_sum+=alph_freq_lst[i][1]

            alphabet_list.append(alph_freq_lst[i][0])
            TOTAL_CUM += alph_freq_lst[i][1]
            cum_list.append(cum_sum)

        alph_indexes = [i for i in range(len(alph_freq_lst))]
        alphabet_dict = dict(zip(alphabet_list,alph_indexes))

        bitlen = 2+ math.ceil(math.log2(TOTAL_CUM))
        max_len = 2**bitlen

        alh_reverse_dict = { value : key for key,value in alphabet_dict.items()}
        left = 0
        right = max_len-1

        decoded_mgs = []


        TAG = int(bit_stream_str[:bitlen],2)



        curr_symbol_ind = bitlen
        while curr_symbol_ind < len(bit_stream_str):

            k = 0
            val =math.floor(((TAG-left+1)* TOTAL_CUM -1)/ (right-left+1) )
            while val>=cum_list[k]:
                k+=1

            decoded_mgs.append(alh_reverse_dict[k-1])

            lenght =right -left + 1
            left_freq = cum_list[k-1]/TOTAL_CUM
            righ_freq = cum_list[k]/TOTAL_CUM
            left,right = left + math.floor(lenght*left_freq), left + math.floor(lenght*righ_freq) -1


            if len(decoded_mgs) == len_str-1:
                break


            while (left >= max_len/2 or right <= max_len/2 or (
                max_len/4 <= left < max_len/2 < right <= 3*max_len/4)) and curr_symbol_ind < len(bit_stream_str)-1:

                if left >= max_len/2 or right <= max_len/2:
                    left = int(bin(left)[2:].zfill(bitlen)[1:] + '0',2)   #? shift left by 1; LSB = 0
                    right = int(bin(right)[2:].zfill(bitlen)[1:] + '1',2) #? shift left by 1; LSB = 1
                    TAG = int(bin(TAG)[2:].zfill(bitlen)[1:] + bit_stream_str[curr_symbol_ind],2)

                    binary = bin(TAG)[2:].zfill(bitlen)[1:]
                    curr_symbol_ind +=1

                if (max_len/4 <= left < max_len/2 < right <= 3*max_len/4):
                    binary = bin(left)[2:].zfill(bitlen)[1:]
                    left = int(str(int(not int(binary[0]))) + binary[1:] + '0',2)  #? shift left by 1; inverse MSB; LSB = 0
                    binary = bin(right)[2:].zfill(bitlen)[1:]
                    right = int(str(int(not int(binary[0]))) + binary[1:] + '1',2) #? shift left by 1; inverse MSB; LSB = 1

                    binary = bin(TAG)[2:].zfill(bitlen)[1:]

                    TAG = int(str(int(not int(binary[0]))) + binary[1:] + bit_stream_str[curr_symbol_ind],2)

                    curr_symbol_ind+=1


        return "".join(decoded_mgs)



    def encode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            in_str = read_f.read() + '$'
            alph_freq = self.getSorted_alph_freq(in_str)
            encoded_msg = self.encode(in_str)
            len_str = len(in_str)

            data_lst = [alph_freq,encoded_msg,len_str]
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')


    def decode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            alph_freq,encoded_msg,len_str = data_lst

            decoded_msg = self.decode(encoded_msg,alph_freq,len_str)

            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(decoded_msg)


    def encode_file_bin(self,in_filename_format,out_filename_format):
            with open(in_filename_format,'rb') as read_f:
                bin_str = read_f.read()
                in_str = IMAGE_METHODS.img_to_str(bin_str) + '$'

                alph_freq = self.getSorted_alph_freq(in_str)
                encoded_msg = self.encode(in_str)
                len_str = len(in_str)

                data_lst = [alph_freq,encoded_msg,len_str]
                with open(out_filename_format,'wb') as write_f:
                    pickle.dump(data_lst,write_f)
                    write_f.write(b'\n')


    def decode_file_bin(self,in_filename_format,out_filename_format):
            with open(in_filename_format, 'rb') as read_f:
                data_lst = pickle.load(read_f)
                alph_freq,encoded_msg,len_str = data_lst

                decoded_msg = self.decode(encoded_msg,alph_freq,len_str)

                ba = IMAGE_METHODS.str_to_byteArray(decoded_msg)
                with open(out_filename_format,'wb') as write_f:
                    write_f.write(ba)

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


class MTF:
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
    

class BWT_MTF:
    @staticmethod
    def encode(in_str,BWT_DELIM):
        '''$ added auto. Returns unicode list and data list [BWT_index,MTF_alphabet]'''
        bwt = BWT()
        index,bwt_string = bwt.encode(in_str+BWT_DELIM)
        mtf = MTF()
        HUFFMAN_CLASS = Huffman()
        
        alph = []
        alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(bwt_string)
        for eleme in alph_freq_list:
            alph.append(eleme[0])
        
        alph.reverse()
        mtf_lst = MTF.encode(bwt_string,alph)
        
        uni_mtf_list = []
        for num in mtf_lst:
            uni_mtf_list.append(chr(num))
            
        data_list = [index,alph]   #!DATA LIST
        return uni_mtf_list,data_list
    @staticmethod
    def decode(encoded_str, BWT_index,MTF_alphabet):
        mtf = MTF()
        after_mtf_str = MTF.decode(encoded_str,MTF_alphabet)
        
        mtf = BWT()
        after_bwt_str = BWT.decode(BWT_index,after_mtf_str)
        return after_bwt_str


    @staticmethod
    def get_unique_symbol(in_str : str):
        for i in range(0,int('0x10ffff',16)):
            if chr(i) not in in_str:
                return chr(i)


class BWT_MTF_HA:
    
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            HUFFMAN_CLASS = Huffman()
            uni_mtf_list, data_list = BWT_MTF.encode(read_f.read(),BWT_DELIM)
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq("".join(uni_mtf_list))
            encoded_huf,last_len = HUFFMAN_CLASS.encode("".join(uni_mtf_list),alph_freq_list)
                  
            data_list.append(last_len)
            data_list.append(HUFFMAN_CLASS.huffCodesDict)
            data_list.append(encoded_huf)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)
    
    def decode_Huf(self,encoded_data,last_len,huff_dict):
        bit_lst = []

        for symbol_ind in range(len(encoded_data)):
            symbol = encoded_data[symbol_ind]
            bit_symbol = bin(symbol)[2:]
            if symbol_ind == len(encoded_data)-1:   
                bit_symbol = bit_symbol.zfill(last_len)
            else:
                bit_symbol = bit_symbol.zfill(8)
            bit_lst.append(bit_symbol)
        
        
        encoded_bit_str = "".join(bit_lst)
        decoded_bit_str = bitarray(encoded_bit_str)
        decoded_list = decoded_bit_str.decode(huff_dict)
        decoded_str = "".join(decoded_list)
        return decoded_str
    
    def decode_file(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,HUF_last_len,huf_dict,encoded_huf = data_list
            
            after_huf_str = self.decode_Huf(encoded_huf,HUF_last_len,huf_dict)
            after_bwt_str = BWT_MTF.decode(after_huf_str,BWT_index,MTF_alphabet)
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = Huffman()
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq("".join(uni_mtf_list))
            encoded_huf,last_len = HUFFMAN_CLASS.encode("".join(uni_mtf_list),alph_freq_list)
            data_list.append(last_len)
            data_list.append(HUFFMAN_CLASS.huffCodesDict)
            data_list.append(encoded_huf)
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)

    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,HUF_last_len,huf_dict,encoded_huf = data_list
            after_huf_str = self.decode_Huf(encoded_huf,HUF_last_len,huf_dict)
            after_bwt_str = BWT_MTF.decode(after_huf_str,BWT_index,MTF_alphabet)
            
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)


class BWT_MTF_AC:
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        #BWT = itog_bwt.BWT()
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:

            HUFFMAN_CLASS = Huffman()
            
            uni_mtf_list, data_list = BWT_MTF.encode(read_f.read(),BWT_DELIM)
            
            uni_mtf_str = "".join(uni_mtf_list) + '$'
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(uni_mtf_str)
            ac = AC()
            encoded_ac = ac.encode(uni_mtf_str)
            
            data_list.append(alph_freq_list)
            data_list.append(len(uni_mtf_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)
    

    
    def decode_file(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,alph_freq_list,str_len,encoded_ac = data_list
            
            ac = AC()
            after_ac_str = ac.decode(encoded_ac,alph_freq_list,str_len)

            after_bwt_str = BWT_MTF.decode(after_ac_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = Huffman()
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            uni_mtf_str = "".join(uni_mtf_list) + '$'
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(uni_mtf_str)
            ac = AC()
            encoded_ac = ac.encode(uni_mtf_str)
            
            data_list.append(alph_freq_list)
            data_list.append(len(uni_mtf_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)

    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,alph_freq_list,str_len,encoded_ac = data_list
            ac = AC()
            after_ac_str = ac.decode(encoded_ac,alph_freq_list,str_len)
            after_bwt_str = BWT_MTF.decode(after_ac_str,BWT_index,MTF_alphabet)
            
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)

class BWT_MTF_RLE_HA:
        
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            HUFFMAN_CLASS = Huffman()

            in_str = read_f.read()
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = RLE()   
            
            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
            
            
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM)
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            
        
            encoded_huf,last_len = HUFFMAN_CLASS.encode(after_rle_str,alph_freq_list)

            
            
            data_list.append(RLE_DELIM)
            data_list.append(last_len)
            data_list.append(HUFFMAN_CLASS.huffCodesDict)
            data_list.append(encoded_huf)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)
    
    def decode_Huf(self,encoded_data,last_len,huff_dict):
        bit_lst = []

        for symbol_ind in range(len(encoded_data)):
            symbol = encoded_data[symbol_ind]
            bit_symbol = bin(symbol)[2:]
            if symbol_ind == len(encoded_data)-1:   
                bit_symbol = bit_symbol.zfill(last_len)
            else:
                bit_symbol = bit_symbol.zfill(8)
            bit_lst.append(bit_symbol)
        
        
        encoded_bit_str = "".join(bit_lst)
        decoded_bit_str = bitarray(encoded_bit_str)
        decoded_list = decoded_bit_str.decode(huff_dict)
        decoded_str = "".join(decoded_list)
        return decoded_str
    
    def decode_file(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,RLE_DELIM, HUF_last_len,huf_dict,encoded_huf = data_list
            
            after_huf_str = self.decode_Huf(encoded_huf,HUF_last_len,huf_dict)
           
            rle = RLE()
           
            decoded_rle_str =rle.decode(after_huf_str,RLE_DELIM)
            
            
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = Huffman()
            
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = RLE()

            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
                
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM)
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            encoded_huf,last_len = HUFFMAN_CLASS.encode(after_rle_str,alph_freq_list)
            
            data_list.append(RLE_DELIM)
            data_list.append(last_len)
            data_list.append(HUFFMAN_CLASS.huffCodesDict)
            data_list.append(encoded_huf)
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)

    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,RLE_DELIM,HUF_last_len,huf_dict,encoded_huf = data_list
            
            after_huf_str = self.decode_Huf(encoded_huf,HUF_last_len,huf_dict)
            
            rle = RLE()
            decoded_rle_str =rle.decode(after_huf_str,RLE_DELIM)
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
        
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)
                
                

class BWT_MTF_RLE_AC:
        
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            HUFFMAN_CLASS = Huffman()

            in_str = read_f.read()
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = RLE()   
            
            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
            
            
            
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM) + '$'
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            
            ac = AC()
            encoded_ac = ac.encode(after_rle_str)

            
            
            data_list.append(RLE_DELIM)
            data_list.append(alph_freq_list)
            data_list.append(len(after_rle_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)
    
    
    def decode_file(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,RLE_DELIM,alph_freq_list ,str_len,encoded_ac = data_list
            
            ac = AC()
            after_ac_str = ac.decode(encoded_ac,alph_freq_list,str_len)
           
            rle = RLE()
           
            decoded_rle_str =rle.decode(after_ac_str,RLE_DELIM)
            
            
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = Huffman()
            
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = RLE()

            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
                
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM) + '$'
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            
            ac = AC()
            encoded_ac = ac.encode(after_rle_str)

            
            
            data_list.append(RLE_DELIM)
            data_list.append(alph_freq_list)
            data_list.append(len(after_rle_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)

    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,RLE_DELIM,alph_freq_list ,str_len,encoded_ac = data_list
            
            ac = AC()
            after_ac_str = ac.decode(encoded_ac,alph_freq_list,str_len)
            
            
            rle = RLE()
            decoded_rle_str =rle.decode(after_ac_str,RLE_DELIM)
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
        
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)
                
                
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


import os
class LZ77_HA:
    def encode_file(self,input_filename_format,output_filename_format,buffer_size):
        lz77 = LZ77()
        lz77.encode_file(input_filename_format,'temp.txt',buffer_size)
        ha = Huffman()
        ha.encode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')
        
    def decode_file(self,input_filename_format,output_filename_format):
        ha = Huffman()
        ha.decode_file_bin(input_filename_format,'temp.txt')
        lz77 = LZ77()
        lz77.decode_file('temp.txt',output_filename_format)
        os.remove('temp.txt')
    
    def encode_file_bin(self,input_filename_format,output_filename_format,buffer_size):
        lz77 = LZ77()
        lz77.encode_file_bin(input_filename_format,'temp.txt',buffer_size)
        ha = Huffman()
        ha.encode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')
    
    def decode_file_bin(self,input_filename_format,output_filename_format):
        ha = Huffman()
        ha.decode_file_bin(input_filename_format,'temp.txt')
        lz77 = LZ77()
        lz77.decode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')
    
class LZ77_AC:
    def encode_file(self,input_filename_format,output_filename_format,buffer_size):
        lz77 = LZ77()
        lz77.encode_file(input_filename_format,'temp.txt',buffer_size)
        ac = AC()
        ac.encode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')
    def decode_file(self,input_filename_format,output_filename_format):
        ac = AC()
        ac.decode_file_bin(input_filename_format,'temp.txt')
        lz77 = LZ77()
        lz77.decode_file('temp.txt',output_filename_format)
        os.remove('temp.txt')

    def encode_file_bin(self,input_filename_format,output_filename_format,buffer_size):
        lz77 = LZ77()
        lz77.encode_file_bin(input_filename_format,'temp.txt',buffer_size)
        ac = AC()
        ac.encode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')
    
    def decode_file_bin(self,input_filename_format,output_filename_format):
        ac = AC()
        ac.decode_file_bin(input_filename_format,'temp.txt')
        lz77 = LZ77()
        lz77.decode_file_bin('temp.txt',output_filename_format)
        os.remove('temp.txt')

if __name__ == '__main__':
    
    code_file = 'LR1\\war_and_peace.ru.txt'
    com_file = 'LR1\\war_and_peace_com.txt'
    decom_file = 'LR1\\war_and_peace_decom.txt'
    