import pickle
import sufarray
import itog_rle
import os

class BWT:
    """ BWT + RLE to measure N"""
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
            
            rle = itog_rle.RLE()
            delim_rle = '\x18'  #* DELIMITTER FOR RLE
            data_lst = [DELIM,index,rle.encode(encoded_str,delim_rle),delim_rle]
            
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return
    
    def decode_file(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            BWT_delim,index,encoded_str,delim_rle = data_lst
            
            rle = itog_rle.RLE()
            decoded_rle_str = rle.decode(encoded_str,delim_rle)
        
            decoded_str = self.decode(index,decoded_rle_str)

            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write("".join(decoded_str))
                
    def encode_file_bin(self, in_filename_format, out_filename_format,DELIM = '$',RLE_DELIM = '\x18'):
        ''' Encode function. Automaticly adds DELIM to end of file
        '''
        with open(in_filename_format,'rb') as read_f:
            
            bin_str = read_f.read()# + DELIM

            in_lst = []
            
            for byte in bin_str:
                in_lst.append(chr(byte))    

            in_str = "".join(in_lst) + DELIM
            index, encoded_str = self.encode(in_str)
            
            rle = itog_rle.RLE()
            delim_rle = RLE_DELIM  #* DELIMITTER FOR RLE
            data_lst = [DELIM,index,rle.encode(encoded_str,delim_rle),delim_rle]
            
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return
    def decode_file_bin(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            BWT_delim,index,encoded_str,delim_rle = data_lst
            
            rle = itog_rle.RLE()
            decoded_rle_str = rle.decode(encoded_str,delim_rle)
        
            decoded_str = self.decode(index,decoded_rle_str)
            decoded_bin_lst = bytearray()
            for char in decoded_str:
                decoded_bin_lst.append(ord(char))
                
            with open(out_filename_format,'wb') as write_f:
                write_f.write(decoded_bin_lst)
def main():
    bwt = BWT()

    code_file = r"COMBINED\BWT+RLE\wb.raw"
    com_file =r"COMBINED\BWT+RLE\wb.txt"
    decom_file = r'COMBINED\BWT+RLE\wb_decoded.txt'

    #bwt.encode_file(code_file,com_file,DELIM= '\x10')
    #bwt.decode_file(com_file, decom_file)
    

    # with open(code_file, 'r',encoding='utf-8',newline='\x0A') as read_f:
    #     str1 = read_f.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as read2_f:
    #     str2 = read2_f.read()
   
   
    bwt.encode_file_bin(code_file,com_file,DELIM='$',RLE_DELIM='^')
    bwt.decode_file_bin(com_file,decom_file)
   
    with open(code_file, 'rb') as read_f:
        str1 = read_f.read()
    with open(decom_file,'rb') as read2_f:
        str2 = read2_f.read()
   
    
    print(str1==str2)



if __name__ == '__main__':
    main()