import sys
import json
import getopt
import os

# print sys.argv
p = sys.argv[1]
q=sys.argv[2]

p = float(p)/float(q)
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


def optimalEV( total, activeAce,dealerUpCard, bet ):

	if(total > 21):
		if(activeAce): #//change A from 11 to 1
			return optimalEV(total-10,false,dealerUpCard)
		else:
			return -1 #; //Bust - Lose 1 bet
	
	evHit = hit(total,activeAce,dealerUpCard)
	evStand = stand(total,dealerUpCard)
	evdoubledown=doubledown(total,activeAce,dealerUpCard)

	return max(evHit,evStand,evdoubledown)


def hit( handTotal, activeAce,dealerUpCard):
	expectation = 0.0
#//normal valued card
	for t in range(2,10):
		expectation += optimalEV(handTotal + t, activeAce, dealerUpCard)
#//10 or face card
	expectation += 4.0*optimalEV(handTotal + 10, activeAce, dealerUpCard)
#//ace -- handled different
	if(handTotal < 11):
		expectation += optimalEV(handTotal + 11, true, dealerUpCard)
	else:
		expectation += optimalEV(handTotal + 1, activeAce, dealerUpCard)
	return expectation / 13.0 #; //average of all possibilities
	
def stand( total,  dealerUpCard) :
return p(D Bust) + p(D < total) - p(D > total) # ; //array lookup


def doubledown(handTotal , activeAce , dealerUpCard ):
	expectation = 0.0
#//normal valued card
	for t in range(2,10):
		expectation += stand(handTotal + t, dealerUpCard)
#//10 or face card
	expectation += 4.0*stand(handTotal + 10, dealerUpCard)
#//ace -- handled different
	if(handTotal < 11):
		expectation += stand(handTotal + 11, dealerUpCard)
	else:
		expectation += stand(handTotal + 1,dealerUpCard)
	return 2*expectation / 13.0 #; //average of all possibilities & two times the bet 
	
#def split()

