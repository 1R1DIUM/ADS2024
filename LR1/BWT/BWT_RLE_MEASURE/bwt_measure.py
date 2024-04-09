import pickle
import sufarray
import itog_rle
import os

class BWT_mes:
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
    
    def encode_file(self, in_filename_format, out_filename_format,N = 0,DELIM = '$'):
        ''' Encode function. Automaticly adds DELIM to end of file
        '''
        with open(in_filename_format,'r',encoding='utf-8') as read_f:
            in_str = read_f.read()
            index_lst = []
            end_lst = []
            for i in range(0,len(in_str)+N,N):
                encode_slice = in_str[i:i+N]+DELIM
                if encode_slice != DELIM:
                    index, encoded_str = self.encode(encode_slice)
                    index_lst.append(index)
                    end_lst.append(encoded_str)
                else:
                    break
            
            rle = itog_rle.RLE()
            delim_rle = '\x18'  #* DELIMITTER FOR RLE
            data_lst = [DELIM,N,index_lst,rle.encode("".join(end_lst),delim_rle),delim_rle]
            
            
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')
        return
    
    def decode_file(self, in_filename_format, out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            data_lst = pickle.load(read_f)
            BWT_delim,N,index_lst,encoded_str,delim_rle = data_lst
            
            rle = itog_rle.RLE()
            decoded_rle_str = rle.decode(encoded_str,delim_rle)
            
            decode_lst = []
            it = 0
            for i in range(0,len(decoded_rle_str)+N+1,N+1): #! N+1 т.к. добавлен доллар
                decoded_slice = decoded_rle_str[i:i+N+1]
                
                if decoded_slice == '':
                    break
                #     decode_lst.append(self.decode(index_lst[it],decoded_slice))
                #     it+=1
                decode_lst.append(self.decode(index_lst[it],decoded_slice))
                it+=1

            with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
                write_f.write("".join(decode_lst))
                


def main():
    BWT = BWT_mes()


    power = 100000
    code_file = "enwik7.txt"
    com_file ="enwik7_coded20_" + str(power) + '.txt'
    decom_file = 'enwik7_decoded.txt'

    size = 50*power
    BWT.encode_file(code_file,com_file,N= int(size), DELIM= '\x07')
    BWT.decode_file(com_file, decom_file)



    with open(code_file, 'r',encoding='utf-8',newline='\x0A') as read_f:
        str1 = read_f.read()
    with open(decom_file,'r',encoding='utf-8',newline='\x0A') as read2_f:
        str2 = read2_f.read()
    
    print(str1==str2)
if __name__ == '__main__':
    main()

