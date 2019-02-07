import hashlib
import sys

''' 
Comments are inline 

'''


def shift(b, i):
    return (b[i:] + b[:i])


'''
#shift first to last position

def shift(b, i):
    return(b[i:] + b[:i])

during un-shifting, handle arbitrary length string. 

Test case result 

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  Original 
[1, 2, 3, 4, 5, 6, 7, 8, 9, 0] After Shift
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] After unshift - back to original 

'''


def unshift(b, i):
    return shift(b, len(b) - i)


# drop() function removes characters from string

# def drop(b,m):
#    return(b[:m]+b[(m+1):])

# above code drops one character.

# test case:
# b = [0,1,2,3,4,5,6,7,8,9]
# print b[:3]
# print b[4:]
# Dropped '3'

# We need to recover those dropped characters later.
# Till then mark dropped characters as '*'
# Pickup function will try to recover location of characters which
# were dropped.

def pickup(g, m):
    return (g[:m] + '*' + g[m:])


# for i in range(len(flag)):
#    b += bin(ord(flag[i]))[2:].zfill(8)
# the string is padded for 8 bit length so divide above result length by 8
# 48/8 = 6 characters , flag length is 6 characters

# now we have length of flag , compressed value , to find dropped characters
# First we need to find value of m
# l = len(b)
# i = 1
# m = l%i
# so value of m is dependent on length of string.
# We can collect all these values of m for original string
# run original program and collect value of m

m_values = [0, 1, 1, 1, 4, 1, 0, 1, 4, 9, 5,
            1, 10, 7, 4, 1, 15, 13, 11, 9, 7, 5, 3, 1]


# For reversing , we need to start from last element of m_values ,
# from right to left


def reverse(b, mvalues):
    print "length of mvalues: " + str(len(mvalues))
    i = len(mvalues) - 1
    print i
    while (i >= 0):
        m = mvalues[i]
        print m
        b = unshift(b, i + 1)
        b = pickup(b, m)
        i = i - 1
    return b


# calculate sha256 for hash calculation
def create_hash(s):
    print "input : " + s
    hash_object = hashlib.sha256(s)
    hex_dig = hash_object.hexdigest()
    print "Hash : " + hex_dig
    return hex_dig


# bin2ascii()
# convert binary string into ascii string

def bin2ascii(input):
    # each char is padded for 1 byte(8bit) so divide length by 8
    # we need to group of 8 bits and convert it into ASCII
    # binary 8 bits --> int  --> ASCII char
    possible_value = []
    no_of_chars = len(input) / 8
    for i in range(no_of_chars):
        x = input[i * 8:i * 8 + 8]
        print " x : " + x
        y = int(x, 2)  # base 2 input
        print " y : " + str(y)
        z = chr(y)
        print "z: " + z
        possible_value.append(z)
    print "Generated flag : " + str(possible_value)
    return ''.join(possible_value)


# We have sha256 hash of original flag string
# 'e67753ef818688790288702b0592a46c390b695a732e1b9fec47a14e2f6f25ae'
# we can bruteforce 6 characters and compare hash of each output with
# given hash
# We are playing with binary here , so brute-forcing is bit easy.
# Dropped digit will be either 0 or 1

def crack(b):
    for i in range(len(b)):
        if b[i] == '*':  # replace unknown bit
            crack(b[:i] + '0' + b[(i + 1):])
            crack(b[:i] + '1' + b[(i + 1):])
            return
    print "b : " + b

    # before comparing hashes we need to convert binary into ASCII character
    # This is done by bin2ascii() function.
    # The given flag format is evlz{xxxxxx}ctf

    flag_hash = 'e67753ef818688790288702b0592a' \
                '46c390b695a732e1b9fec47a14e2f6f25ae'

    flag = 'evlz{%s}ctf' % bin2ascii(b)
    hash_new = create_hash(flag)

    # compare hash

    if hash_new == flag_hash:
        print "Found it : Flag = " + flag
        sys.exit(0)


# call main routine

part1 = reverse('100001000100110000000100', m_values)
# print part1
part2 = crack(part1)
