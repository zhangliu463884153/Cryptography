# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# Example code for generating the MILP model for LBlock
# Run on Python 3
half_cipher_lenght = 64
WORD_SIZE = 16
marker = 0
add_counter = 0
flag = 0
#共有4个s盒用于加密阶段


def sboxSpecificSubjection (inX , outY ):
    
    global marker
    eqn = []
    
    eqn . append (' + '. join ([ inX [t] for t in range (0, WORD_SIZE )]) + ' - y'+ str( marker ) + ' >= 0')
    for t in range (0, WORD_SIZE ):
        eqn . append (inX [t] + ' - ' + 'y' + str ( marker ) + ' <= 0')
    marker = marker + 1
    temp1 = ' + '. join (['16 ' + inX[i] for i in range (0 ,16)])
    temp2 = ' - '. join ([ outY [i] for i in range (0 ,16)])
    eqn . append ( temp1 + ' - ' + temp2 + ' >= 0')

    temp1 = ' + '. join ([ '16 ' + outY [i] for i in range (0 ,16)])
    temp2 = ' - '. join ([ inX[i] for i in range (0 ,16)])
    eqn . append ( temp1 + ' - ' + temp2 + ' >= 0')

    '''
    #差分分支数
    global flag
    for j in range (0, len (inX)):
        eqn . append (inX[j]+'+'+outY[j] + ' - 2 d' + str ( flag ) +' >= 0')
        eqn . append ('d' + str ( flag ) + ' - ' + inX[j] + ' >= 0')
        eqn . append ('d' + str ( flag ) + ' - ' + outY[j] + ' >= 0')
        flag = flag + 1
    '''
    return eqn



def xorAdditionSubjection (A, B, C):
    
    global add_counter
    eqn = []
    for j in range (0, len (A)):
        eqn . append (' + '. join ([A[j],B[j],C[j]]) + ' - 2 a' + str ( add_counter ) +' >= 0')
        eqn . append ('a' + str ( add_counter ) + ' - ' + A[j] + ' >= 0')
        eqn . append ('a' + str ( add_counter ) + ' - ' + B[j] + ' >= 0')
        eqn . append ('a' + str ( add_counter ) + ' - ' + C[j] + ' >= 0')
        eqn . append (' + '. join ([A[j],B[j],C[j]]) + ' <= 2')
        add_counter = add_counter + 1
    return eqn


def F_Subjection (r,inV , outV , rightV , middV ):
    
    eqn = []
    
    eqn = eqn + sboxSpecificSubjection ( inV [0 : 16], outV [0 :16]  )
    eqn = eqn + sboxSpecificSubjection ( inV [16 : 32], outV [16 : 32],  )
    eqn = eqn + sboxSpecificSubjection ( inV [32 :48] , outV [32 :48]  )
    eqn = eqn + sboxSpecificSubjection ( inV [48:64] , outV [48:64] )

    eqn = eqn + xorAdditionSubjection (outV , rightV , middV )
    
    if r < ROUND_TO_COUNT+1:
        count=0
        L=L_At_Round (r+1)
        for i in range(0,16):
            eqn.append(middV[i]+" - "+L[count]+" =  0")
            count=count+1
        for i in range(32,48):
            eqn.append(middV[i]+" - "+L[count]+" = 0")
            count=count+1
        for i in range(16 , 32):
            eqn.append(middV[i]+" - "+L[count]+" = 0")
            count=count+1
        for i in range(48,64):
            eqn.append(middV[i]+" - "+L[count]+" = 0")
            count=count+1
        count=0
        R=R_At_Round (r+1)
        for i in range(16 , 32):
            eqn.append(inV[i]+" - "+R[count]+" = 0 ")
            count=count+1
        for i in range(0,16):
            eqn.append(inV[i]+" - "+R[count]+" = 0 ")
            count=count+1
        for i in range(48,64):
            eqn.append(inV[i]+" - "+R[count]+" = 0 ")
            count=count+1
        for i in range(32,48):
            eqn.append(inV[i]+" - "+R[count]+" = 0 ")
            count=count+1
    
    return eqn


def F_Out_At_Round (r):
    assert (r >= 1)
    return ['fout_r'+ str(r)+ '_'+ str(i) for i in range (0, half_cipher_lenght )]

def middVars_At_Round (r):
    assert (r >= 1)
    return ['midd_r'+ str(r)+ '_'+ str(i) for i in range (0, half_cipher_lenght )]

def L_At_Round (r):
    assert (r >= 1)
    return ['L_r'+ str(r)+ '_'+ str(i) for i in range (0, half_cipher_lenght )]

def R_At_Round (r):
    assert (r >= 1)
    return ['R_r'+ str(r)+ '_'+ str(i) for i in range (0, half_cipher_lenght )]
def rotXorOut_At_Round (r):
    assert (r >= 1)
    return L_At_Round (r +1)


def genEncryptSubjectionAtRound (r):
    eqn = []
    inF_bits = L_At_Round (r)
    midd_bits = middVars_At_Round (r)
    fout_bits = F_Out_At_Round (r)
    right_bits = R_At_Round (r)
    
    eqn . append (' + '. join ([ inF_bits [t] for t in range (0, half_cipher_lenght )]) + ' >= 1')
    eqn = eqn + F_Subjection (r, inF_bits , fout_bits, right_bits , midd_bits)
    #eqn = eqn + Permutation(right_bits)
    return eqn

def genEncrypSubjection ( totalRound ):
    eqn = []
    
    for i in range (1, totalRound + 1):
        eqn = eqn + genEncryptSubjectionAtRound (i)
    return eqn


def getVariables (C):
    V = set ([])
    for s in C:
        temp = s. strip ()
        temp = temp . replace ('+', ' ')
        temp = temp . replace ('-', ' ')
        temp = temp . replace (' >=', ' ')
        temp = temp . replace (' <=', ' ')
        temp = temp . split ()
        for v in temp :
            if not v. isdecimal ():
                V.add(v)
    return V



    
filename="NBC.lp"
f=open(filename,'w')
    
global ROUND_TO_COUNT
ROUND_TO_COUNT = 8
f.write("Minimize"+'\n')
f.write(' + '. join ( ['y' + str(i) for i in range (0, ROUND_TO_COUNT *4)] )+'\n')

f.write('Subject To'+'\n')
    
AA = genEncrypSubjection ( ROUND_TO_COUNT )
    

for x in AA:
    f.write(str(x)+'\n')
    
f.write('Binary'+'\n')
for v in getVariables (AA):
    f.write(str(v)+'\n')
f.write('End'+'\n')
    
f.close()
