# 2023-05-11 - versioning.py
#
# A program that replaces a string in a file and optionally, truncates its length.
#
# Written by Yousif Mohamad

import argparse

# Function that replaces a string
def versioning(absolutePath, originalStr, replaceStr, stringLen):
    # Open the source file
    with open(absolutePath) as src_file:
        contents = src_file.read()

    # Replace a string with another string.
    with open(absolutePath,'r+') as scriptfile:
        # Truncate the string if necessary
        contents = contents.replace(originalStr, replaceStr[0:stringLen])
        scriptfile.write(contents)
        return replaceStr[0:stringLen]

# Argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program that reduces the length of a string')
    parser.add_argument('--absolutePath', type=str, metavar='', help='absolute path of file')
    parser.add_argument('--originalStr', type=str, metavar='', help='string to be replaced')
    parser.add_argument('--replaceStr', type=str, metavar='', help='new value to replace the original string')
    parser.add_argument('--stringLen', required=False, type=int, metavar='', help='maximum integer value of the replacement string\'s length')
    args = parser.parse_args()

    # If conditions are met, output the result of the string after it has been replaced.
    if args.absolutePath != None and args.originalStr != None and args.replaceStr:
        print(versioning(args.absolutePath, args.originalStr, args.replaceStr, args.stringLen))
    # Instruct the user how to use this program
    else:
        print('Error: Usage is versioning.py --absolutePath WWW --originalStr XXX --replaceStr YYY --stringLen ZZZ,\nwhere WWW is the absolute path of the file (e.g. C:\Program Files\...)\nXXX is the original string to be replaced (e.g. 0.0.1)\nYYY is the replacement string (e.g. 0.1.117.fe76eg)\nand ZZZ is the maximum length of the string.')
        print('Example usage: versioning.py --absolutePath C:\Program Files -- originalStr 0.0.1 --replaceStr 0.1.117.fe76eg --stringLen 14')

