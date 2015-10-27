import sys
import json
import getopt
import os

# print sys.argv
p = sys.argv[1]
p = float(p)
p = (1-p)/9
print 'p = ', p
# print 'type of p = ', type(p)

# class state:
# 	dealerFaceUp = 0

dealerProb = [[0 for x in range(50)] for x in range(6)]
for ii in range(0, 6):
	for jj in range(0, 50):
		dealerProb[ii][jj] = 0

dealerProb[0][15] = 1
dealerProb[1][16] = 1
dealerProb[2][17] = 1
dealerProb[3][18] = 1
dealerProb[4][19] = 1
dealerProb[0][35] = 1
dealerProb[1][36] = 1
dealerProb[2][37] = 1
dealerProb[3][38] = 1
dealerProb[4][39] = 1
dealerProb[0][45] = 1
dealerProb[1][46] = 1
dealerProb[2][47] = 1
dealerProb[3][48] = 1
dealerProb[4][49] = 1
for ii in range(20, 30):
	dealerProb[5][ii] = 1

def printDealerTable():
	# for ii in range(0, 30):
	# 	print ii % 10,
	for ii in range(0, 6):
		print '\n'
		for jj in range(0, 30):
			print dealerProb[ii][jj],
# printDealerTable()

def genDealerTable():
	for ii in range(0, 6):
		jj = 14
		while (jj >= 0):
			for count in range(2, 10):
				dealerProb[ii][jj] += p*dealerProb[ii][jj+count]
			count += 1
			dealerProb[ii][jj] += (1-9*p)*dealerProb[ii][jj+count]
			dealerProb[ii][jj] += p*dealerProb[ii][jj+31]
			
			if (jj >= 10):
				dealerProb[ii][jj+30] = dealerProb[ii][jj]
			if (jj <= 4):
				for count in range(1, 10):
					dealerProb[ii][jj+30] += p*dealerProb[ii][jj+30+count]
				dealerProb[ii][jj+30] += (1-9*p)*dealerProb[ii][jj+40]
			jj -= 1

genDealerTable()
printDealerTable()