# reannu123  
import socket
import hashlib
from time import sleep, time
import random

def compute_checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

"""
!PARAMS:
!	Change however you want
!	(but I think the timeLimit is close to the real ones)
"""
uniqueID = "UniqueID"       
payloadSize = 1612

minTimeLimit = 70							# Estimated parameter for the time limit of each payload based on many tested payloads
maxTimeLimit = 85							# Estimated parameter for the time limit of each payload based on many tested payloads
minPacketSize = 20							# Estimated parameter for the minimum size of each packet
maxPacketSize = 100							# Estimated parameter for the maximum size of each packet
TxnID = str(100).zfill(7)                   # Doesnt matter what this is


# Socket Object
serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSock.bind(('',9000))


packetSize = 1		# Placeholder: to be randomized in line 46
procTime = 1		# Placeholder: to be determined in line 48
ackNum = 0
start = 0
while True:
	message = ""
	data, addr = serverSock.recvfrom(1024)
	message = data.decode()
	end = time()
	print(end-start)
	MD5 = compute_checksum(message)

	if len(data) > 0:
		if message == f"ID{uniqueID}":
			serverSock.sendto(TxnID.encode(), addr)
			timeLimit = random.randint(minTimeLimit,maxTimeLimit)
			packetSize = random.randint(minPacketSize,maxPacketSize)			# Randomize packet size
			numOfPackets = int(payloadSize/packetSize)	# Calculate number of packets
			procTime = timeLimit/numOfPackets			# Determine processing time for each packet
			print("Packet Size: ", packetSize)
			print("Processing Time: ", procTime)
			ackNum = 0
			start = time()
			
		elif len(message) < 35 + packetSize and end-start<120:
			sleep(procTime)
			serverSock.sendto(f"ACK{str(ackNum).zfill(7)}TXN{str(0).zfill(7)}MD5{MD5}".encode(), addr)
			ackNum += 1
		else:
			pass
	