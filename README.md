# MLDC-MAC-Protocol
A Multi-Hop Low Duty Cycle Medium Access Control (MLDC-MAC) protocol for Wireless Sensor Networks, assumes that the deployment area is composed of equal-sized grids. The sensor nodes that fall within a grid are considered to be the part of the same cluster. The base station appoints the node with the highest residual energy as the cluster head in each grid. The base station also establishes multi-hop paths for communicating with the cluster heads and broadcasts the schedule for inter-cluster communication in the network. After receiving this information, each cluster head broadcasts a schedule for intra-cluster communication within its cluster. When a cluster head receives data from the source nodes in its cluster, it computes the aggregate and sends it to the base station. The result shows that MLDC-MAC increases the network lifetime compared with Low Duty Cycle MAC (LDC-MAC) protocol and Bit-Map- Assisted MAC (BMA-MAC) protocol.

   The proposed model assumes that the deployment area is composed of n equal-sized grids. Sensor nodes lying in a grid are considered to be the part of the same cluster. All the sensor nodes are homogenous, stationary, and fitted with GPS devices that can be used to know their locations. It is assumed that each node in the deployment area can transmit to the BS directly. It is also assumed that all the nodes are time synchronized. This can be achieved by having the BS broadcast a synchronization pulse at the start of each round. The proposed model divides a round into two phases: Set-up Phase and Steady-state Phase.

   Simulation Parameters:
Deployment area             : 50x50 m2, 100x100 m2
Initial energy of node      : 5 joule
Energy transmission         : 50 nJ/bit
Idle Energy                 : 40 nJ/bit
Transmit amplifier Energy   : 100 pJ/bit/m2
Threshold Energy            : 0.1 Joule
Data/Schedule message size  : 500 Bytes
Control message size        : 20 Bytes
Number of frames in a round : 20
Number of CHs (C)           : 16, 25
Number of nodes (N)         : 100, 200
