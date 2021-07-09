import os
from decompressor import Decompressor
from tqdm import tqdm
class Compressor:
    def __init__(self):
        self.frequency_map = {}
        self.char_list = []
        self.charbit_map = {}
        self.reverse_charbit_map = {}
        self.data = None
        self.encoded_data = ''
        self.bytes_array = None
        self.path = None
        


    def compress(self):
        print("Enter a valid file path..")
        self.path = input()
        file_name,file_extension = os.path.splitext(self.path)

        output_path = file_name + '.bin'

        with open(self.path,'r+') as file , open(output_path,'wb') as output:
            string = file.read()
            string = string.rstrip()
            self.getPaddedEncodedString(string)
            # print(self.encoded_data)
            # print("length",len(self.encoded_data))
            self.getBytesArray()
            output.write(self.bytes_array)
        pass

    def getPaddedEncodedString(self,string):
        # Heloping Methods
        def createBitMap():
            blank = ''
            createBitMapHelper(self.char_list,blank)
            pass

        def createBitMapHelper(char,bit):
            if type(char) == str:
                self.charbit_map[char] = bit
                self.reverse_charbit_map[bit] = char
                return
            left = 0
            right = 1
            createBitMapHelper(char[left],bit+str(left))
            createBitMapHelper(char[right],bit+str(right))

        def encode():
            if self.data == None:
                print("Invalid data!!")
                return
            print("encoding in progress...")
            data_length = len(self.data)
            # progress_bar = tqdm(range(data_length))
            # for i in progress_bar:
            #     if self.data[i] in self.charbit_map:
            #         self.encoded_data += str(self.charbit_map[self.data[i]])
            #     else:

            #         print(data,"Not encoded properly, Or the input string was changed")
            #         return 

            self.encoded_data = ''.join([self.charbit_map[i] for i in self.data])
            # print(self.encoded_data)
            pass
        
        def getPaddedString():
            if self.encoded_data == None:
                print("First encode string ")
                return

            encoded_data_length = len(self.encoded_data)
            rem = encoded_data_length%8
            extra_zero = 8 - rem
            
            # Append Extra string
            self.encoded_data += '0'*extra_zero


            # Binary of extra_zero in 8-bit
            extra_zero = bin(extra_zero)[2:]
            extra_zero = '0'*(8-len(extra_zero)) + extra_zero

            self.encoded_data = extra_zero + self.encoded_data

        # Operations

        self.data = string

        for char in self.data:
            if char in self.frequency_map:
                self.frequency_map[char] = self.frequency_map[char] + 1
            else:
                self.frequency_map[char] = 1


        sorted_chars = sorted(self.frequency_map.items(), key=lambda x: x[1], reverse = True)

        current = None
        self.char_list = list(sorted_chars)
        while len(self.char_list) > 1:
            first = self.char_list.pop()
            second = self.char_list.pop()

            if current == None:
                current = [[first[0],second[0]],first[1] + second[1]]
            else:
                if current[1] > second[1]:
                    current,second = second,current
                    pass
                self.char_list.append(second)
                current = [[current[0],first[0]],current[1] + first[1]]

        first = self.char_list.pop()
        if current == None:
            current = first
        else:
            current = [[current[0],first[0]],current[1] + first[1]]
        self.char_list = current[0]
        createBitMap()
        encode()
        getPaddedString()
        print("Encoding Done")

        pass

    def getBytesArray(self):
        if len(self.encoded_data)%8 != 0:
            print("data was not encoded properly, length is not in multiplle of 8")

        array = []
        for i in range(0,len(self.encoded_data),8):
            byte = self.encoded_data[i:i+8]
            array.append(int(byte,2))

        self.bytes_array = bytes(array)

        pass


    pass



if __name__ == "__main__":
    c = Compressor()

    # c.getPaddedEncodedString('abcdakabcaghaghiklmdfcbmhg')
    # c.getBytesArray()
    c.compress()

    d = Decompressor(c)
    d.decompress()