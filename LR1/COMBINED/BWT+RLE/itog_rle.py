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
    
# Rle = RLE()
# str = "abaaaaakan"*500000 + "b"*255000 + 'Cab'*9000000
# abc = Rle.encode(str)
# print(abc)
# cba = Rle.decode(abc, DELIM=  '^')
# print(cba)
# print(cba == str)