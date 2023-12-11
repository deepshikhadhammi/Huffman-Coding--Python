"""
CLASS: CPSC231 FALL 2021
NAME:DEEPSHIKHA DHAMMI
TUTORIAL: T08(SARTHAK SHARAN)
STUDENT ID: 30140157
DATE: DECEMBER 10,2021
DESCRIPTION: EncodingTable returns encoded value of all the characters. __init__function assigns values to parameters.
recurse method is used to recursively call tree.left and tree.right. It returns the dictionary which stores the character
as a key and the encoded form of characters as value. __str__ is used to return the string of character and its encoded form.
"""
import sys


class EncodingTable:
    """
    A class to represent an Encoding Table made from a Huffman Tree
    Attributes
    ----------
    encode : str
        The dictionary storing for each symbol "char" as binary bit string code "code"
    """

    def __init__(self, tree):
        """
        Constructs an EncodingTable using a HuffmanTree
        :param tree: The HuffmanTree to use to build the EncodingTable dictionary encode
        """
        # Create empty dictionary
        self.encode = {}
        # Launch recursive function to store values into self.encode dictionary
        self.recurse(tree, "")
    def __str__(self):    # used to return the encoded string
         encode_str=""
         encode_list=[]
         for key in self.encode:    #accessing keys from dictionary self.encode
            encode_list.append(key)  #storing keys in a list
         encode_list.sort()       #sorting the list
         for char in encode_list:   #accessing character from the list
             encode_str+="{}:{}\n".format(repr(char),self.encode[char])   #adding sorted key and value to a string
         return encode_str     #return encoded string
    # PART 7 (recurse)
    def recurse(self, tree, code):    # recursive function

        if tree.bit is not None:    #if bit for tree is not none
            if tree.bit is True:    #if bit is true add 1 to the code
                code=code+"1"
            else:
                code=code+"0"      #if bit is false add 0 to the code
        if tree.left is None and tree.right is None:   # Base Case if left and right tree is none store the character in the dictionary at key and code at value
            self.encode[tree.char]=code
            return self.encode    #return dictionary
        else:
            self.recurse(tree.left,code) #Recursive Case
            self.recurse(tree.right,code)  #Recursive Case

    # PART 6 (string)

    def encode_text(self, text):
        """
        Encodes the provided text using the internal encoding dictionary (turns each character symbol into a bit string)
        :param text: The string text to encode
        :return: A bit string "000100" based on the internal encode dictionary
        """
        output_text = ""
        # Loop through characters
        for char in text:
            # If one matches then encode into bitstring
            if char in self.encode:
                output_text += self.encode[char]
            else:
                sys.exit(f"Can't encode symbol {char} as it isn't in the encoding table:\n{self}")
        return output_text
