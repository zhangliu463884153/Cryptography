#ʹ��sagemath�����ַ�֧�������Է�֧��

sbox=[]
with open('sbox.txt', 'r') as f:
    for line in f:
        sbox.append(int(line))
from sage.crypto.sbox import SBox
S=SBox(sbox)

S.differential_branch_number()
S.linear_branch_number()