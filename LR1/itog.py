import os
from queue import PriorityQueue
from bitarray import bitarray

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
    
    def encode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format,encoding='utf-8') as read_f:
            with open(out_filename_format,'w', encoding='utf-8')as write_f:
                
                in_str = read_f.read()
                alph_freq_list = self.getSorted_alph_freq(in_str)

            
                
                chr_str,last_len = self.encode(in_str,alph_freq_list)
                
                #!writing metadata
                #write_f.write(str(len(alph_freq_list))+'\n') #! writing number of unique symbols + \n
                
                #* writing symbol and its code (symbolcode\n)
                #alph_freq_list.reverse()
                
                #for symbol_ind in range(len(self.huffCodesList)):
                #    write_f.write(alph_freq_list[symbol_ind][0]+ str(alph_freq_list[symbol_ind][1])+'\n')
                #& writing encoded_str as sequence of chars, representing bits
                write_f.write(chr_str)
                
                
               
        at = self.decode(chr_str,alph_freq_list,last_len)
        with open(out_filename_format,'r', encoding='utf-8')as write_f:
            ab_str = write_f.read()
            ab = self.decode(ab_str,alph_freq_list,last_len)
            return ab
    

    def encode(self, in_str,alph_freq_list : list): 
        node = self.build_huff_tree(alph_freq_list)
        self.get_huff_codes(node)
        self.sort_huff_code()
        self.toCanonicalHuffCodes()

        for chr_ind in range(len(self.huffCodesList)):
            self.huffCodesDict[self.huffCodesList[chr_ind][0]] = bitarray(self.huffCodesList[chr_ind][1])
        
        encoded = bitarray()
        bitarray.encode(encoded,self.huffCodesDict,in_str)
        
        encoded_str,last_len = self.bit_str_to_chars(encoded.to01())
        
        return encoded_str,last_len    
      
    
    def encodev2(self, in_str,alph_freq_list : list): 
        node = self.build_huff_tree(alph_freq_list)
        self.get_huff_codes(node)
        self.sort_huff_code()
        self.toCanonicalHuffCodes()

        for chr_ind in range(len(self.huffCodesList)):
            self.huffCodesDict[self.huffCodesList[chr_ind][0]] = bitarray(self.huffCodesList[chr_ind][1])
        
        encoded = bitarray()
        bitarray.encode(encoded,self.huffCodesDict,in_str)
        
        encoded_str,last_len = self.bit_str_to_chars(encoded.to01())
        
        return encoded_str,last_len    
    
    def encode_file_test(self,in_filename_format,out_filename_format):
        with open(in_filename_format,encoding='utf-8') as read_f:
            with open(out_filename_format,'w', encoding='utf-8',newline='\x0A')as write_f:
                
                in_str = (read_f.read()).replace("\0A","\x0D\x0A")
                alph_freq_list = self.getSorted_alph_freq(in_str)

                chr_str,last_len = self.encodev2(in_str,alph_freq_list)
                #dec = bitarray(chr_str).decode(self.huffCodesDict)
                #write_f.write("".join(dec).replace('\x0D\x0A','\x0A'))
                
                
                write_f.write(str(len(alph_freq_list))+'\n') #! writing number of unique symbols + \n
                alph_freq_list.reverse()
                
                for symbol_ind in range(len(self.huffCodesList)):
                    write_f.write(alph_freq_list[symbol_ind][0]+ str(alph_freq_list[symbol_ind][1])+'\n')
                
                with open('abcd.bin','wb')as write_f2:
                    write_f2.write(chr_str)
                    
                with open('abcd.txt','rb')as read_f2:
                    b = read_f2.read()
                
                
                
                
                alph_freq_list.reverse()
                self.decode2(chr_str,alph_freq_list,last_len)
                
                
                bit_lst = []
                for symbol_ind in range(len(b)):
                    symbol = b[symbol_ind]
                    bit_symbol = bin(ord(b[symbol_ind]))[2:]
                    if symbol_ind == len(b)-1:
                        
                        bit_symbol = bit_symbol.zfill(last_len)
                    else:
                        bit_symbol = bit_symbol.zfill(8)
                    bit_lst.append(bit_symbol)
                
                encoded_bit_str = "".join(bit_lst)
                decoded_bit_str = bitarray(encoded_bit_str)
                decoded_list = decoded_bit_str.decode(self.huffCodesDict)
                decoded_str = "".join(decoded_list)
                return decoded_str
                     
                #^dec = self.decode(chr_str,alph_freq_list)
                #^write_f.write(dec.replace('\x0D\x0A','\x0A'))
                
    def encode_test(self,in_str,alph_freq_list):
        node = self.build_huff_tree(alph_freq_list)
        self.get_huff_codes(node)
        self.sort_huff_code()
        self.toCanonicalHuffCodes()

        for chr_ind in range(len(self.huffCodesList)):
            self.huffCodesDict[self.huffCodesList[chr_ind][0]] = bitarray(self.huffCodesList[chr_ind][1])

        encoded = bitarray()
        bitarray.encode(encoded,self.huffCodesDict,in_str)
        
        encoded_str,last_len = self.bit_str_to_chars(encoded.to01())

        # bit_lst = []
        # for symbol_ind in range(len(encoded_str)):
        #     bit_symbol = bin(ord(encoded_str[symbol_ind]))[2:]
            
        #     if symbol_ind == len(encoded_str)-1:
        #         bit_symbol = bit_symbol.zfill(last_len)
        #     else:
        #         bit_symbol = bit_symbol.zfill(8)
            
        #     # if symbol_ind != len(encoded_str)-1:
        #     #     bit_symbol = bit_symbol.zfill(8)
                
        #     bit_lst.append(bit_symbol)
            
        # decoded_data = "".join(bit_lst)
        
        # ab = bitarray(decoded_data)
        # ak = ab.decode(self.huffCodesDict)
        
        # at = "".join(ak)
        
        
        self.decode(encoded_str,alph_freq_list,last_len)
        
        
        #return at
        return
    
    
    
    
    
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
        dec = bitarray(bit_str)
        some = dec.decode(self.huffCodesDict)     
        com = "".join(some)
        return com

    def bit_str_to_bytes(self,bit_str):
        out_lst =[]
        last_len = 0
        for i in range(0,len(bit_str),8):
            slice = bit_str[i:i+8]
            if len(slice) < 8:
                last_len = len(slice)
            out_lst.append(bytes(int(bit_str[i:i+8],2)))
        str =  "".join(out_lst)
        
        return str,last_len
        
    def sort_huff_code(self):
        self.huffCodesList.sort(key = lambda x:[[len(x[1]),x[0]]])


    def decode_file(self,in_filename_format,out_filename_format):
        with open(in_filename_format,'r',encoding='utf-8',newline='\x0D\x0A') as read_f:
            alph_amount = int(read_f.readline()[:-1])
            alph_freq_list = []
            for i in range(alph_amount):
                temp_str = read_f.readline()
                if temp_str == '\n' or temp_str =='\r\n' or temp_str == '\x0D':
                    temp_str+= read_f.readline()
                alph_freq_list.append((temp_str[0],int(temp_str[1:-1])))
            encoded_data = read_f.read()
        alph_freq_list.reverse()
            
        decoded_data = self.decode(encoded_data,alph_freq_list)
        with open(out_filename_format,'w',encoding='utf-8',newline='\x0A') as write_f:
            write_f.write(decoded_data)

    @staticmethod
    def decode(encoded_data: str,alph_freq_list: list,last_len = 7) -> str:
        decode_hf = Huffman()


        node = decode_hf.build_huff_tree(alph_freq_list)
        decode_hf.get_huff_codes(node,"")
        decode_hf.sort_huff_code()
        decode_hf.toCanonicalHuffCodes()
        
        
        for chr_ind in range(len(decode_hf.huffCodesList)):
            decode_hf.huffCodesDict[decode_hf.huffCodesList[chr_ind][0]] = bitarray(decode_hf.huffCodesList[chr_ind][1])
  
        encoded_data.replace('\r','\n')
  
        bit_lst = []
        for symbol_ind in range(len(encoded_data)):
            symbol = encoded_data[symbol_ind]
            bit_symbol = bin(ord(encoded_data[symbol_ind]))[2:]
            if symbol_ind == len(encoded_data)-1:
                
                bit_symbol = bit_symbol.zfill(last_len)
            else:
                bit_symbol = bit_symbol.zfill(8)
            bit_lst.append(bit_symbol)
        
        encoded_bit_str = "".join(bit_lst)
        decoded_bit_str = bitarray(encoded_bit_str)
        decoded_list = decoded_bit_str.decode(decode_hf.huffCodesDict)
        decoded_str = "".join(decoded_list)
        
        return decoded_str
    
    
    
    def decode2(self,encoded_data: str,alph_freq_list: list,last_len = 7) -> str:
        with open('abcd.txt','r',encoding='utf-8',newline='\x0D\x0A')as read_f2:
            b = read_f2.read()
            
        
        b.replace('\r','\n')
        
        bit_lst = []
        for symbol_ind in range(len(encoded_data)):
            symbol = encoded_data[symbol_ind]
            bit_symbol = bin(ord(encoded_data[symbol_ind]))[2:]
            if symbol_ind == len(encoded_data)-1:
                
                bit_symbol = bit_symbol.zfill(last_len)
            else:
                bit_symbol = bit_symbol.zfill(8)
            bit_lst.append(bit_symbol)
        
        encoded_bit_str = "".join(bit_lst)
        decoded_bit_str = bitarray(encoded_bit_str)
        decoded_list = decoded_bit_str.decode(self.huffCodesDict)
        decoded_str = "".join(decoded_list)
        
        bit_lst = []
        for symbol_ind in range(len(b)):
            symbol = b[symbol_ind]
            bit_symbol = bin(ord(b[symbol_ind]))[2:]
            if symbol_ind == len(b)-1:
                
                bit_symbol = bit_symbol.zfill(last_len)
            else:
                bit_symbol = bit_symbol.zfill(8)
            bit_lst.append(bit_symbol)
        
        encoded_bit_str = "".join(bit_lst)
        decoded_bit_str = bitarray(encoded_bit_str)
        decoded_list = decoded_bit_str.decode(self.huffCodesDict)
        decoded_str = "".join(decoded_list)
        
        
        
        return decoded_str

        
hf = Huffman()
hf.encode_file("war_and_peace.test.txt","war_and_com.txt")
#hf.encode_file("enwik7.txt","enwik7_huf.txt")
#hf.decode_file("war_and_com.txt","war_dec.txt")

#hf.encode_file_test("war_and_peace.test.txt","test.txt")
#hf.decode_file('test.txt','test.dec')

print("abc"[:1])


from queue import PriorityQueue


class Node:
    def __init__(self, char, f):
        self.char = char
        self.freq = f
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.huffmanCodes: dict[str, str] = {}

    def encode(self, input_path, output_path):
        with open(input_path, "r", encoding="utf-8") as file_read:
            data: str = file_read.read()

            frequency: dict[str, int] = self.getFrequency(data)
            node: Node = self.getHuffmanTree(frequency)
            blank = str()
            self.getHuffmanCodes(node,str())

            with open(output_path, "wb") as file_write:
                encode_data = ""
                for char in data:
                   encode_data += self.huffmanCodes[char]
                num = int(encode_data, 2)
                #test = num.to_bytes((num.bit_length() + 7) // 8, byteorder="big")
                file_write.write(num.to_bytes((num.bit_length() + 7) // 8, byteorder="big"))
    # Возможные проблемы - из-за переполнения int может неправильно кодироваться, лучше разделить на части

    def decode(self, code_data: str) -> str:
        huffmanReverseCodes: dict[str, str] = {self.huffmanCodes[i]: i for i in self.huffmanCodes.keys()}
        original_text = ""
        code_part = ""
        for code in code_data:
            code_part += code
            if code_part in huffmanReverseCodes:
                original_text += huffmanReverseCodes[code_part]
                code_part = ""
        return original_text

    @staticmethod
    def getFrequency(data: str) -> dict[str, int]:
        frequency: dict[str, int] = {}

        for char in data:
            if char not in frequency:
                frequency[char] = data.count(char)

        return frequency

    @staticmethod
    def getHuffmanTree(frequency: dict[str, int]) -> Node:
        q = PriorityQueue()
        for char in frequency.keys():
            node = Node(char, frequency[char])
            q.put(node)

        while q.qsize() > 1:
            node1 = q.get()
            node2 = q.get()
            node = Node(node1.char + node2.char, node1.freq + node2.freq)
            node.left = node1
            node.right = node2

            q.put(node)

        node = q.get()

        return node

    def getHuffmanCodes(self, node: Node, code: str):
        if node is None:
            return

        if (node.left is None) and (node.right is None):
            self.huffmanCodes[node.char] = code

        self.getHuffmanCodes(node.left, code + "0")
        self.getHuffmanCodes(node.right, code + "1")
        


#hf = HuffmanCoding()
#hf.encode("enwik7.txt","outwik7.txt")


from string import ascii_lowercase
class AC:
    def encode(self,str, probs, alphabet = ascii_lowercase):
        intervals = [sum(probs[:i]) for i in range (len(probs)+1)]
        left_b = 0
        right_b = 1
        
        
        for c in str:
            lenght = right_b - left_b
            left_b,right_b = left_b+ intervals[alphabet.index(c)]*lenght,left_b + intervals[alphabet.index(c)+1]*lenght
            if left_b == right_b:
                break
        return (right_b+left_b)/2
    
    def encode_data_AC(self,in_filename_format,out_filename_format,N):
    
        in_file = open(in_filename_format, 'r', encoding = 'utf8',newline='')
        out_file = open(out_filename_format, 'w', encoding = 'utf8',newline='')
        Lenght = os.path.getsize(in_filename_format)
        
        
        out_file.write(str(N) + '\n') #!
        
        list_num = list() #!
        it = 0
        while it < Lenght -N:
            str1 = in_file.read(N)
            if str1 != '':
                alph,probs = self.get_probs_and_alph(str1)
                list_num.append(self.encode(str1,probs,alph)) #!
                #num = self.encode(str1,probs,alph)
                
                #out_file.write(str(num)+' ')
                out_file.write(self.write_alph_and_probs(alph,probs)) #!
            it+= N
        
        if Lenght-it > 0:
            str1 = in_file.read(N)
            if str1 != '':
                alph,probs = self.get_probs_and_alph(str1)
                #num = self.encode(str1,probs,alph)
                list_num.append(self.encode(str1,probs,alph)) #!
                #out_file.write(str(num)+' ')
                out_file.write(self.write_alph_and_probs(alph,probs)) #!
        
        out_file.write(str(list_num[0])) #!
        for k in range(1,len(list_num)): #!
            out_file.write(' '+str(list_num[k])) #!
        
        in_file.close()
        out_file.close()
    
    
    
    def encode_data_AC2(self,in_filename_format,out_filename_format,N = 5):
        in_file = open(in_filename_format, 'r', encoding = 'utf8')
        out_file = open(out_filename_format, 'w', encoding = 'utf-8')
        
        in_str = in_file.read()
        alph,probs = self.get_probs_and_alph(in_str)
        Lenght = os.path.getsize(in_filename_format)
        it = 0
        while it < Lenght -N:
            if in_str[it:it+N] != '':
                some = self.encode(in_str[it:it+N],probs,alph)
                out_file.write(str(some)+' ')
            it+=N
        if Lenght-it > 0:
            if in_str[it:it+N] != '':
                out_file.write(str(self.encode(in_str[it:it+N],probs,alph)))
        
        in_file.close()
        out_file.close()
        
    def get_probs_and_alph(self,in_str):
        alhpabet = ''
        probs = []
        set_alphabet = sorted(set(in_str))

        for symbol in set_alphabet:
            alhpabet+=str(symbol)
            curr_amount = in_str.count(symbol)
            probs.append(curr_amount/len(in_str))
        return alhpabet, probs
    
    def write_alph_and_probs(self,alph,probs:list):
        out_str = alph
        for k in probs:
            out_str += ' ' + str(int(k*100))
        return out_str + '\n'
    
#ac = AC()
#ac.encode_data_AC2("war_and_peace.ru.txt","wap_ac2.txt",40)