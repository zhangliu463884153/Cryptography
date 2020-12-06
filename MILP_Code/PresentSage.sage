#-- Present Differential --
# Counting the minimal number of active S-boxes for Present using "Coin" solver in Sage.
# (at least version 5.0 is required, other solvers are possible)
# - Differential cryptanalysis in non-related key setting
# - Any number of rounds (default 1)


#Writes the constraints implied by the input of the Sbox operation to the file f
#in: i1,i2,i3,i4 (bit inputs to Sbox), s (nibble input to Sbox),f (file to write to)
#out: \
def EqSIn(i1,i2,i3,i4,s,f):
  f.write("p.add_constraint(x["+str(i1)+"] + x["+str(i2)+"] + x["+str(i3)+"] + x["+str(i4)+"] - s["+str(s)+"] >=0)"+'\n')
  f.write("p.add_constraint(s["+str(s)+"] - x["+str(i1)+"] >= 0)"+'\n')
  f.write("p.add_constraint(s["+str(s)+"] - x["+str(i2)+"] >= 0)"+'\n')
  f.write("p.add_constraint(s["+str(s)+"] - x["+str(i3)+"] >= 0)"+'\n')
  f.write("p.add_constraint(s["+str(s)+"] - x["+str(i4)+"] >= 0)"+'\n')

#Writes the constraints implied by the Sbox operation to the file f
#in: i1,i2,i3,i4 (inputs to Sbox), o1,o2,o3,o4 (outputs from Sbox),next_i (input difference), next_o (output difference), d (dummy #variable), f (file to write to)
#out: \
def EqSOut(i1,i2,i3,i4,o1,o2,o3,o4,next_i,next_o,d,f):
  #Sbox operation has differential branch number equal to 3  
  f.write("p.add_constraint(x["+str(i1)+"] + x["+str(i2)+"] + x["+str(i3)+"]+ x["+str(i4)+"]+ x["+str(o1)+"]+ x["+str(o2)+"]+ x["+str(o3)+"]+ x["+str(o4)+"] - 3*d["+str(d)+"] >= 0)"+'\n') 
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(i1)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(i2)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(i3)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(i4)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(o1)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(o2)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(o3)+"] >= 0)"+'\n')
  f.write("p.add_constraint(d["+str(d)+"] - x["+str(o4)+"] >= 0)"+'\n')
  
  #Additional constraints to ensure that an input difference always leads to an output difference 
  f.write("p.add_constraint(x["+str(i1)+"] + x["+str(i2)+"] + x["+str(i3)+"] + x["+str(i4)+"] - i["+str(next_i)+"] >= 0)"+'\n') 
  f.write("p.add_constraint(x["+str(o1)+"] + x["+str(o2)+"] + x["+str(o3)+"] + x["+str(o4)+"] - o["+str(next_o)+"] >= 0)"+'\n') 
  f.write("p.add_constraint(i["+str(next_i)+"] - x["+str(i1)+"] >= 0)"+'\n')
  f.write("p.add_constraint(i["+str(next_i)+"] - x["+str(i2)+"] >= 0)"+'\n')
  f.write("p.add_constraint(i["+str(next_i)+"] - x["+str(i3)+"] >= 0)"+'\n')
  f.write("p.add_constraint(i["+str(next_i)+"] - x["+str(i4)+"] >= 0)"+'\n')
  f.write("p.add_constraint(o["+str(next_o)+"] - x["+str(o1)+"] >= 0)"+'\n')
  f.write("p.add_constraint(o["+str(next_o)+"] - x["+str(o2)+"] >= 0)"+'\n')
  f.write("p.add_constraint(o["+str(next_o)+"] - x["+str(o3)+"] >= 0)"+'\n')
  f.write("p.add_constraint(o["+str(next_o)+"] - x["+str(o4)+"] >= 0)"+'\n')
  f.write("p.add_constraint(o["+str(next_o)+"] - i["+str(next_i)+"] >= 0)"+'\n')
  f.write("p.add_constraint(i["+str(next_i)+"] - o["+str(next_o)+"] >= 0)"+'\n')

#Updates a, s, next, dummy, sb, O, CSOut, CSIn, next_i and next_o for the S-box transformation
#in: a (difference vector), s (nibble difference vector for Sbox), next (the next unused index for x), dummy (the next unused index #for d), sb (the next unused index for s), O (list of indices for objective function) CSOut (list of constraints implied by the Sbox #operation), CSIn (list of constraints implied by the input of the Sbox operation), next_i(the next unused index for input difference #for Sbox operation), next_o (the next unused index for output difference for Sbox operation)  
#out: a (difference vector), s (nibble difference vector for Sbox), next (the next unused index for x), dummy (the next unused index #for d), sb (the next unused index for s), O (list of indices for objective function) CSOut (list of constraints implied by the Sbox #operation), CSIn (list of constraints implied by the input of the Sbox operation), next_i(the next unused index for input difference #for Sbox operation), next_o (the next unused index for output difference for Sbox operation)  
def Substitution(a,s,next,dummy,sb,O,CSOut,CSIn,next_i,next_o):
  for i in range(0,16):
    CSOut.append([a[4*i],a[4*i+1],a[4*i+2],a[4*i+3],next,next+1,next+2,next+3,next_i,next_o,dummy])
    dummy=dummy+1
    next_i=next_i+1
    next_o=next_o+1
    O.append(s[i])
    CSIn.append([a[4*i],a[4*i+1],a[4*i+2],a[4*i+3],s[i]])
    s[i]=sb
    sb=sb+1
    a[4*i]=next
    a[4*i+1]=next+1
    a[4*i+2]=next+2
    a[4*i+3]=next+3
    next=next+4
  return [a,s,next,dummy,sb,O,CSOut,CSIn,next_i,next_o]

#Updates a for the permutation operation
#in: a (difference vector)
#out: a (difference vector)
def Permutation(a):
  new_a=[]
  for i in range(0,64):
    new_a.append(0)
  for i in range(0,16):
    new_a[i]=a[4*i]
  for i in range(0,16):
    new_a[i+16]=a[1+4*i]  
  for i in range(0,16):
    new_a[i+32]=a[2+4*i]
  for i in range(0,16):
    new_a[i+48]=a[3+4*i]
  a=new_a
  return a

#Updates a,s,next,dummy,sb,O,CSOut, CSIn, next_i and next_o after one round
#in: a (difference vector), s (nibble difference vector for Sbox), next (the next unused index for x), dummy (the next unused index #for d), sb (the next unused index for s), O (list of indices for objective function) CSOut (list of constraints implied by the Sbox #operation), CSIn (list of constraints implied by the input of the Sbox operation), next_i(the next unused index for input difference #for Sbox operation), next_o (the next unused index for output difference for Sbox operation)  
#out:a (difference vector), s (nibble difference vector for Sbox), next (the next unused index for x), dummy (the next unused index #for d), sb (the next unused index for s), O (list of indices for objective function) CSOut (list of constraints implied by the Sbox #operation), CSIn (list of constraints implied by the input of the Sbox operation), next_i(the next unused index for input difference #for Sbox operation), next_o (the next unused index for output difference for Sbox operation)  
def round(a,s,next,dummy,sb,O,CSOut,CSIn,next_i,next_o):
  S=Substitution(a,s,next,dummy,sb,O,CSOut,CSIn, next_i,next_o)   
  a=S[0]
  s=S[1]
  next=S[2]
  dummy=S[3]
  sb=S[4]
  O=S[5]
  CSOut=S[6]
  CSIn=S[7]
  next_i=S[8]
  next_o=S[9]
  a=Permutation(a)
  return[a,s,next,dummy,sb,O,CSOut,CSIn,next_i,next_o]

#Generates a MILP (Sage) for calculating the minimum number of differentially active S-boxes for 'rounds' rounds of Present in the non-#related key setting and solves this program using the "Coin" solver
#in: rounds (the number of rounds)
#out: the MILP (for calculating the minimum number of differentially active S-boxes for 'rounds' rounds of Present in the non-related #key setting and prints the solution of this program
def giveEquationsPresentandSolve(rounds):
  next=0   #next unused state/key variable index 
  dummy=0  #next unused dummy variable index
  next_i=0 #next unused input variable index
  next_o=0 #next unused output variable index
  sb=0     #next unused state nibble variable index
  a=[]     #state variable
  s=[]     #state nibble variable
  O=[]     #list of indices for objective function  
  CSIn=[]  #list of constraints implied by the input of the Sbox operation  
  CSOut=[] #list of constraints implied by the Sbox operation   
  CA=[]    #list of indices for constraint to ensure not all inputs are zero 

  for i in range(0,64):
    a.append(next)
    CA.append(next)
    next=next+1
  for i in range(0,16):
    s.append(sb)
    sb=sb+1

  for i in range(0,rounds):
    NR=round(a,s,next,dummy,sb,O,CSOut,CSIn,next_i,next_o)
    a=NR[0]
    s=NR[1]
    next=NR[2]
    dummy=NR[3]
    sb=NR[4]
    O=NR[5]
    CSOut=NR[6]
    CSIn=NR[7]
    next_i=NR[8]
    next_o=NR[9]

  f = open('Eq-Present-With-'+str(rounds)+'-Rounds-Differential.sage','w')
  f.write("p = MixedIntegerLinearProgram(maximization=False, solver=\"Coin\")"+'\n')
  f.write("x = p.new_variable(binary=True)"+'\n')
  f.write("d = p.new_variable(binary=True)"+'\n')
  f.write("s = p.new_variable(binary=True)"+'\n')
  f.write("i = p.new_variable(binary=True)"+'\n')
  f.write("o = p.new_variable(binary=True)"+'\n')
  f.write('\n')
  f.write("p.set_objective(")   
  for i in range (0, len(O)-1):
    f.write("s["+str(O[i])+"] + ")
  f.write("s["+str(O[len(O)-1])+"] )"+'\n')
  f.write('\n')
  f.write("p.add_constraint(")
  for i in range (0, len(CA)-1):
    f.write("x["+str(CA[i])+"] + ")
  f.write("x["+str(CA[len(CA)-1])+"] >= 1 )"+'\n')
  for i in range (0, len(CSOut)):
    EqSOut(CSOut[i][0],CSOut[i][1],CSOut[i][2],CSOut[i][3],CSOut[i][4],CSOut[i][5],CSOut[i][6],CSOut[i][7],CSOut[i][8],CSOut[i][9],CSOut[i][10],f)
  for i in range (0, len(CSIn)):
    EqSIn(CSIn[i][0],CSIn[i][1],CSIn[i][2],CSIn[i][3],CSIn[i][4],f)
  f.write('\n')
  f.write("solution=p.solve()"+'\n')
  f.write("print \"Minimal number of S-boxes:\", solution"+'\n')
  f.close()
  execfile('Eq-Present-With-'+str(rounds)+'-Rounds-Differential.sage')

giveEquationsPresentandSolve(1)