import matplotlib.pyplot as plt  # For visualizations
import numpy as np        # For numeric multidimensional array values
from scipy.interpolate import interp1d
from scipy.interpolate import spline
from draw import *      # Including another code file to draw the output
from statistics import mean  # From statistics module include mean() function
import random        # Inlcuding random module
import math   # For mathematical calculations
import time   # To get system time
import json   # To store the data

# Function to calculate euclid distance between two points.
def euclid_dist(x1,y1,x2,y2):
	return (math.sqrt((x1-x2)**2+(y1-y2)**2))

# Function to make clusterhead in a cluster based on the threshhold energy (0.1 joules)
def calculateClusterHead(cellsList,consider):
	for i in range(1,17):     # Considering total 16 clusters(4x4 grid)
		if(consider[i]==True):
			max_energy_index = -1
			max_energy = 0
			for j in range(len(cellsList[i])):
				if(cellsList[i][j]['energy']>=cellsList[i][j]['threshold'] and cellsList[i][j]['isDead']==False and cellsList[i][j]['energy']>=max_energy):
					max_energy = cellsList[i][j]['energy']
					max_energy_index = cellsList[i][j]['id']

			for j in range(len(cellsList[i])):
				if(max_energy_index == cellsList[i][j]['id']):
					cellsList[i][j]['isclusterHead'] = True
					break
	return cellsList

# Function to calculate energy by nodes to transmit a packet between two nodes
def transmissionEnergy(k,d):
	return 50*pow(10,-9)*k+10*pow(10,-12)*(d**2)*k  # 50 nJ/bit + 100 pJ/bit/m2

# Function to calculate energy consummed by node while receiving any packet
def receivingEnergy(k):
	return 50*pow(10,-9)*k  # 50 nJ/bit 

# Function to calculate idle energy
def idleEnergy(k):
	return 40*pow(10,-9)*k # 40 nJ/bit

# Function to find location of clusterHead in a cluster
def findClusterHeadLocation(cell):
	x_ch,y_ch=0,0
	for i in range(len(cell)):
		if(cell[i]['isClusterHead']):
			x_ch,y_ch=cell[i]['location']['x'],cell[i]['location']['y']
			break
	return (x_ch,y_ch)

# Function to check whether all the nodes of a cell are dead
def isCellDead(cell):
	flag=True
	for i in range(len(cell)):
		if(cell[i]['isClusterHead']==True and cell[i]['isDead']==False):
			flag=False
			break
	return flag

# Function to find the path to transmit the data
def findQueryPath(cellsList):
	path={i:[] for i in range(1,5)}
	for col in range(1,5):   # 4 columns in 4x4 grid
		for row in range(4):  # 4 rows in 4x4 grid
			if(isCellDead(cellsList[4*row+col])==False):
				path[col].append(4*row+col)
	return path

# Function to find the number of dead nodes in the network
def findNumberOfDeadNodes(cellsList):
	count_=0
	for i in range(len(cellsList)):
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isDead']==True):
				count_+=1
				print('Dead Node ID:',cellsList[i][j]['id'])
	return count_

# Function to check if all nodes having energy less than thershhold energy
def isAllLessThanThreshold(cell):
	flag = True
	for i in range(len(cell)):
		if(cell[i]['energy']>=cell[i]['threshold']):
			flag = False
			break
	return flag

# Function to make node dead
def makeDead(cellsList):
	for i in range(1,len(cellsList)):
		if(isAllLessThanThreshold(cellsList[i])):
			print("****************** ALL DEAD! ********************** CELL ",i)
			for j in range(len(cellsList[i])):
				if(cellsList[i][j]['energy']<cellsList[i][j]['threshold']):
					cellsList[i][j]['isDead'] = True
	return cellsList

# Function to find the round count where first node dead
def findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind=0
	for i in range(len(roundAxis)):
		if(numberOfDeadNodesAxis[i]==1):
			ind = i
			break
	return ind

# Consider BS having infinite energy
# When BaseStation broadcasts SYNC message
def step2(cellsList,consider):
	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				k=250*8   # Each packet size 250 byte
				energyUsed=receivingEnergy(k)
				if(cellsList[i][j]['isDead']==False):
					cellsList[i][j]['energy']-=energyUsed
					if(cellsList[i][j]['energy']<=0):
						cellsList[i][j]['energy']=0
						cellsList[i][j]['isDead']=True
	return cellsList

# When BS broadcast DUTY message.
def step5(cellsList,consider):
	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				k=250*8  # Each packet size 250 bytes
				energyUsed=receivingEnergy(k)
				if(cellsList[i][j]['isDead']==False):
					cellsList[i][j]['energy']-=energyUsed
					if(cellsList[i][j]['energy']<=0):
						cellsList[i][j]['energy']=0
						cellsList[i][j]['isDead']=True
	return cellsList

# When BS broadcasts SCH message (frame and slot information, CH_id, US_CH_id, SL_no)
def step7(cellsList,consider):
	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				k=250*8  # Each packet size 250 bytes
				energyUsed=receivingEnergy(k)
				if(cellsList[i][j]['isDead']==False):
					cellsList[i][j]['energy']-=energyUsed
					if(cellsList[i][j]['energy']<=0):
						cellsList[i][j]['energy']=0
						cellsList[i][j]['isDead']=True
	return cellsList

# Each cluster head will send TDMA schedule for its cluster members.
def step10(cellsList,consider):
	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				if(cellsList[i][j]['isClusterHead']==True and cellsList[i][j]['isDead']==False):
					cellsList[i][j]['energy']-=broadcastingEnergy
					if(cellsList[i][j]['energy']<=0):
						cellsList[i][j]['energy']=0
						cellsList[i][j]['isDead']=True

	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				if(cellsList[i][j]['isClusterHead']==False and cellsList[i][j]['isDead']==False):
					cellsList[i][j]['energy']-=receivingEnergy(800)
					if(cellsList[i][j]['energy']<=0):
						cellsList[i][j]['energy']=0
						cellsList[i][j]['isDead']=True
	return cellsList

# Control slot communication according to LDC MAC protocol
def step11_a(cellsList):
	for i in range(len(cellsList)):
		count_=0
		total_nodes=0
		x_ch,y_ch = findClusterHeadLocation(cellsList[i])
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==False and cellsList[i][j]['isDead']==False):
				total_nodes+=1
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==False and cellsList[i][j]['isDead']==False and math.floor(random.random()/0.5)==1):
				count_+=1
				x,y = cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y']
				d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
				k = 20*8   # Control slot size 20 bytes
				cellsList[i][j]['wantToSendData']=True
				cellsList[i][j]['energy']-=transmissionEnergy(k,d)
				if(cellsList[i][j]['energy']<=0):
					cellsList[i][j]['energy']=0
					cellsList[i][j]['isDead']=True
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==True and cellsList[i][j]['isDead']==False):
				k = 20*8  # Control slot size 20 bytes
				cellsList[i][j]['energy']-= count_*receivingEnergy(k)
				cellsList[i][j]['energy']-= (total_nodes-count_)*(receivingEnergy(k))/2
				if(cellsList[i][j]['energy']<=0):
					cellsList[i][j]['energy']=0
					cellsList[i][j]['isDead']=True
	return cellsList

# Data transmission starts according to LDC-MAC protocol
def step11_b(cellsList):
	for i in range(len(cellsList)):
		x_ch,y_ch = findClusterHeadLocation(cellsList[i])
		count_=0
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==False and cellsList[i][j]['isDead']==False and cellsList[i][j]['wantToSendData']==True):
				x,y=cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y']
				d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
				k = 250*8   #Data packet size 250 bytes
				count_+=1
				cellsList[i][j]['energy']-=transmissionEnergy(k,d)
				if(cellsList[i][j]['energy']<=0):
					cellsList[i][j]['energy']=0
					cellsList[i][j]['isDead']=True
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==True and cellsList[i][j]['isDead']==False):
				k = 250*8  #Data packet size 250 bytes
				cellsList[i][j]['energy']-= count_*receivingEnergy(k)
				if(cellsList[i][j]['energy']<=0):
					cellsList[i][j]['energy']=0
					cellsList[i][j]['isDead']=True
				break
	return cellsList

#Data collection from all clusterHeads via upstream path
def step12(cellsList,considerColumn,queryPath):
	for col in queryPath.keys():
		if(considerColumn[col]==True):
			upstreamPath=queryPath[col][::-1]
			for i in range(len(upstreamPath)):
				energyUsed=0
				if(i!=(len(upstreamPath)-1)):
					x_ch,y_ch=findClusterHeadLocation(cellsList[upstreamPath[i+1]])
					x,y=findClusterHeadLocation(cellsList[upstreamPath[i]])
					d=euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
					k=250*8*(i+1) #Each packet size 250 bytes
					energyUsed=transmissionEnergy(k,d)
					for j in range(len(cellsList[upstreamPath[i]])):
						if(cellsList[upstreamPath[i]][j]['isClusterHead']==True and cellsList[upstreamPath[i]][j]['isDead']==False):
							k=250*8  # Each packet size 250 bytes
							cellsList[upstreamPath[i]][j]['energy']-=(energyUsed)
							if(cellsList[upstreamPath[i]][j]['energy']<=0):
								cellsList[upstreamPath[i]][j]['energy']=0
								cellsList[upstreamPath[i]][j]['isDead']=True
							break
				else:
					x_ch,y_ch=0,105  # BaseStation location for 100x100 area
					x,y=findClusterHeadLocation(cellsList[upstreamPath[i]])
					d=euclid_dist(x/4,y/4,x_ch,y_ch)
					k=250*8*(i+1)   # Each packet size 250 bytes
					energyUsed=transmissionEnergy(k,d)
					for j in range(len(cellsList[upstreamPath[i]])):
						if(cellsList[upstreamPath[i]][j]['isClusterHead']==True and cellsList[upstreamPath[i]][j]['isDead']==False):
							k=250*8  #Each packet size 250 bytes
							cellsList[upstreamPath[i]][j]['energy']-=(energyUsed)
							if(cellsList[upstreamPath[i]][j]['energy']<=0):
								cellsList[upstreamPath[i]][j]['energy']=0
								cellsList[upstreamPath[i]][j]['isDead']=True
							break
			for i in range(1,len(upstreamPath)):
				for j in range(len(cellsList[upstreamPath[i]])):
					if(cellsList[upstreamPath[i]][j]['isClusterHead']==True and cellsList[upstreamPath[i]][j]['isDead']==False):
						k=250*8*i  #Each packet size 250 bytes
						cellsList[upstreamPath[i]][j]['energy']-=receivingEnergy(k)
						if(cellsList[upstreamPath[i]][j]['energy']<=0):
							cellsList[upstreamPath[i]][j]['energy']=0
							cellsList[upstreamPath[i]][j]['isDead']=True
						break
	return cellsList


factor=4
show_graphics = 0
if(show_graphics==1):
	Screen()
	ht()
	title('Grid')
	speed(0)
	draw_grid(4)
	draw_base_station('red',-15,50*factor+40,15,50*factor+40,0,50*factor+70,0,50*factor+20) # Deployment of all nodes in 100x100 area
base_stn={
	'x':0,
	'y':105,
}  # BaseStation coordinates
X=[]
Y=[]

file_='random_points200.txt'   # Deployed nodes coordinate file
listt=[]
with open(file_,'r') as f:
	for line in f:
		listt.append(line)

X = list(map(float,listt[0].strip().split(' ')))
Y = list(map(float,listt[1].strip().split(' ')))

NodesList=[]

for i in range(len(X)):
	Node={
		'id':0,
		'energy': 0,
		'location':
		{
			'x':0,
			'y': 0,
		},
		'isClusterHead': False,
		'cellNumber':0,
		'isDead':False,
		'threshold':0.1,
		'wantToSendData':False
	}
	Node['id']=i+1
	Node['energy']=5    # Energy of Each node is 5 Joules
	Node['location']['x']=X[i]
	Node['location']['y']=Y[i]
	Node['isClusterHead']=False
	Node['cellNumber']=0
	NodesList.append(Node)

if(show_graphics==1):
	for i in range(len(X)):
		draw_vertex('red',X[i],Y[i])
l=[(0,0)]*16   # 4x4 grid (total 16 clusters)

cell_data={i:{'x_min':0,'x_max':0,'y_min':0,'y_max':0} for i in range(1,17)}
cnt=0

for j in range(0,100,25):   # 100x100 area is divied into 16 grids(4x4 Each)
	for i in range(0,100,25):
		cnt+=1
		x_min=(-50+i)*factor
		x_max=(-25+i)*factor
		y_min=(-50+j)*factor
		y_max=(-25+j)*factor
		cell_data[cnt]['x_min']=x_min
		cell_data[cnt]['x_max']=x_max
		cell_data[cnt]['y_min']=y_min
		cell_data[cnt]['y_max']=y_max

cellsList=[]*17
for i in range(17):
	cellsList.append([])

for i in range(len(NodesList)):
	x=NodesList[i]['location']['x']
	y=NodesList[i]['location']['y']
	for j in cell_data.keys():
		if(cell_data[j]['x_min']<=x and x<=cell_data[j]['x_max'] and cell_data[j]['y_min']<=y and y<=cell_data[j]['y_max']):
			NodesList[i]['cellNumber']=j
			cellsList[j].append(NodesList[i])
			break

clusterHead=[0]*17
consider = { i:True for i in range(1,17)}
cellsList = calculateClusterHead(cellsList,consider)
time.sleep(2)
for i in range(1,17):
	for j in range(len(cellsList[i])):
		if(cellsList[i][j]['isClusterHead']==True):
			(x,y)=(cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y'])
			if(show_graphics==1):
				draw_vertex('green',x,y)
			break

broadcastingEnergy=transmissionEnergy(800,25*math.sqrt(2))

#step:1 Each sensor node sends Hello message to BS
for i in range(len(cellsList)):
	for j in range(len(cellsList[i])):
		(x,y)=(cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y'])
		# (x_base,y_base)=(base_stn['x'],base_stn['y'])
		x_base,y_base=0,105
		d=euclid_dist(x/4,y/4,x_base,y_base)
		k=250*8 #changed
		energyUsed=transmissionEnergy(k,d)
		cellsList[i][j]['energy']-=energyUsed
		if(cellsList[i][j]['energy']<=0):
			cellsList[i][j]['isDead']=True
			cellsList[i][j]['energy']=0

#step:2 BS broadcasts SYNC message
consider={ i: True for i in range(17) }
cellsList = step2(cellsList,consider)

#step:4 BS chooses the node with the highest RE as the CH in each grid
consider={ i: True for i in range(17) }
cellsList = calculateClusterHead(cellsList,consider)

#step:5 BS broadcast DUTY message.
consider={ i: True for i in range(17) }
cellsList = step5(cellsList,consider)


#step:7 BS broadcasts SCH message (frame and slot information, CH_id, US_CH_id, SL_no)
consider={ i: True for i in range(17) }
cellsList = step7(cellsList,consider)

#step:8 Each CH learns about its upstream CH and slot allotted for intercluster communication from the SCH message.
path = findQueryPath(cellsList)
print(path)

#step:10 Each cluster head will send TDMA schedule for its cluster members.
consider={ i: True for i in range(17) }
cellsList = step10(cellsList,consider)

#step:11 data transmission starts according ldc mac protocol
for num in range(20):
	cellsList=step11_a(cellsList)
	cellsList=step11_b(cellsList)
    #step 12: Each CH will send a response to its upstream 
	considerColumn={ i: True for i in range(1,5)}
	cellsList=step12(cellsList,considerColumn,path)
print('After Round 1:')
print(json.dumps(cellsList[1:],indent=4))
roundAxis=[]
numberOfDeadNodesAxis=[]
roundAxis.append(1)
numberOfDeadNodesAxis.append(findNumberOfDeadNodes(cellsList))
total_rounds=6000  # total number of rounds
for rounds in range(2,total_rounds):
	cellsList = step2(cellsList,consider)
	considerColumn={ i: False for i in range(1,5)}
	consider={ i: False for i in range(17) }
	cellsList = makeDead(cellsList)
	for i in range(len(cellsList)):
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isClusterHead']==True):
				consider[i]=True
				if(i%4==0):
					considerColumn[i%4+4]=True
				else:
					considerColumn[i%4]=True
				x,y=cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y']
				idx=cellsList[i][j]['id']
				print('CH dead! having ID:',idx)
				cellsList[i][j]['isClusterHead']=False
	cellsList = calculateClusterHead(cellsList,consider)
	for i in range(len(cellsList)):
		if(consider[i]==True):
			for j in range(len(cellsList[i])):
				if(cellsList[i][j]['isClusterHead']==True and cellsList[i][j]['energy']<cellsList[i][j]['threshold']):
					(x,y)=(cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y'])
					if(show_graphics==1):
						draw_vertex('green',x,y)
					idx=cellsList[i][j]['id']
					print('CH changed! having ID:',idx)
	for i in range(len(cellsList)):
		for j in range(len(cellsList[i])):
			if(cellsList[i][j]['isDead']==True):
				x,y=cellsList[i][j]['location']['x'],cellsList[i][j]['location']['y']
				if(show_graphics==1):
					draw_vertex('black',x,y)


	cellsList = step5(cellsList,consider)
	cellsList = step7(cellsList,consider)
	cellsList = step10(cellsList,consider)
	total_frame = 20
	consider={ i: True for i in range(17) }
	considerColumn={ i: True for i in range(1,5) }
	for num in range(total_frame):
		cellsList=step11_a(cellsList)
		cellsList=step11_b(cellsList)
		cellsList=step12(cellsList,considerColumn,path)
	print('After Round ',rounds)
	print(json.dumps(cellsList[1:],indent=4))
	roundAxis.append(rounds)
	numberOfDeadNodesAxis.append(findNumberOfDeadNodes(cellsList))

print(numberOfDeadNodesAxis)
file_name='output_mldc_mac200.txt'
with open(file_name,'w') as f:
	for i in roundAxis:
		f.write(str(i)+' ')
	f.write('\n')
	for i in numberOfDeadNodesAxis:
		f.write(str(i)+' ')
firstDeadRound = findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis)
print("Round at which the first node is dead is ",firstDeadRound)
roundAxis=roundAxis[0:5]+roundAxis[5::350]
numberOfDeadNodesAxis=numberOfDeadNodesAxis[0:5]+numberOfDeadNodesAxis[5::350]
roundAxis=np.asarray(roundAxis)
numberOfDeadNodesAxis=np.asarray(numberOfDeadNodesAxis)
roundAxis_new = np.linspace(roundAxis.min(), roundAxis.max(),8000)
numberOfDeadNodesAxis_smooth=spline(roundAxis,numberOfDeadNodesAxis,roundAxis_new)
plt.plot(roundAxis_new,numberOfDeadNodesAxis_smooth)
plt.xlabel('Number of rounds')
plt.ylabel('Number of Dead Nodes')
plt.title('Graph between dead nodes and rounds')
plt.show()
if(show_graphics==1):
	done()