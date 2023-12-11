import math
import os
import sys
import HuffmanTree as HuffmanTree
import EncodingTable as EncodingTable

# CONSTANTS for output file extensions
EXT_BINARY = ".bin"
EXT_CHARACTERS = ".txt"
EXT_TABLE = ".tbl"


def main():
    """
    Main of program.

    python CPSC231F21A4.py
        Prompt for <input_filename> to compress.
    python CPSC231F21A4.py <input_filename>
        Compresses <input_filename>.
    python CPSC231F21A4.py <input_filename1> <input_filename2>
        Creates Huffman Tree for <input_filename1> and <input_filename1> and determines if structure of the trees are equal.
            Equality means same amount of left/right connections and same character in each part of tree.
    python CPSC231F21A4.py <arg1> <arg2> <arg3>
        (exits program with descriptive error indicating too many arguments)

    -V          (optional) argument that turns on more detailed printing (repr instead of str and tree structure output)

    :return: None
    """
    # Check arguments
    args = sys.argv[:]
    verbose = False
    if "-V" in args:
        verbose = True
        args.remove("-V")

    input_filename, input_filename2 = check_args(args)

    # Determine what mode program is in (if comparing second filename will exist)
    compare = input_filename2 is not None

    if compare:
        print("Comparing Huffman Trees of two different files.")
        print()

    # Read in file and turn into dictionary of char -> count
    check_read_access(input_filename)
    text = read_file(input_filename)
    dictionary = to_dictionary(text)

    # Create Huffman Tree
    final_tree = create_huffman_tree(dictionary, verbose)

    print()
    # If compare mode
    if compare:
        # Load second file and do same steps as with first one
        check_read_access(input_filename2)
        text2 = read_file(input_filename2)
        dictionary2 = to_dictionary(text2)
        final_tree2 = create_huffman_tree(dictionary2, verbose)
        print()
        if verbose:
            print("Tree 1:")
            print_indented_tree(final_tree)
            print()
            print("Tree 2:")
            print_indented_tree(final_tree2)
            print()
        # PART 5
        try:
            # Compare the trees
            if final_tree == final_tree2:
                print("Trees are the same in structure!")
            else:
                print("Trees are the different in structure!")
        except Exception as e:
            print("Exception during Part 5", file=sys.stderr)
            raise e
        print("Program completed successfully!")
        sys.exit(0)

    # If we are here we are in the single file mode and not comparing trees
    if verbose:
        print("Created huffman tree:")
        print_indented_tree(final_tree)

    print()

    print(f"Original text was {len(text)} characters in length"
          f" which, with 1 byte per character, would be {len(text)} ASCII bytes!")

    # PART 6
    # Get encoding table
    try:
        encoding_table = EncodingTable.EncodingTable(final_tree)
    except Exception as e:
        print("Exception during Part 6", file=sys.stderr)
        raise e

    # PART 7
    # Turn table into a string
    try:
        output_table = str(encoding_table)
    except Exception as e:
        print("Exception during Part 7", file=sys.stderr)
        raise e

    print(f"The encoding table is:\n{output_table}")

    # Create encoded string from the table for output
    try:
        encode_text = encoding_table.encode_text(text)
    except Exception as e:
        print("Exception during Encoding", file=sys.stderr)
        raise e

    print(f"New text is {len(encode_text)} bits in length, which is {math.ceil(len(encode_text) / 8)} bytes! "
          f"(Plus we'd also have to store the decoding table as well.)")
    print(f"That is {((math.ceil(len(encode_text) / 8)) / len(text)) * 100:.2f}% of the size")

    write_output(input_filename, output_table, encode_text)

    print("Program completed successfully!")


def check_args(args):
    """
    Check program arguments
    :param args: sys.argv copy passed into function
    :return: Two input filenames
                    None for second if not given
                    Prompt for input if first and second not given
    """
    input_filename2 = None
    if len(args) > 3:
        sys.exit(
            f"""Program requires zero/one/two argument(s). Usage:
            Generate (ask for filename): python {args[0]}
            Generate: python {args[0]} input_filename
            Compare: python {args[0]} input_filename1 input_filename2""")
    elif len(args) == 3:
        input_filename = args[1]
        input_filename2 = args[2]
    elif len(args) == 2:
        input_filename = args[1]
    else:
        input_filename = input("Enter an input filename: ")
    return input_filename, input_filename2


def check_read_access(filename):
    """
    Determine if filename is accessible for reading
    :param filename: The string filename
    :return: True if file exists and can be read
    """
    if not os.path.exists(filename):
        sys.exit(f"Input file {filename} does not exist!")
    if not os.access(filename, os.R_OK):
        sys.exit(f"Input file {filename} can not be read from!")


def check_continue(*filenames):
    """
    Check if the user wants to overwrite the files in a list of filenames
    :param filenames: A list of filenames
    :return: True if the user chooses to overwrite these files, otherwise program will exit and not return
    """
    flag = False
    for filename in filenames:
        if os.path.exists(filename):
            flag = True
    if flag:
        print(
            f"Existing output files will be overwritten!")
        confirmation = input("Enter Y/N to continue or exit: ")
        if confirmation.strip().lower() not in ["yes", "y"]:
            sys.exit("Chose not to continue program!")


def read_file(filename):
    """
    Read a file and return as a string of text
    :param filename: The filename to read
    :return: A string of contents of file
    """
    try:
        with open(filename, encoding="utf-8") as input_file:
            text = input_file.read()
    except IOError as ioe:
        sys.exit(f"Error reading input file {filename}!\nIOError -> {ioe}")
    return text


def to_dictionary(text):
    """
    Create a dictionary storing for each symbols as a key, a count of how many times it occurred
    :param text: The string to examine the symbols in
    :return: The dictionary of dict[char] = count
    """
    dictionary = {}
    for char in text:
        # Record 0 for new characters
        if char not in dictionary:
            dictionary[char] = 0
        dictionary[char] += 1
    return dictionary


def create_huffman_tree(dictionary, verbose):
    """
    Created HuffmanTree using the given dictionary
    :param dictionary: The dict[char] = count dictionary from a text file
    :param verbose: Whether or not to print detailed output
    :return: A HuffmanTree from the dictionary
    """
    print("Making huffman tree!")
    # PART1
    try:
        trees = HuffmanTree.make_trees(dictionary)
    except Exception as e:
        print("Exception during Part 1", file=sys.stderr)
        raise e
    # PART2
    try:
        trees.sort()
    except Exception as e:
        print("Exception during Part 2", file=sys.stderr)
        raise e
    # PART3
    try:
        if verbose:
            print("Original list of individual Huffman trees (repr):")
        else:
            print("Original list of individual Huffman trees (str):")
        for tree in trees:
            if verbose:
                print(repr(tree))
            else:
                print(tree)
    except Exception as e:
        print("Exception during Part 3", file=sys.stderr)
        raise e
    print()

    format_length = len(trees) * 3 + 5

    print("Merging trees to make a complete Huffman Tree:")
    while len(trees) > 1:
        trees.sort()
        t1 = trees.pop()
        t2 = trees.pop()
        if verbose:
            print(f"Merging tree {repr(t1)} and {repr(t2)}", end=" ")
        else:
            print(f"Merging tree {str(t1):<{format_length}} and {str(t2):<{format_length}}", end=" ")
        # PART4
        try:
            nt = HuffmanTree.merge(t1, t2)
        except Exception as e:
            print("Exception during Part 4", file=sys.stderr)
            raise e
        if verbose:
            print(f"to make {repr(nt)}")
        else:
            print(f"to make {nt}")
            print(f"\tMerged child trees left {nt.left} and right {nt.right}")
        trees.append(nt)
    print("Merging done!")
    final_tree = trees.pop()
    print("Final tree")
    if verbose:
        print(repr(final_tree))
    else:
        print(final_tree)
    return final_tree


def print_tree(tree):
    """
    Prints out tree information
    :param tree: The HuffmanTree to print
    :return: None
    """
    print("Final tree as a string:")
    print(tree)
    print("Final tree full python representation:")
    print(repr(tree))
    print("Final tree as formatted tree:")
    print_tree(tree)


def write_output(input_filename, output_table, encode_text):
    """
    Write to output files info about the HuffmanTree and resultant encoded information
    :param input_filename: The original filename
    :param output_table: The encoding table string form
    :param encode_text: The encoded text as bit string
    :return: None
    """
    # Make the output files for encoded binary data, encode bit string, and the encoding table
    input_filename = os.path.basename(input_filename)
    output_dir = "output" + os.sep
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_filename_bin = output_dir + input_filename + EXT_BINARY
    output_filename_chr = output_dir + input_filename + EXT_CHARACTERS
    output_filename_tbl = output_dir + input_filename + EXT_TABLE

    # Check if file exists and if so if the user wants to overwrite
    check_continue(output_filename_bin, output_filename_chr, output_filename_tbl)

    # Write en coding table
    try:
        with open(output_filename_tbl, "w", encoding="utf-8") as output_file:
            output_file.write(output_table)
    except IOError as ioe:
        sys.exit(f"Error writing output file {output_filename_tbl}!\nIOError -> {ioe}")
    # Write encoded text
    try:
        with open(output_filename_chr, "w", encoding="utf-8") as output_file:
            output_file.write(encode_text)
    except IOError as ioe:
        sys.exit(f"Error writing output file {output_filename_chr}!\nIOError -> {ioe}")
    # Create binary output and write
    try:
        with open(output_filename_bin, "w+b") as output_file:
            loc = 0
            while loc < len(encode_text):
                binary_string = encode_text[loc:loc + 8]
                binary_string = f"{binary_string:<08}"
                output_file.write(bytearray([int(binary_string, 2)]))
                loc += 8
    except IOError as ioe:
        sys.exit(f"Error writing output file {output_filename_bin}!\nIOError -> {ioe}")


def print_indented_tree(tree, level=0):
    """
    Helper function will traverse HuffmanTree to print structured output
    :param tree: The HuffmanTree to print
    :param level: The level of the tree that program is one
    :return: String form of the HuffmanTree
    """
    # Recurse left first
    if tree.left is not None:
        print_indented_tree(tree.right, level + 1)

    # In the middle print something
    # (Only print characters of length one and not concatenated middle chars)
    if len(tree.char) == 1:
        char = f" ({repr(tree.char)},{tree.count})"
    else:
        char = ""
    # Fill in bit string
    if tree.bit is None:
        bit = ""
    elif tree.bit:
        bit = "1"
    else:
        bit = "0"
    # Print line for the current spot in HuffmanTree
    print(f"{' ' * 5 * level} -{bit}->{char}")

    # Recurse right last
    if tree.right is not None:
        print_indented_tree(tree.left, level + 1)


# Start program here
main()
