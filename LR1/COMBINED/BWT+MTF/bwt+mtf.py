import pickle
import itog_mtf
import itog2
import itog_bwt
import itog_rle

from ac import encode,decode


from bitarray import bitarray

# MTF_class = itog_mtf.MTF()

class BWT_MTF_HA:
    
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        #BWT = itog_bwt.BWT()
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            #index,bwt_string = BWT.encode(read_f.read()+BWT_DELIM)
           # MTF = itog_mtf.MTF()
            HUFFMAN_CLASS = itog2.Huffman()
            
            # alph = []
            # alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(bwt_string)
            # for eleme in alph_freq_list:
            #     alph.append(eleme[0])
            
            # alph.reverse()
            # mtf_lst = MTF.encode(bwt_string,alph)
            
            # uni_mtf_list = []
            # for num in mtf_lst:
            #     uni_mtf_list.append(chr(num))
            uni_mtf_list, data_list = BWT_MTF.encode(read_f.read(),BWT_DELIM)
            
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq("".join(uni_mtf_list))
            encoded_huf,last_len = HUFFMAN_CLASS.encode("".join(uni_mtf_list),alph_freq_list)
            
            #data_list = [index,alph,last_len,HUFFMAN_CLASS.huffCodesDict ,encoded_huf]
            
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
            # MTF = itog_mtf.MTF()
            # after_mtf_str = MTF.decode(after_huf_str,MTF_alphabet)
            
            # BWT = itog_bwt.BWT()
            # after_bwt_str = BWT.decode(BWT_index,after_mtf_str)
            after_bwt_str = BWT_MTF.decode(after_huf_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = itog2.Huffman()
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

class BWT_MTF_RLE_HA:
        
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            HUFFMAN_CLASS = itog2.Huffman()

            in_str = read_f.read()
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = itog_rle.RLE()   
            
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
           
            rle = itog_rle.RLE()
           
            decoded_rle_str =rle.decode(after_huf_str,RLE_DELIM)
            
            
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = itog2.Huffman()
            
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = itog_rle.RLE()

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
            
            rle = itog_rle.RLE()
            decoded_rle_str =rle.decode(after_huf_str,RLE_DELIM)
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
        
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)


            
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
           


class BWT_MTF_AC:
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        #BWT = itog_bwt.BWT()
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:

            HUFFMAN_CLASS = itog2.Huffman()
            
            uni_mtf_list, data_list = BWT_MTF.encode(read_f.read(),BWT_DELIM)
            
            uni_mtf_str = "".join(uni_mtf_list) + '$'
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(uni_mtf_str)
            encoded_ac = encode(uni_mtf_str)
            

            
            data_list.append(alph_freq_list)
            data_list.append(len(uni_mtf_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)
    

    
    def decode_file(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,alph_freq_list,str_len,encoded_ac = data_list
            
            after_ac_str = decode(encoded_ac,alph_freq_list,str_len)

            after_bwt_str = BWT_MTF.decode(after_ac_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = itog2.Huffman()
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            uni_mtf_str = "".join(uni_mtf_list) + '$'
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(uni_mtf_str)
            encoded_ac = encode(uni_mtf_str)
            

            
            data_list.append(alph_freq_list)
            data_list.append(len(uni_mtf_str))
            data_list.append(encoded_ac)
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_list,write_f)

    def decode_file_bin(self,in_filename_format,out_filename_format):
        with open (in_filename_format,'rb') as read_f:
            data_list = pickle.load(read_f)
            BWT_index,MTF_alphabet,alph_freq_list,str_len,encoded_ac = data_list
            after_ac_str = decode(encoded_ac,alph_freq_list,str_len)
            after_bwt_str = BWT_MTF.decode(after_ac_str,BWT_index,MTF_alphabet)
            
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)

  
           
class BWT_MTF:
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        #BWT = itog_bwt.BWT()
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            #index,bwt_string = BWT.encode(read_f.read()+BWT_DELIM)
           # MTF = itog_mtf.MTF()
            HUFFMAN_CLASS = itog2.Huffman()
            
            # alph = []
            # alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(bwt_string)
            # for eleme in alph_freq_list:
            #     alph.append(eleme[0])
            
            # alph.reverse()
            # mtf_lst = MTF.encode(bwt_string,alph)
            
            # uni_mtf_list = []
            # for num in mtf_lst:
            #     uni_mtf_list.append(chr(num))
            uni_mtf_list, data_list = BWT_MTF.encode(read_f.read(),BWT_DELIM)
            
            
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq("".join(uni_mtf_list))
            encoded_huf,last_len = HUFFMAN_CLASS.encode("".join(uni_mtf_list),alph_freq_list)
            
            #data_list = [index,alph,last_len,HUFFMAN_CLASS.huffCodesDict ,encoded_huf]
            
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
            # MTF = itog_mtf.MTF()
            # after_mtf_str = MTF.decode(after_huf_str,MTF_alphabet)
            
            # BWT = itog_bwt.BWT()
            # after_bwt_str = BWT.decode(BWT_index,after_mtf_str)
            after_bwt_str = BWT_MTF.decode(after_huf_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = itog2.Huffman()
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
    
    @staticmethod
    def encode(in_str,BWT_DELIM):
        '''$ added auto. Returns unicode list and data list [BWT_index,MTF_alphabet]'''
        BWT = itog_bwt.BWT()
        index,bwt_string = BWT.encode(in_str+BWT_DELIM)
        MTF = itog_mtf.MTF()
        HUFFMAN_CLASS = itog2.Huffman()
        
        
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
        MTF = itog_mtf.MTF()
        after_mtf_str = MTF.decode(encoded_str,MTF_alphabet)
        
        BWT = itog_bwt.BWT()
        after_bwt_str = BWT.decode(BWT_index,after_mtf_str)
        return after_bwt_str


    @staticmethod
    def get_unique_symbol(in_str : str):
        for i in range(0,int('0x10ffff',16)):
            if chr(i) not in in_str:
                return chr(i)
    


class BWT_MTF_RLE_AC:
        
    def encode_file(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
            HUFFMAN_CLASS = itog2.Huffman()

            in_str = read_f.read()
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = itog_rle.RLE()   
            
            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
            
            
            
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM) + '$'
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            

            encoded_ac = encode(after_rle_str)

            
            
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
            
            after_ac_str = decode(encoded_ac,alph_freq_list,str_len)
           
            rle = itog_rle.RLE()
           
            decoded_rle_str =rle.decode(after_ac_str,RLE_DELIM)
            
            
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
            
            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write(after_bwt_str)
    
    
    def encode_file_bin(self,in_filename_format,out_filename_format,BWT_DELIM:str,RLE_DELIM:str,UNIQUE_DELIM = False):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str)
            HUFFMAN_CLASS = itog2.Huffman()
            
            if UNIQUE_DELIM:
                BWT_DELIM = BWT_MTF.get_unique_symbol(in_str)
            uni_mtf_list, data_list = BWT_MTF.encode(in_str,BWT_DELIM)
            
            rle = itog_rle.RLE()

            if UNIQUE_DELIM:
                RLE_DELIM = BWT_MTF.get_unique_symbol("".join(uni_mtf_list))
                
            after_rle_str = rle.encode("".join(uni_mtf_list),RLE_DELIM) + '$'
            alph_freq_list = HUFFMAN_CLASS.getSorted_alph_freq(after_rle_str)
            

            encoded_ac = encode(after_rle_str)

            
            
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
            
            after_ac_str = decode(encoded_ac,alph_freq_list,str_len)
            
            rle = itog_rle.RLE()
            decoded_rle_str =rle.decode(after_ac_str,RLE_DELIM)
            after_bwt_str = BWT_MTF.decode(decoded_rle_str,BWT_index,MTF_alphabet)
            
        
            ba = IMAGE_METHODS.str_to_byteArray(after_bwt_str)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)






def main_BWT_MTF_HA():
    
    #*
    # code_file = r"COMBINED\BWT+MTF\enwik7.txt"
    # com_file =r"COMBINED\BWT+MTF\outwik7_bmh.txt"
    # decom_file = r"COMBINED\BWT+MTF\enwik7_bmh_decoded.txt"


    # bmh = BWT_MTF_HA()
    # bmh.encode_file(code_file,com_file,'\x10')
    # bmh.decode_file(com_file,decom_file)


    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #         str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #         str2 = file2.read()
            
    # print(str1==str2)
    
    #*
    
    code_file = r"COMBINED\BWT+MTF\grey.raw"
    com_file =r"COMBINED\BWT+MTF\grey_bmh.txt"
    decom_file = r"COMBINED\BWT+MTF\grey_bmh_decoded.txt"


    bmh = BWT_MTF_HA()
    bmh.encode_file_bin(code_file,com_file,'ы')
    bmh.decode_file_bin(com_file,decom_file)


    with open(code_file, 'rb') as read_f:
        str1 = read_f.read()
    with open(decom_file,'rb') as read2_f:
        str2 = read2_f.read()
            
    print(str1==str2)



def main_BWT_MTF_RLE_HA():
    # code_file = r"COMBINED\BWT+MTF\enwik7.txt"
    # com_file =r"COMBINED\BWT+MTF\enwik7_bmrleh.txt"
    # decom_file = r"COMBINED\BWT+MTF\enwik7_bmrleh_decoded.txt"


    # bmrh = BWT_MTF_RLE_HA()
    # bmrh.encode_file(code_file,com_file,'№','\xFF',UNIQUE_DELIM=True)
    # bmrh.decode_file(com_file,decom_file)


    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #         str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #         str2 = file2.read()
            
    # print(str1==str2)

    
    code_file = r"COMBINED\BWT+MTF\rgb.raw"
    com_file =r"COMBINED\BWT+MTF\rgb_bmh.txt"
    decom_file = r"COMBINED\BWT+MTF\rgb_bmh_decoded.txt"


    bmh = BWT_MTF_RLE_HA()
    bmh.encode_file_bin(code_file,com_file,'ы','s',UNIQUE_DELIM=True)
    bmh.decode_file_bin(com_file,decom_file)


    with open(code_file, 'rb') as read_f:
        str1 = read_f.read()
    with open(decom_file,'rb') as read2_f:
        str2 = read2_f.read()
            
    print(str1==str2)
    

def main_BWT_MTF_AC():
    
    #*
    # code_file = r"COMBINED\BWT+MTF\war_and_peace.ru.txt"
    # com_file =r"COMBINED\BWT+MTF\war_coded_bmAC.txt"
    # decom_file = r"COMBINED\BWT+MTF\war_bmAC_decoded.txt"


    # bmh = BWT_MTF_AC()
    # bmh.encode_file(code_file,com_file,'\x10')
    # bmh.decode_file(com_file,decom_file)


    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #         str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #         str2 = file2.read()
            
    # print(str1==str2)
    
    #*
    
    code_file = r"COMBINED\BWT+MTF\grey.raw"
    com_file =r"COMBINED\BWT+MTF\grey_bmAC.txt"
    decom_file = r"COMBINED\BWT+MTF\grey_bmAC_decoded.txt"


    bmac = BWT_MTF_AC()
    bmac.encode_file_bin(code_file,com_file,'ы')
    bmac.decode_file_bin(com_file,decom_file)


    with open(code_file, 'rb') as read_f:
        str1 = read_f.read()
    with open(decom_file,'rb') as read2_f:
        str2 = read2_f.read()
            
    print(str1==str2)


def main_BWT_MTF_RLE_AC():
    # code_file = r"COMBINED\BWT+MTF\war_and_peace.ru.txt"
    # com_file =r"COMBINED\BWT+MTF\war_bmrleAC.txt"
    # decom_file = r"COMBINED\BWT+MTF\war_bmrleAC_decoded.txt"


    # bmrh = BWT_MTF_RLE_AC()
    # bmrh.encode_file(code_file,com_file,'№','\xFF',UNIQUE_DELIM=True)
    # bmrh.decode_file(com_file,decom_file)


    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #         str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #         str2 = file2.read()
            
    # print(str1==str2)

    code_file = r"COMBINED\BWT+MTF\grey.raw"
    com_file =r"COMBINED\BWT+MTF\grey_bmrAC.txt"
    decom_file = r"COMBINED\BWT+MTF\grey_bmAC_decoded.txt"


    bmh = BWT_MTF_RLE_AC()
    bmh.encode_file_bin(code_file,com_file,'ы','s',UNIQUE_DELIM=True)
    bmh.decode_file_bin(com_file,decom_file)


    with open(code_file, 'rb') as read_f:
        str1 = read_f.read()
    with open(decom_file,'rb') as read2_f:
        str2 = read2_f.read()
            
    print(str1==str2)
    
    
    
    
    

if __name__ == '__main__':
    main_BWT_MTF_RLE_AC()