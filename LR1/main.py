# Определение класса для хранения триплета (сдвиг, длина, следующий символ)
class Triplet:
    def __init__(self, prev, length, next_char):
        self.prev = prev
        self.length = length
        self.next_char = next_char

# Определение класса для хранения одиночного символа, когда нет повторений
class TripletOneSymbol:
    def __init__(self, next_char):
        self.next_char = next_char


# Функция кодирования строки алгоритмом LZ77
def lz77_coder(string, buffer_size):
    triplet_list = [] # Список для хранения результатов кодирования
    pos = 0 # Текущая позиция в строке

    while pos < len(string):
        # Определение буфера поиска
        buffer = string[max(pos - buffer_size, 0):pos]
        index_substr_buffer = len(buffer)
        length_substring = 0 # Длина найденной подстроки

        # Поиск самой длинной повторяющейся подстроки в буфере
        for i in range(1, len(buffer) + 1):
            if buffer.rfind(string[pos:pos + i]) != -1:
                index_substr_buffer = buffer.rfind(string[pos:pos + i])
                length_substring = i
            else:
                break

        prev_symbols_triplet = len(buffer) - index_substr_buffer
        length_triplet = length_substring

        # Проверка на повторяющиеся символы после найденной подстроки
        pos_repeat = pos
        length_substring_repeat = length_substring
        if length_substring != 0:
            while pos_repeat + length_substring < len(string) and string[pos_repeat] == string[pos_repeat + length_substring]:
                pos_repeat += 1
                length_substring_repeat += 1

            if pos_repeat - pos > 1:
                pos = pos_repeat
                length_triplet = length_substring_repeat

        # Определение следующего символа после подстроки
        next_symbol_triplet = string[pos + length_substring] if pos + length_substring < len(string) else ''
        pos += length_substring + 1

        # Добавление триплета в список
        if prev_symbols_triplet == 0 and length_triplet == 0:
            triplet_list.append(TripletOneSymbol(next_symbol_triplet))
        else:
            triplet_list.append(Triplet(prev_symbols_triplet, length_triplet, next_symbol_triplet))

    return triplet_list

# Функция декодирования списка триплетов обратно в строку
def lz77_decoder(triplet_list):
    result_string = ""
    for triplet in triplet_list:
        if isinstance(triplet, TripletOneSymbol):
            result_string += triplet.next_char
        else:
            # Восстановление повторяющейся подстроки из триплета
            if triplet.prev != 0:
                full_buffer = triplet.length // triplet.prev
                for _ in range(full_buffer):
                    result_string += result_string[-triplet.prev:]
                result_string += result_string[-triplet.prev: -triplet.prev + (triplet.length % triplet.prev)]
            result_string += triplet.next_char
    return result_string

# Функция чтения текста из файла
def read_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8',newline='\x0A') as file:
        return file.read()


# Функция записи данных в файл
def write_to_file(file_path, data, is_triplets=False):
    with open(file_path, 'w', encoding='utf-8',newline='\x0A') as file:
        if is_triplets:
            for triplet in data:
                if isinstance(triplet, TripletOneSymbol):
                    file.write(f"({triplet.next_char})\n")
                else:
                    file.write(f"({triplet.prev},{triplet.length},{triplet.next_char})\n")
        else:
            file.write(data)

def main():
    input_file_path = 'enwik7.txt'  # Путь к входному файлу с исходным текстом
    encoded_file_path = 'encoded.txt'  # Путь к файлу, куда будет сохранён сжатый текст
    decoded_file_path = 'decoded.txt'  # Путь к файлу, куда будет сохранён декодированный текст

    # Чтение текста из файла
    data = read_from_file(input_file_path)

    # Кодирование текста
    triplet_list = lz77_coder(data, buffer_size=32768)
    # Сохранение сжатых данных в файл
    write_to_file(encoded_file_path, triplet_list, is_triplets=True)

    # Декодирование сжатых данных обратно в текст
    decoded_data = lz77_decoder(triplet_list)
    # Сохранение декодированного текста в файл
    write_to_file(decoded_file_path, decoded_data)

    print(f"Исходный текст сохранён в {input_file_path}")
    print(f"Сжатый текст сохранён в {encoded_file_path}")
    print(f"Декодированный текст сохранён в {decoded_file_path}")
    
    with open(input_file_path,'r',encoding='utf-8',newline='\x0A') as read_f:
        str1 = read_f.read()
    
    with open(decoded_file_path,'r',encoding='utf-8',newline='\x0A') as read_f2:
        str2 = read_f2.read()

    print(str1 == str2)

if __name__ == "__main__":
    main()