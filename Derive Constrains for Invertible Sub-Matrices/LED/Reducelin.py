#-*- coding:utf-8 -*-
from Compute_Sbox_Division_Trail import Sbox
import copy

#继承于Sbox
class Reduce(Sbox):
	def __init__(self, filename, sbox):
		Sbox.__init__(self, sbox)
		self.filename = filename
		self.divtrial = self.CreateDivisionTrails()

	def ReadIne(self):
		"""
		Read the linear inequalites from filename to a list
		"""
		fileobj = open(self.filename, "r")
		ine = []
		for i in fileobj:
			#strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
			ine.append(list(map(int, (i.strip()).split())))
		fileobj.close()
		return ine

	@staticmethod
	def Integer2Bitlist(n, l):
		"""
		Convert an integer n to its bitstring representation, and the length of the
		bitstring is restricted to l. For an integer whose bitstring representation
		with a length less than l, we add 0 ahead. This function return a list of
		length l.
		we assume the length of the bitstring representation of n is < 256
		"""
		s = list(map(int, list(format(n, "0256b"))))
		s = s[len(s) - l :]
		return s

	@staticmethod
	def ValueOfExpression(p, l):
		"""
		Evaluate the value of the linear inequality at point p, and l represents a linear inequality.
		"""
		assert len(p) + 1 == len(l)
		# COPY the list, since we will modify the list and this will result in a
		# change of the list outside the function.
		temp_p = copy.deepcopy(p)
		temp_p.append(1)
		return sum([x * y for (x, y) in zip(temp_p, l)])


	def InequalitySizeReduce(self):
		"""
		Given a set of points and the corresponding H-Representation, choose a
		subset of inequalities from H-Representation which is equivalent to
		describe the points.
		"""
        #用可分轨道来验证不等式
		points = self.divtrial
		inequalities = self.ReadIne()
		assert len(points) > 0
		assert len(inequalities) > 0
		assert len(points[0]) + 1 == len(inequalities[0])
		length = len(points[0])
		# get all possible points in {0,1}^n
		apoints = [Reduce.Integer2Bitlist(i, length) for i in range(2**length)]
		# get the complementary set of points,也就是不是可分轨道
		cpoints = [p for p in apoints if p not in points]
		ineq = copy.deepcopy(inequalities)
		# rineq stores the inequalities we choose
		rineq = []
		while len(cpoints) > 0:
			temp_p = []
			temp_l = []
			# Fine the inequality which has the most points in cpoints that do
			# not satisfy this inequality
			for l in ineq:
				temp = [p for p in cpoints if (Reduce.ValueOfExpression(p, l) < 0)]
				if len(temp) > len(temp_p):
					temp_p = temp
					temp_l = l
			for p in temp_p:
				cpoints.remove(p)
			rineq.append(temp_l)
			ineq.remove(temp_l)
		return rineq

if __name__ == "__main__":

    cipher = "LED"
    sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]

    filename = cipher + "_Inequalities.txt"
    LED = Reduce(filename, sbox)

    rine = LED.InequalitySizeReduce()

    filename_result = cipher + "_Reduce_Inequalities.txt"

    fileobj = open(filename_result, "w")
    for l in rine:
        fileobj.write(str(l) + "\n")
    fileobj.close()