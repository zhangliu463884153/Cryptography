# This will output the subkey with maximum bias and output all bias calculations
# to the file 'bias.csv'
'''
Pandas是Python的一个数据分析包，该工具为解决数据分析任务而创建。
Pandas纳入大量库和标准数据模型，提供高效的操作数据集所需的工具。
Pandas提供大量能使我们快速便捷地处理数据的函数和方法。
Pandas是字典形式，基于NumPy创建，让NumPy为中心的应用变得更加简单
'''
import csv
import pandas as pd

key = "AEA5"  # The same key is used for each round of key mixing
'''将DES的S盒S1的第一行作为新的S盒'''
s_box = {'0': 'E',
         '1': '4',
         '2': 'D',
         '3': '1',
         '4': '2',
         '5': 'F',
         '6': 'B',
         '7': '8',
         '8': '3',
         '9': 'A',
         'A': '6',
         'B': 'C',
         'C': '5',
         'D': '9',
         'E': '0',
         'F': '7'
         }

'''
s_box.linear_approximation_table()
     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
0  [ 8  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
1  [ 0  0 -2 -2  0  0 -2  6  2  2  0  0  2  2  0  0]
2  [ 0  0 -2 -2  0  0 -2 -2  0  0  2  2  0  0 -6  2]
3  [ 0  0  0  0  0  0  0  0  2 -6 -2 -2  2  2 -2 -2]
4  [ 0  2  0 -2 -2 -4 -2  0  0 -2  0  2  2 -4  2  0]
5  [ 0 -2 -2  0 -2  0  4  2 -2  0 -4  2  0 -2 -2  0]
6  [ 0  2 -2  4  2  0  0  2  0 -2  2  4 -2  0  0 -2]
7  [ 0 -2  0  2  2 -4  2  0 -2  0  2  0  4  2  0  2]
8  [ 0  0  0  0  0  0  0  0 -2  2  2 -2  2 -2 -2 -6]
9  [ 0  0 -2 -2  0  0 -2 -2 -4  0 -2  2  0  4  2 -2]
10 [ 0  4 -2  2 -4  0  2 -2  2  2  0  0  2  2  0  0]
11 [ 0  4  0 -4  4  0  4  0  0  0  0  0  0  0  0  0]
12 [ 0 -2  4 -2 -2  0  2  0  2  0  2  4  0  2  0 -2]
13 [ 0  2  2  0 -2  4  0  2 -4 -2  2  0  2  0  0  2]
14 [ 0  2  2  0 -2 -4  0  2 -2  0  0 -2 -4  2 -2  0]
15 [ 0 -2 -4 -2 -2  0  2  0  0 -2  4 -2 -2  0  2  0]
maximial value:6
(1, 7): 6 binary(0001,0111)
(2,14):-6 binary(0010,1110)
(3, 9):-6 binary(0011,1001)
(8,15):-6 binary(1000,1111)

'''

inv_s_box = {v: k for k, v in s_box.items()}  # Inverted s-box mapping

perm = [0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15]

#十六进制转二进制
def convert_binary(hex_key):
    scale = 16  # Hex
    num_of_bits = 4
    binary_string = ""

    for hex_char in hex_key:
        i = bin(int(hex_char, scale))[2:].zfill(num_of_bits)
        binary_string += i

    binary_string = binary_string.zfill(16) # Add this?
    return binary_string

#进行S盒操作
def apply_sbox(text):
    out = ""
    for i in text:
        out += s_box[i]
    return out

#置换操作
def permute(original, permutation):
    return [original[i] for i in permutation]

#生成明文
def generate_plaintext():
    # Generate 10 000 16-bit plaintext values
    '''存储为明文字典,下标为明文'''
    plaintext = {}
    for i in range(0, 10000):
        plaintext[str(i)] = ""
        # plaintext[str(i).zfill(16)] = ""
    return plaintext


def encrypt(key):
    """
    4轮操作
    Encrypts 10 000 plaintext to cipher text values. This algorithm has 4 rounds of:
    A) Key Mixing
    B) S-Box substitution
    C) Permutation
    :param key: 16 bit hex key used to encrypt plaintext
    :return: Dictionary of 10 000 plaintext cipher text pairs
    """
    #加密过程执行轮数
    round=4
    plaintext_cipher = generate_plaintext() 
    
    for plain in plaintext_cipher:
        # Initial XOR
        # plaintext_cipher[plain] = format((int(plain, 16)) ^ (int(key, 16)), 'X')
        plaintext_cipher[plain] = format(int(plain) ^ int(key, 16), 'X')
        
        for i in range(0, round):
            # Apply S-box substitutions
            plaintext_cipher[plain] = apply_sbox(plaintext_cipher[plain])

            # Permute output of S-box
            plaintext_cipher[plain] = ''.join(permute(convert_binary(plaintext_cipher[plain]), perm))
            plaintext_cipher[plain] = format(int(plaintext_cipher[plain], 2), 'X')

            # XOR with Key
            plaintext_cipher[plain] = format((int(plaintext_cipher[plain], 16)) ^ (int(key, 16)), 'X').zfill(4)
        #print("Plain=%s,Cihper=%s" %( plain,plaintext_cipher[plain]))
    return plaintext_cipher


def output_plain_cipher_pairs():
    """
    Prints plaintext ciphertext pairs into out_hex.csv
    """
    plain_cipher = encrypt(key)
    w = csv.writer(open("out_hex.csv", "w"))
    for plain, cipher in plain_cipher.items():
        w.writerow([plain, cipher])

def get_U(guess_subkey, cipher):
    """
    Gets the input to the 4th round of S-Box substitutions
    :param subkey: 4 bit Hex value in range (0000, F)
    :param cipher: Corresponding cipher text for the plain text
    :return: Binary string representing the 4th round input to S Box
    返回第四轮S盒的输入,也就是第三轮加密的输出
    """
    # Convert cipher to hex
    hex_cipher = hex(int(cipher, 2))

    # XOR with partial subkey
    r = format(int(guess_subkey, 16) ^ (int(hex_cipher, 16)), 'X')
    #print("r=%s" %r)
    # Reverse S-Box
    out = ""
    for i in str(r):
        out += inv_s_box[i]

    # Return binary
    '''由于convert_binary的原因总是要补齐16位,实际上前12位都是0'''
    return convert_binary(out)[12:]  # This is a 16 bit binary, only want last 4 bits

def attack():
    """
    Generates 10 000 plaintext-ciphertext pairs and calculates the bias for each
    possible partial subkey from 0 - 255.
    :return: Prints the subkey with maximum bias and outputs all results into file "bias.csv"
    """
    plain_cipher_hex = encrypt(key)
    plain_cipher_bin = {}
    d = {'partial_subkey':[], 'count': [], 'bias':[]}

    # Convert the plaintext cipher pairs into binary
    for plain, cipher in plain_cipher_hex.items():
        plain_cipher_bin[convert_binary(plain)] = convert_binary(cipher)

    # Test 256 Partial Subkeys
    '''判断两位密钥,所以二进制表示共8位'''
    for i in range(0, 256):
        count = 0
        for plain, cipher in plain_cipher_bin.items():
            '''猜测第二位和第四位的十六进制密钥'''
            '''第三轮加密的第二位输出'''
            u4_5to8 = get_U(guess_subkey=format(i, 'X').zfill(2)[0],  # EX: F8 -> F
                            cipher=cipher[4:8])
            '''第三轮加密的第四位输出'''
            u4_13to16 = get_U(guess_subkey=format(i, 'X').zfill(2)[1],  # EX: F8 -> 8
                              cipher=cipher[12:])

            u46 = int(u4_5to8[1])
            u48 = int(u4_5to8[3])
            u414 = int(u4_13to16[1])
            u416 = int(u4_13to16[3])

            p5 = int(plain[4])
            p7 = int(plain[6])
            p8 = int(plain[7])

            '''这个式子应该是线性逼近表达式'''
            if u46 ^ u48 ^ u414 ^ u416 ^ p5 ^ p7 ^ p8 == 0:
                count += 1

        d['partial_subkey'].append(format(i,'X').zfill(2))
        d['count'].append(count)
        d['bias'].append(abs(count - 5000) / 10000)

    df = pd.DataFrame(d)
    print("SUBKEY WITH MAXIMUM BIAS: ")
    print(df.loc[df['bias'].idxmax()])
    df.to_csv('bias.csv')

    # Print the binary plaintext cipher text keys into a CSV file
    # w = csv.writer(open("out_bin.csv", "w"))
    # for plain, cipher in plain_cipher_bin.items():
    #     w.writerow([plain, cipher])




if __name__ == "__main__":
    attack()