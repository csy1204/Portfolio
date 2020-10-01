import sys
import time
import socket
import threading

MAX_SIZE = 4 + 3 + 1400 # Header + DATA
startTime = 0

def make_packet(seq, fin, data):
    seq_byte = seq.to_bytes(4, byteorder='big')
    fin_byte = fin.to_bytes(1, byteorder='big')
    return seq_byte + fin_byte + data

def parse_packet(packet):
    seq = int.from_bytes(packet[:4], byteorder='big')
    fin = int.from_bytes(packet[4:5], byteorder='big')
    data = packet[5:]
    return seq, fin, data

"Use this method to write Packet log"
def writePkt(logFile, pktNum, event):
    global startTime
    procTime = time.time() - startTime
    logFile.write('{:1.3f} pkt: {} | {}\n'.format(procTime, pktNum, event))

"Use this method to write ACK log"
def writeAck(logFile, ackNum, event):
    global startTime
    procTime = time.time() - startTime
    logFile.write('{:1.3f} ACK: {} | {}\n'.format(procTime, ackNum, event))

"Use this method to write final throughput log"
def writeEnd(logFile, throughput):
    logFile.write('\nFile transfer is finished.\n')
    logFile.write('Throughput : {:.2f} pkts/sec\n'.format(throughput))


def max_cum_ack(seq, seq_nums):
    for i in range(seq, 100000):
        if seq_nums[i] == 0:
            return i-1


def log_file_init(filename):
    return open(filename + '_receiving_log.txt' , 'w')

def fileReceiver():
    global startTime
    # print('receiver program starts...')

    port = 10080
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", int(port)))

    buffers = {}
    seq_nums = [0] * 100000
    cumAck = -1

    dest_filename = ''
    logFile = None
    startFlag = True
    finFlag = False
    last_seq = 100000

    while True:
        packet, cAddr = sock.recvfrom(MAX_SIZE)

        if startFlag:
            startTime = time.time()
            startFlag = False

        seq, fin, data = parse_packet(packet)
        # print("Seq ", seq, fin)

        if seq == 0:
            dest_filename = data.decode('utf-8')
            logFile = log_file_init(dest_filename)
        else:
            buffers[seq] = data
        
        writePkt(logFile, seq, "received")
        
        seq_nums[seq] = 1

        if seq - cumAck == 1:
            cumAck = max_cum_ack(seq, seq_nums)
        
        ack_packet = make_packet(cumAck,0,b'')
        sock.sendto(ack_packet,cAddr)
        writeAck(logFile, cumAck, "sent")
        
        if fin:
            last_seq = seq
            finFlag = True
            if last_seq+1 == sum(seq_nums[:last_seq+1]):
                break
            # fin은 왔는데 아직 다 안도착한 경우
            continue
            
        if finFlag and last_seq+1 == sum(seq_nums[:last_seq+1]):
            break
        
    sock.close()
    writeEnd(logFile,  (last_seq + 1) / (time.time() - startTime))
    
    # print("Received : ", time.time() - startTime)
    # print("!!", buffers.get(last_seq))
    with open(dest_filename, 'wb') as dest_file:
        for i in range(1, last_seq+1):
            dest_file.write(buffers.get(i))



if __name__=='__main__':
    fileReceiver()
