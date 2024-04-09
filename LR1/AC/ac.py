
import pickle
from bitarray import bitarray
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





def float_to_binary(num):
    # Check if the float is negative
    if num < 0:
        sign = '-'
        num = abs(num)
    else:
        sign = ''
    # Split the float into integer and fractional parts
    integer_part = int(num)
    fractional_part = num - integer_part
    # Convert the integer part to binary
    binary_integer = bin(integer_part)[2:]
    # Convert the fractional part to binary
    binary_fractional = ''
    while fractional_part > 0:
        # Multiply the fractional part by 2 and check if it's greater than 1
        fractional_part *= 2
        if fractional_part >= 1:
            binary_fractional += '1'
            fractional_part -= 1
        else:
            binary_fractional += '0'
    # Combine the binary integer and fractional parts
    binary = binary_integer + '.' + binary_fractional
    # Add the sign to the binary representation
    binary = sign + binary
    return binary

def getSorted_alph_freq(in_str :str):
        afList = []
        set_alphabet = sorted(set(in_str))
        for symbol in set_alphabet:
            curr_amount = in_str.count(symbol)
            afList.append((symbol,curr_amount))
        return sorted(afList, key= lambda x:[(x[1],x[0])])

def encode(in_str) ->bytearray:

    alphabet_list = []
    cum_sum = 0
    cum_list = [0]
    TOTAL_CUM = 0

    alph_freq_lst= getSorted_alph_freq(in_str)


        #!total cumulitive frequency
    for i in range(len(alph_freq_lst)):
        cum_sum+=alph_freq_lst[i][1]
        #intervals.append(cum_sum)
        alphabet_list.append(alph_freq_lst[i][0])
        TOTAL_CUM += alph_freq_lst[i][1]
        cum_list.append(cum_sum)

    alph_indexes = [i for i in range(len(alph_freq_lst))]
    alphabet_dict = dict(zip(alphabet_list,alph_indexes))

    max_len = math.log2(TOTAL_CUM)
    if max_len.is_integer():
        max_len+=1
    bitlen = math.ceil(max_len)
    max_len= 2**bitlen



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

def decode(bytes, alph_freq_lst : list,len_str:int) -> str:

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

    max_len = math.log2(TOTAL_CUM)
    if max_len.is_integer():
        max_len+=1
    bitlen = math.ceil(max_len)
    max_len= 2**bitlen


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


        while left >= max_len/2 or right <= max_len/2 or (
            max_len/4 <= left < max_len/2 < right <= 3*max_len/4):

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



def encode_file(in_filename_format,out_filename_format):
    with open(in_filename_format,'r',encoding='utf-8',newline='\x0A') as read_f:
        in_str = read_f.read() + '$'
        alph_freq = getSorted_alph_freq(in_str)
        encoded_msg = encode(in_str)
        len_str = len(in_str)

        data_lst = [alph_freq,encoded_msg,len_str]
        with open(out_filename_format,'wb') as write_f:
            pickle.dump(data_lst,write_f)
            write_f.write(b'\n')


def decode_file(in_filename_format,out_filename_format):
    with open(in_filename_format,'rb') as read_f:
        data_lst = pickle.load(read_f)
        alph_freq,encoded_msg,len_str = data_lst

        decoded_msg = decode(encoded_msg,alph_freq,len_str)

        with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
            write_f.write(decoded_msg)


def encode_file_bin(in_filename_format,out_filename_format):
        with open(in_filename_format,'rb') as read_f:
            bin_str = read_f.read()
            in_str = IMAGE_METHODS.img_to_str(bin_str) + '$'

            alph_freq = getSorted_alph_freq(in_str)
            encoded_msg = encode(in_str)
            len_str = len(in_str)

            data_lst = [alph_freq,encoded_msg,len_str]
            with open(out_filename_format,'wb') as write_f:
                pickle.dump(data_lst,write_f)
                write_f.write(b'\n')


def decode_file_bin(in_filename_format,out_filename_format):
        with open(in_filename_format, 'rb') as read_f:
            data_lst = pickle.load(read_f)
            alph_freq,encoded_msg,len_str = data_lst

            decoded_msg = decode(encoded_msg,alph_freq,len_str)

            ba = IMAGE_METHODS.str_to_byteArray(decoded_msg)
            with open(out_filename_format,'wb') as write_f:
                write_f.write(ba)


if __name__ == '__main__':

    code_file = 'wb LZ77.txt'
    com_file = "wb LZ77AC_com.txt"
    decom_file = "wb LZ77AC_decom.txt"

    encode_file(code_file,com_file)
    #decode_file(com_file,decom_file)


    # with open(code_file,'r',encoding='utf-8',newline='\x0A') as file1:
    #     str1 = file1.read()
    # with open(decom_file,'r',encoding='utf-8',newline='\x0A') as file2:
    #     str2 = file2.read()

    # print(str1==str2)
    
    # code_file = 'grey.raw'
    # com_file = "grey_AC_com.txt"
    # decom_file = "grey_AC_decom.raw"

    # encode_file_bin(code_file,com_file)
    # decode_file_bin(com_file,decom_file)


    # with open(code_file, 'rb') as read_f:
    #     str1 = read_f.read()
    # with open(decom_file,'rb') as read2_f:
    #     str2 = read2_f.read()

    # print(str1==str2)
    
    

#encode('1321')

