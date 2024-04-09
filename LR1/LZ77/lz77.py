import os
import sys
def compress(str):
        dictionary =1024
        size = len(str)
        str_compress = []
        memory = []
        char_coded = 0
        type = 0
        i=0
        while i<size:
            if (i%10000==0):
                #print(i)
                pass
            dictionary_start = 0
            dictionary_leng = 0
            for j in range(max(0, i - dictionary), i):
                if str[j] == str[i]:  # есть вхождение
                    start = j
                    tmp = j + 1
                    length = 1
                    while (i + length) < size and str[tmp] == str[i + length]:
                        tmp += 1
                        length += 1
                    if dictionary_leng < length:
                        dictionary_start = i - start
                        dictionary_leng = length

            type = (type << 1)
            if dictionary_leng > 1:  # запись из словаря
                memory.append(chr(dictionary_start))
                memory.append(chr(dictionary_leng))
                type += 1
                i += dictionary_leng - 1
            else:  # обычная запись
                memory.append(str[i])
            char_coded += 1

            if char_coded == 8:
                str_compress.append(chr(type))  # запишим типы кодов
                char_coded = 0
                type = 0
                str_compress.extend(memory)
                memory = []
            i+=1

        if char_coded != 0:
            type = (type << (8 - char_coded))  # чтобы при дешифрации не было особого случая
            str_compress.append(chr(type))  # запишим типы кодов
            str_compress.extend(memory)

        return ''.join(str_compress)

def deCompress( str):
        dictionary = 1024
        str_out = []
        size = len(str)
        str_end = False
        j = 0
        while not str_end and j < size:
            types = ord(str[j])
            j += 1
            for i in range(7, -1, -1):
                if j<size:
                    if (types & (2 ** i)) == 0:  # обычный символ
                        str_out.append(str[j])
                        j += 1
                    else:
                        start = ord(str[j])
                        j += 1
                        length = ord(str[j])
                        k=0
                        for k in range(length):
                            str_out.append(str_out[len(str_out)-start])
                        j += 1
                else:
                    break
        return ''.join(str_out)
    
    

# file_r=open("enwik7.txt", "r",encoding="utf-8")
# input_stream=file_r.read()


# file_w=open("LZ77.txt", "w",encoding="utf-8")
# result = compress(input_stream)
# file_w.write(result)
# print("result")
# print(os.path.getsize("LZ77.txt"))

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
           
#!!BINIRY


file_r = open("grey.raw",'rb') 
bin_str =file_r.read()
in_str = IMAGE_METHODS.img_to_str(bin_str)
result = compress(in_str)
file_w=open("grey LZ77.txt", "w",encoding="utf-8")
file_w.write(result)
