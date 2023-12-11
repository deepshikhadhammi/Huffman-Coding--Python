"""
CLASS: CPSC231 FALL 2021
NAME:DEEPSHIKHA DHAMMI
TUTORIAL: T08(SARTHAK SHARAN)
STUDENT ID: 30140157
DATE: DECEMBER 10,2021
DESCRIPTION: The program creates tree based on the characters and their occurences(count).Thereafter, they are sorted
according to the count value by using __lt__ function.Thereafter merge function is used to combine two huffmann trees
and at the end this function gives us the final huffmann tree.__eq__method is used to compare the two Huffmann trees.
__str__ and __repr__ are used to return the merging trees, merged tree and the final tree.

"""

class HuffmanTree:
    """
    A class to represent an Huffman Tree
    Attributes
    ----------
    char : str
        The characters represented by this tree
    count : int
        The count of how many times char occurred in the text
    left : HuffmanTree/None
        The left HuffmanTree below this one
    right : HuffmanTree/None
        The right HuffmanTree below this one
    bit : bool
        The bit symbol used to reach this HuffmanTree (either True/False for 1/0)


    General Structure
                         HuffmanTree (char,count,bit)
                          /    \
                      left    right
                        /        \
                HuffmanTree      HuffmanTree

    Default Structure
                         HuffmanTree (char,count,None)
                          /    \
                      left    right
                        /        \
                     None         None
    """

    # PART1 (constructor)
    def __init__(self, char, count, left=None, right=None, bit=None): #used to assign values to the parameters
        self.char = char
        self.count = count
        self.left = left
        self.right = right
        self.bit = bit

    # PART 2 (order)
    def __lt__(self, other): # used to sort the list of trees based on the count value of characters
        if self.count > other.count:
            return True
        elif self.count < other.count:
            return False
        elif self.count == other.count: # if both the counts are equal it will check which character is greater
            if self.char > other.char:
                return True
            else:
                return False
    #PART 3 (string)
    def __str__(self):     # method used to produce a string
        bitstring=None
        left=""
        right=""
        if self.left is None: # if left is assign it will assign the string"None" to left
            left="None"
        else:
           left=repr(self.left.char) # otherwise it will assign the character to left
        if self.right is None:    # if right is none it will assign the string"None" to right
            right="None"
        else:
           right=repr(self.right.char) # otherwise it will assign the character to the right
        if self.bit == True: #if bit is true it will assign string "1" to bitstring
            bitstring = "1"
        elif self.bit == False: # if bit is false it will assign"0" to bitstring
            bitstring = "0"

        return "(%s,%d,%s,%s,%s)" % (repr(self.char),self.count,left,right, bitstring) #returning string
    #PART 3 (representation)
    def __repr__(self):

        return "HuffmannTree(%s,%d,%s,%s,%s)"%(repr(self.char),(self.count),repr(self.left),repr(self.right),repr(self.bit))
    #PART 5 (equality)
    def __eq__(self, other):  # it checks whether the two Huffmann trees are equal or not
     if (self.char == other.char and self.left== other.left and self.right == other.right):# based on the character, left and the right tree it checks for equality
       return True
     else:
        return False
# PART4 (merge)
def merge(t1,t2):  #this method is used to merge two Huffmann Trees
    A=None
    B=None
    if t1.count < t2.count:   #if count is smaller for tree1 A will be equal to tree1 and b will be equal to tree2
        A=t1
        B =t2

    elif t2.count < t1.count: # if tree 2 count is smaller A will be equal to tree 2 and B will be tree1
        A = t2
        B = t1

    elif t1.count == t2.count: # if both the counts are equal check based on character
     if (t1.char< t2.char): # if character for tree1 is smaller A will be tree1 and and B will be T2
        A = t1
        B = t2
     else:  #if character for tree2 is smaller A will be tree2 and B will be tree1
        A = t2
        B = t1
    A.bit=False  # assign bit 0 to A
    B.bit=True   #assign bit 1 to B
    char = A.char + B.char   #merging character
    count = A.count + B.count    #merging count
    left = A                    #left tree
    right = B                    #right tree
    bit=None                    #bit value
    merge_tree = HuffmanTree(char, count, left, right, bit)     #merging tree by calling the constructor
    return merge_tree         #returning merge_tree

#PART1 (merge_trees)
def make_trees(dictionary):
    list = []          #list to store Huffmann Tree
    for key, value in dictionary.items():  #extracting key and values from the dictionary

        huff_tree = HuffmanTree(key, value)   #calling constructor
        list.append(huff_tree)              #storing Huffmann tree in list

    return list          #return Huffmann Tree list



