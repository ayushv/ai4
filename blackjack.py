import sys
import json
import getopt
import os

# print sys.argv
p = sys.argv[1]
p = float(p)
p = (1-p)/9
# print 'prob = ', p
# print 'type of p = ', type(p)

dealerProb = [[0 for x in range(50)] for x in range(6)]
dealerUpFace = [[0 for x in range(10)] for x in range(6)]

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

def print2DArray(arrayname):
	for ii in range(0, len(arrayname)):
		print '\n'
		for jj in range(0, len(arrayname[0])):
			print arrayname[ii][jj],

# print2DArray(dealerProb)
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
# printDealerTable()
def genDealerUpFace():
	for ii in range(0, 6):
		for jj in range(0, 8):
			dealerUpFace[ii][jj] = dealerProb[ii][jj]
		for count in range(0, 8):
			dealerUpFace[ii][8] += p*dealerProb[ii][count+10]
		dealerUpFace[ii][8] += (1-p*9)*dealerProb[ii][18]
		dealerUpFace[ii][8] += p*dealerProb[ii][19]

		for count in range(0, 9):
			dealerUpFace[ii][9] += p*dealerProb[ii][count+30]
		dealerUpFace[ii][9] += (1-p*9)*dealerProb[ii][39]

genDealerTable()
genDealerUpFace()
# print2DArray(dealerUpFace)

# expected value for action stand
evStand = [[0 for x in range(10)] for x in range(48)]

def genEvStand():
	calcHardEvStand()
	calcSoftEvStand()
def calcHardEvStand():
	for ii in range(0, 13):
		for jj in range(0, 10):	
			kk = 0
			while (kk < len(dealerUpFace)-1):
				evStand[ii][jj] -= dealerUpFace[kk][jj]
				# if (jj == 9):
					# print 'asd', dealerUpFace[kk][jj]
				kk += 1
			evStand[ii][jj] += dealerUpFace[5][jj]
	for ii in range(13, 18):
		for jj in range(0, 10):
			count = 13
			# print 'ii = ', ii, ' jj = ', jj
			while (count < ii):
				evStand[ii][jj] += dealerUpFace[count-13][jj]
				# if (ii == 13 and jj == 0):
				# 	print 'add ', dealerUpFace[count-13][jj]
				count += 1
			count = ii+1
			while (count < 18):
				evStand[ii][jj] -= dealerUpFace[count-13][jj]
				# if (ii == 13 and jj == 0):
					# print 'subtract ', dealerUpFace[count-13][jj]
				count += 1
			evStand[ii][jj] += dealerUpFace[5][jj]
			# if (ii == 13 and jj == 0):
			# 	print 'add ', dealerUpFace[5][jj]
def calcSoftEvStand():
	for ii in range(18, 28):
		for jj in range(0, 10):
			evStand[ii][jj] = -1
	for ii in range(28, 38):
		for jj in range(0, 10):
			evStand[ii][jj] = evStand[ii-20][jj]
			evStand[ii+10][jj] = evStand[ii][jj]
genEvStand()
# print2DArray(evStand)

evHit = [[0 for x in range(10)] for x in range(48)]
for ii in range(17, 28):
	for jj in range(0, 10):
		evHit[ii][jj] = -1
def updateEvHit():
	evHitUpdated = False
	ii = 16
	while (ii >= 0):
		for jj in range(0, 10):
			if (ii > 6):
				evHit[ii+31][jj] = evHit[ii+1][jj]
			temp = 0.0
			for count in range(2, 10):
				temp += p*evStandHit[ii+count][jj]
			temp += (1-9*p)*evStandHit[ii+count+1][jj]
			temp += p*evStandHit[ii+31][jj]
			if (evHit[ii][jj] != temp):
				evHit[ii][jj] = temp
				evHitUpdated = True
				# print 'updated evHit'
		ii -= 1
	ii = 37
	while(ii > 27):
		for jj in range(0, 10):
			temp = 0.0
			for count in range(1, 10):
				temp += p*evStandHit[ii+count][jj]
			temp += (1-9*p)*evStandHit[ii+count+1][jj]
			if (evHit[ii][jj] != temp):
				evHit[ii][jj] = temp
				evHitUpdated = True
		ii -= 1


evStandHit = [[0 for x in range(10)] for x in range(48)]
def updateEvStandHit():
	evStandHitUpdated = False
	for ii in range(0, 48):
		for jj in range(0, 10):
			if (evStandHit[ii][jj] != max(evStand[ii][jj], evHit[ii][jj])):
				evStandHit[ii][jj] = max(evStand[ii][jj], evHit[ii][jj])
				evStandHitUpdated = True
				# print 'updated evStandHit'
def genEvStandHit():
	evHitUpdated = True
	evStandHitUpdated = True
	for ii in range(0, 300):
		# print 'while loop ', evHitUpdated, ' ', evStandHitUpdated
		if (evStandHitUpdated):
			# print 'update StandHit'
			updateEvStandHit()
		if (evHitUpdated):
			# print 'update Hit'
			updateEvHit()
	# print 'while end'
genEvStandHit()
# print2DArray(evStandHit)

evDouble = [[0 for x in range(10)] for x in range(48)]
for ii in range(17, 28):
		for jj in range(0, 10):
			evDouble[ii][jj] = -2
def genEvDouble():
	ii = 16
	while(ii > 7):
		for jj in range(0, 10):
			for count in range(1, 10):
				evDouble[ii][jj] += p*evStand[ii+count][jj]
			evDouble[ii][jj] += (1-9*p)*evStand[ii+count+1][jj]
			evDouble[ii][jj] = 2*evDouble[ii][jj]
			evDouble[ii+31][jj] = evDouble[ii+1][jj]
		ii -= 1
	for jj in range(0, 10):
		evDouble[ii+31][jj] = evDouble[ii+1][jj]
	while(ii >= 0):
		for jj in range(0, 10):
			for count in range(2, 10):
				evDouble[ii][jj] += p*evStand[ii+count][jj]
			evDouble[ii][jj] += (1-9*p)*evStand[ii+count+1][jj]
			evDouble[ii][jj] += p*evStand[ii+31][jj]
			evDouble[ii][jj] = 2*evDouble[ii][jj]
		ii -= 1
	ii = 37
	while(ii > 27):
		for jj in range(0, 10):
			for count in range(1, 10):
				evDouble[ii][jj] += p*evStand[ii+count][jj]
			evDouble[ii][jj] += (1-9*p)*evStand[ii+count+1][jj]
			evDouble[ii][jj] = 2*evDouble[ii][jj]
		ii -= 1
genEvDouble()
# print2DArray(evDouble)

evStandHitDouble = [[0 for x in range(10)] for x in range(48)]
def genEvStandHitDouble():
	for ii in range(0, 48):
		for jj in range(0, 10):
			evStandHitDouble[ii][jj] = max(evDouble[ii][jj], evStandHit[ii][jj])
genEvStandHitDouble()

evSplit = [[0 for x in range(10)] for x in range(10)]
def genEvSplit():
	for ii in range(0, 9):
		for jj in range(0, 10):
			for count in range(0, 8):
				evSplit[ii][jj] += p*evStandHitDouble[ii+count][jj]
				# if (ii == 0 and jj == 0):
					# print evStandHitDouble[ii+count][jj]
			evSplit[ii][jj] += (1-9*p)*evStandHitDouble[ii+count+1][jj]
			# if (ii == 0 and jj == 0):
				# print evStandHitDouble[ii+count+1][jj]
			evSplit[ii][jj] += p*evStandHitDouble[ii+29][jj]
			# if (ii == 0 and jj == 0):
				# print evStandHitDouble[ii+29][jj]
			evSplit[ii][jj] = 2*evSplit[ii][jj]
	ii = 9
	for jj in range(0, 10):
		for count in range(0, 9):
			evSplit[ii][jj] += p*evStand[ii+count+19][jj]
		evSplit[ii][jj] += (1-9*p)*evStand[ii+count+20][jj]
		evSplit[ii][jj] = 2*evSplit[ii][jj]
genEvSplit()

evFinalStrategy = [[0 for x in range(10)] for x in range(33)]
finalStrategy = [[0 for x in range(10)] for x in range(33)]
def genEvFinalStrategy():
	# total 33 hand values for player: 15 + 8 + 10
	for ii in range(1, 16):
		for jj in range(0, 10):
			evFinalStrategy[ii-1][jj] = max(evDouble[ii][jj], evStandHit[ii][jj])
			if (evFinalStrategy[ii-1][jj] == evDouble[ii][jj]):
				finalStrategy[ii-1][jj] = 'D'
			elif (evFinalStrategy[ii-1][jj] == evStand[ii][jj]):
				finalStrategy[ii-1][jj] = 'S'
			elif (evFinalStrategy[ii-1][jj] == evHit[ii][jj]):
				finalStrategy[ii-1][jj] = 'H'
	for ii in range(29, 37):
		for jj in range(0, 10):
			evFinalStrategy[ii-14][jj] = max(evDouble[ii][jj], evStandHit[ii][jj])
			if (evFinalStrategy[ii-14][jj] == evDouble[ii][jj]):
				finalStrategy[ii-14][jj] = 'D'
			elif (evFinalStrategy[ii-14][jj] == evStand[ii][jj]):
				finalStrategy[ii-14][jj] = 'S'
			elif (evFinalStrategy[ii-14][jj] == evHit[ii][jj]):
				finalStrategy[ii-14][jj] = 'H'
	index = 0
	ii = 23
	while(ii < 32):
		for jj in range(0, 10):
			evFinalStrategy[ii][jj] = max(evStandHitDouble[index][jj], evSplit[index/2][jj])
			if (evFinalStrategy[ii][jj] == evSplit[index/2][jj]):
				finalStrategy[ii][jj] = 'P'
			elif (evFinalStrategy[ii][jj] == evDouble[index][jj]):
				finalStrategy[ii][jj] = 'D'
			elif (evFinalStrategy[ii][jj] == evStand[index][jj]):
				finalStrategy[ii][jj] = 'S'
			elif (evFinalStrategy[ii][jj] == evHit[index][jj]):
				finalStrategy[ii][jj] = 'H'
		ii += 1
		index += 2
	index = 28 # for soft 12 hand of player
	for jj in range(0, 10):
		evFinalStrategy[ii][jj] = max(evStandHitDouble[index][jj], evSplit[9][jj])
		if (evFinalStrategy[ii][jj] == evSplit[9][jj]):
				finalStrategy[ii][jj] = 'P'
		elif (evFinalStrategy[ii][jj] == evDouble[index][jj]):
			finalStrategy[ii][jj] = 'D'
		elif (evFinalStrategy[ii][jj] == evStand[index][jj]):
			finalStrategy[ii][jj] = 'S'
		elif (evFinalStrategy[ii][jj] == evHit[index][jj]):
			finalStrategy[ii][jj] = 'H'

genEvFinalStrategy()

data = ''
index = 5
count = 0
while (index < 20):
	data += str(index)
	data += '\t'
	for jj in range(0, 10):
		data += str(finalStrategy[count][jj])
		if (jj != 9):
			data += ' '
	data += '\n'
	index += 1
	count += 1
index = 2
while (index < 10):
	data += ('A' + str(index))
	data += '\t'
	for jj in range(0, 10):
		data += str(finalStrategy[count][jj])
		if (jj != 9):
			data += ' '
	data += '\n'
	index += 1
	count += 1
index = 2
while (index < 12):
	if (index == 11):
		data += 'AA'
	else:
		data += (str(index) + str(index))
	data += '\t'
	for jj in range(0, 10):
		data += str(finalStrategy[count][jj])
		if (jj != 9):
			data += ' '
	if (index != 11):
		data += '\n'
	index += 1
	count += 1
# print data

myfile = open('Policy.txt', 'wb')
myfile.write(data)
myfile.close()
# print2DArray(evSplit)