import random

factor=4
X=[]
Y=[]
number_of_points = 200
for i in range(number_of_points):
	X.append(-50*factor+100*factor*random.random())
	Y.append(-50*factor+100*factor*random.random())

file_name='random_points200.txt'
with open(file_name,'w') as f:
	for i in X:
		f.write(str(i)+' ')
	f.write('\n')
	for i in Y:
		f.write(str(i)+' ')