import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import spline
import matplotlib.patches as mpatches

def findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind=0
	for i in range(len(roundAxis)):
		if(numberOfDeadNodesAxis[i]>=1):
			ind = i
			break
	return ind

def findLastDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind = 0
	for i in range(len(roundAxis)-1,0,-1):
		if(numberOfDeadNodesAxis[i]<200):
			ind = i
			break
	return ind+1

listt_1=[]
file_ = 'output_ldc_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_1.append(line)

listt_2=[]
file_ = 'output_mldc_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_2.append(line)

listt_3=[]
file_ = 'output_bma_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_3.append(line)

roundAxis_3 = list(map(int,listt_3[0].strip().split(' ')))
numberOfDeadNodesAxis_3 = list(map(int,listt_3[1].strip().split(' ')))
firstDeadNodeRound_3 = findFirstDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
lastDeadNodeRound_3 = findLastDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
roundAxis_3=roundAxis_3[0:firstDeadNodeRound_3//2]+roundAxis_3[firstDeadNodeRound_3//2:5000:30]
numberOfDeadNodesAxis_3=numberOfDeadNodesAxis_3[0:firstDeadNodeRound_3//2]+numberOfDeadNodesAxis_3[firstDeadNodeRound_3//2:5000:30]
roundAxis_3=np.asarray(roundAxis_3)
numberOfDeadNodesAxis_3=np.asarray(numberOfDeadNodesAxis_3)
roundAxis_new_3 = np.linspace(roundAxis_3.min(), roundAxis_3.max(),60000)
numberOfDeadNodesAxis_smooth_3=spline(roundAxis_3,numberOfDeadNodesAxis_3,roundAxis_new_3)
plt.text(firstDeadNodeRound_3, -10, firstDeadNodeRound_3,fontsize=16)
plt.text(lastDeadNodeRound_3, 190, lastDeadNodeRound_3,fontsize=16)
plt.plot(roundAxis_new_3,numberOfDeadNodesAxis_smooth_3,'g',label='BMA-MAC',linewidth=2.5)

roundAxis_1 = list(map(int,listt_1[0].strip().split(' ')))
numberOfDeadNodesAxis_1 = list(map(int,listt_1[1].strip().split(' ')))
firstDeadNodeRound_1 = findFirstDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
lastDeadNodeRound_1 = findLastDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
roundAxis_1=roundAxis_1[0:firstDeadNodeRound_1//2:30]+roundAxis_1[firstDeadNodeRound_1//2:5000:50]
numberOfDeadNodesAxis_1=numberOfDeadNodesAxis_1[0:firstDeadNodeRound_1//2:30]+numberOfDeadNodesAxis_1[firstDeadNodeRound_1//2:5000:50]
roundAxis_1=np.asarray(roundAxis_1)
numberOfDeadNodesAxis_1=np.asarray(numberOfDeadNodesAxis_1)
roundAxis_new_1 = np.linspace(roundAxis_1.min(), roundAxis_1.max(),60000)
numberOfDeadNodesAxis_smooth_1=spline(roundAxis_1,numberOfDeadNodesAxis_1,roundAxis_new_1)
plt.text(firstDeadNodeRound_1+50, 5, firstDeadNodeRound_1,fontsize=16)
plt.text(lastDeadNodeRound_1, 205, lastDeadNodeRound_1,fontsize=16)
plt.plot(roundAxis_new_1,numberOfDeadNodesAxis_smooth_1,'b',label='LDC-MAC',linewidth=2.5)

roundAxis_2 = list(map(int,listt_2[0].strip().split(' ')))
numberOfDeadNodesAxis_2 = list(map(int,listt_2[1].strip().split(' ')))
firstDeadNodeRound_2 = findFirstDeadNodeRound(roundAxis_2,numberOfDeadNodesAxis_2)
lastDeadNodeRound_2 = findLastDeadNodeRound(roundAxis_2,numberOfDeadNodesAxis_2)
roundAxis_2=roundAxis_2[0:firstDeadNodeRound_2//2]+roundAxis_2[firstDeadNodeRound_2//2:5000:200]
numberOfDeadNodesAxis_2=numberOfDeadNodesAxis_2[0:firstDeadNodeRound_2//2]+numberOfDeadNodesAxis_2[firstDeadNodeRound_2//2:5000:200]
roundAxis_2=np.asarray(roundAxis_2)
numberOfDeadNodesAxis_2=np.asarray(numberOfDeadNodesAxis_2)
roundAxis_new_2 = np.linspace(roundAxis_2.min(), roundAxis_2.max(),60000)
numberOfDeadNodesAxis_smooth_2=spline(roundAxis_2,numberOfDeadNodesAxis_2,roundAxis_new_2)
plt.text(firstDeadNodeRound_2+100, -5, firstDeadNodeRound_2,fontsize=16)
plt.text(lastDeadNodeRound_2+100, 195, lastDeadNodeRound_2,fontsize=16)
plt.plot(roundAxis_new_2,numberOfDeadNodesAxis_smooth_2,'r',label='MLDC-MAC',linewidth=2.5)

plt.xlabel('Number of rounds',fontsize=15)
plt.ylabel('Number of Dead Nodes',fontsize=15)
plt.legend(loc="upper left",fontsize=15,numpoints=1)
plt.show()