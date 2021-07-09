import os
from progressbar import ProgressBar
class Decompressor:
    def __init__(self,compressor):
        print('Welcome top decompressor')
        self.compressor = compressor

    def decompress(self):
        print('input bin file to decompress')
        input_path = input()
        filename, file_extension = os.path.splitext(self.compressor.path)
        output_path = filename + '_decompressed' + '.txt'
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string = self.__bitString(file)
            actual_bit_string = self.__removePadding(bit_string)

            actual_string = self.__convert_actual_string(actual_bit_string)
            
            output.write(actual_string)
            
        pass

    def __bitString(self,file):
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8,'0')
            bit_string += bits
            byte = file.read(1)

        return bit_string

    def __removePadding(self,bit_string):

        # Get padding bit
        padding_bin = bit_string[:8]

        # convert padding bit to integer
        padding_integer = int(padding_bin, 2)

        last_index = len(bit_string) - padding_integer
        actual_bit_string = bit_string[8:last_index]

        return actual_bit_string

        
        pass

    def __convert_actual_string(self,actual_bit_string):
        # Initialize progress bar
        actual_bit_string_length = len(actual_bit_string)
        p = ProgressBar(actual_bit_string_length)

        actual_string = ""
        # print(self.compressor.reverse_charbit_map)
        bit_string = ''
        for i in p.progress:
            bit_string += str(actual_bit_string[i])
            if bit_string in self.compressor.reverse_charbit_map:
                actual_string += self.compressor.reverse_charbit_map[bit_string]
                bit_string = ''

        return(actual_string)
        pass