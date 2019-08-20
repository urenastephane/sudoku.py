import sys
#creating a tab to contain the game from command lines
tab=[]

#function that detects if an element of the game is an unknown value (ie a dot ".") or a fixed figure 
#in reality this function only detects numbers....
import re
def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

#... but we use it once we get arguments to analyse whether the argument is part of the game or a command line (like the name of the file)
#to use this method, you need not to include figures in the name of your python file (otherwise it will be considered part of the game)x
for x in sys.argv:
	#print "Argument: ", x
	if hasNumbers(x) or "...." in x:
		tab.append(x)

#we print the tab to check if it collected all the correct arguments to form the game
print("print initial sudoku game : ")
print(tab)

#print(tab[0][1])

#saving the game's size in l and the size of small squares in cubeLen
l=len(tab)
print(l)

# CHECKING if game size correct and saving size of little cubes. If size not standard, the program will crash 
#their are better ways to do it but i do it for fun during my holidays: no time for that, and it's just to show my mum this game is stupid!
#I'd rather go to the pool!
existingGameSizes=[4,9,12]

if l in existingGameSizes:
	if l == 4:
		cubeLen=2
	if l == 9:
		cubeLen=3
	if l == 12:
		cubeLen=4
else:
	print("GAME NOT STANDARD SIZE - must be 4, 9 or 12 ")
	cubeLen=0

print("cubeLen :")
print(cubeLen)
#we create a list to collect all missing values' coordinates and an array to store their possible values given vetical and horizontal constraints
# and the small cubes in which they are stored to satisfy the sudoku's rules
#if the size of the game is not standard, the program will crash
unknowns=[]
unknownsBis=[]
for i in range(0,l):
	#print(tab[i])
	for j in range(0,l):
		if tab[i][j]==".":
			unknowns.append([i,j,[]])
			unknownsBis.append([i,j,[]])
unknowns2=unknowns
if cubeLen!=0:
	print("unknowns ;")
	print(unknowns)

# now let's check column and vertical of interest and the content of the small cubes in which each values are stored
#to determine the lists of possible values for each unknown value

#first here is a function to return a list with single values (no repeated values)
def unique(list1):
	unique_list = []
	for x in list1:
		if x not in unique_list:
			unique_list.append(x)
	return unique_list
values=[str(x) for x in range(1,l+1)]
print(" possible values :")
print(values)

#here we store for each unknown coordinate their possible values given cubic, horizontal and vertical constraints
def getCubeContent(size,i,j,constraint,tab):
	if i<= (size-1) and j <= (size-1):
		for a in range(0,size):
			for b in range(0,size):
				constraint.append(tab[a][b])
	if i<= (size-1) and j > (size-1):
		for a in range(0,size):
			for b in range(size,2*size):
				constraint.append(tab[a][b])
	if i> (size-1) and j <= (size-1):
		for a in range(size,2*size):
			for b in range(0,size):
				constraint.append(tab[a][b])
	if i> (size-1) and j > (size-1):
		for a in range(size,2*size):
			for b in range(size,2*size):
				constraint.append(tab[a][b])
	return constraint	
					

#getting possibilities for each coordinates
for i in range(0,l):
	for j in range(0,l):
		if tab[i][j]==".":
			constraints=[]
			for a in tab[i]:
				constraints.append(a)
			for a in range(0,l):
				constraints.append(tab[a][j])
			const=getCubeContent(cubeLen,i,j,constraints,tab)
			uniqueConstraints=unique(const)
			val=[x for x in values if x not in uniqueConstraints]
			for a in unknowns:
				if i==a[0] and j==a[1]:
					a[2].append(val)

		
print("unknowns and possible values :")			
print(unknowns)			


#START RESEARCH GIVEN INITIAL CONSTRAINTS CONTAINED INSIDE TAB AND UNKNOWN
#checking the number of unknons
print("len(unknowns) :")
print(len(unknowns))


#function to check if inserting a value satisfies the constraints of the sudoku game
def satisfies(x,tab,i,j,cubeLen):
	constraints=[]
	for a in tab[i]:
		constraints.append(a)
	for a in range(0,l):
		constraints.append(tab[a][j])
	const=getCubeContent(cubeLen,i,j,constraints,tab)
	uniqueConstraints=unique(const)
	if x not in uniqueConstraints:
		return True
	else:
		return False


#check that function satisfies works
print(satisfies(unknowns[1][2][0][0],tab,0,2,cubeLen))


#START RESEARCH OF OPTIMAL CONFIG
# We have a list of strings, to make modifications we have to convert it to a list of lists (mutable)

print(tab[0][0])
table=[]
for a in tab:
	table.append(list(a))

#here check inside the unknowns which ones have only one possibility: in this case, we insert them directly since there is no debate
import time 
for i in range(0,len(unknowns)):
	if len(unknowns[i][2][0])==1:
		table[unknowns[i][0]][unknowns[i][1]]=unknowns[i][2][0][0]
		unknowns[i][2][0]=[]	
print(unknowns)
for a in unknowns:
	if not a[2][0]:
		unknowns.remove(a)
for e in table:
	print(e)
print(unknowns)
print("******************")
table2=list()
for x in table:
	for y in x:
		table2.append(y)

print("-------------- BEGIN ALGORITHM of research: testing possible values given constraints and backtracking-----------------")
print("")
print("")
print("")
finalTab=table

i=-1
i=0
while "." in table2 and i < (len(unknowns)):
	j=0
	while table[unknowns[i][0]][unknowns[i][1]] in "." and j<=(len(unknowns[i][2][0])-1):
		if satisfies(unknowns[i][2][0][j],table,unknowns[i][0],unknowns[i][1],cubeLen) and unknowns[i][2][0][j] not in unknownsBis[i][2]:
			table[unknowns[i][0]][unknowns[i][1]]=unknowns[i][2][0][j]
			unknownsBis[i][2].append(unknowns[i][2][0][j])
			print(unknownsBis[i][2])
		else:
			j=j+1
	if table[unknowns[i][0]][unknowns[i][1]] in ".":
		i=i-1
		print(i)
		table[unknowns[i][0]][unknowns[i][1]]="."
		if unknownsBis[i+1][2]:
			for a in unknownsBis[i+1][2]:
				unknownsBis[i+1][2].remove(a)
		for e in table:
			print(e)
		print("")
	else:
		print("ELSE")
		i=i+1
	table2=list()
	for x in finalTab:
		for y in x:
			table2.append(y)
	

print("------------- FINAL VERSION -------------")
print(unknowns)
print(i)
print(unknownsBis)
for a in finalTab:
	print(a)


