import sys
import time
# from socket import *
import socket
import threading
# from .utils import *

startTime = time.time()
CHUNK_SIZE = 1400
serverInfo = ''
SOCK = ''
logFile = ''
TIMEOUT_VALUE = 1

packetTimeDict = {}
# {seq: [출발 시간, timeout_value]}

def make_packet(_packet_raw):
    seq, fin, data = _packet_raw
    seq_byte = seq.to_bytes(4, byteorder='big')
    fin_byte = fin.to_bytes(1, byteorder='big')
    return seq_byte + fin_byte + data

def parse_packet(packet):
    seq = int.from_bytes(packet[:4], byteorder='big')
    fin = int.from_bytes(packet[4:5], byteorder='big')
    data = packet[5:]
    return seq, fin, data

# "Use this method to write Packet log"
def writePkt(pktNum, event):
    global startTime
    global logFile
    procTime = time.time() - startTime
    logFile.write('{:1.3f} pkt: {} | {}\n'.format(procTime, pktNum, event))

# "Use this method to write ACK log"
def writeAck(ackNum, event):
    global startTime
    global logFile
    procTime = time.time() - startTime
    logFile.write('{:1.3f} ACK: {} | {}\n'.format(procTime, ackNum, event))

# "Use this method to write final throughput log"
def writeEnd(throughput, avgRTT):
    global logFile
    logFile.write('\nFile transfer is finished.\n')
    logFile.write('Throughput : {:.2f} pkts/sec\n'.format(throughput))
    logFile.write('Average RTT : {:.1f} ms\n'.format(avgRTT*1000))

def get_file_chunks(filename):
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk
    

def sent_as_window(packets, windowSize, offset=0):
    for pkt in packets[offset:offset + windowSize]:
        send_packet(pkt)


def send_packet(packet, context='sent'):
    global serverInfo, startTime, packetTimeDict, TIMEOUT_VALUE
    global SOCK

    seq, fin, _ = packet
    SOCK.sendto(make_packet(packet), serverInfo)
    # print("{}) SEND! SEQ: {} FIN: {}".format(context, seq, fin))

    # write log by context
    # if context == 'sent':
    packetTimeDict[seq] = [time.time(), TIMEOUT_VALUE]
    writePkt(seq, context)


def calculate_rtt(samplertt, avgRtt, devrtt):
    alpha = 0.125
    beta = 0.25
    avgRtt = (1-alpha) * avgRtt + (alpha * samplertt)
    devrtt = (1-beta) * devrtt + beta * abs(samplertt - avgRtt)
    return avgRtt, devrtt



def get_recieved_pkt():
    global SOCK
    packet, serverAddress = SOCK.recvfrom(1024)
    ack, _, _, = parse_packet(packet)
    # print("ACK ", ack)
    writeAck(ack, "received")
    return ack




def fileSender(serverIP, windowSize, srcFilename, dstFilename):
    global serverInfo, TIMEOUT_VALUE, startTime
    global SOCK

    serverPort = 10080
    serverInfo = (serverIP, serverPort)
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # windowSize
    file_read_start = time.time()

    packets = []
    packets.append([0, 0, dstFilename.encode()])

    packets.extend([
        [i+1, 0, chunk]
        for i, chunk in 
        enumerate(get_file_chunks(srcFilename))
    ])

    packets[-1][1] = 1
    # print("Packet Ready :", time.time() - file_read_start)
    
    prevAck = -1
    nextSeq = windowSize
    ackDupCount = 0
    max_packets = len(packets) - 1

    alpha = 0.125
    beta = 0.25
    avgRtt = 1
    devrtt = 0
    

    # ack_received = True


    SOCK.settimeout(1)

    startTime = time.time()
    sent_as_window(packets, windowSize)
    dup_flag = False  
    
    while prevAck < max_packets:
        # check timeout packet
        seq_timeout = checkTimeout()

        if seq_timeout:
            # print("Timeout!", seq_timeout)
            send_packet(packets[seq_timeout], "retransmitted")
            continue

        try:
            ack = get_recieved_pkt()
        except:
            continue
        # cumAck 확인

        
        if ack > prevAck:
            # 이전 ack와 같지 않은 경우 
            # 이전 ack보다 큰 경우
            prevAck = ack
            start, _ = packetTimeDict.get(ack)
            samplertt = time.time() - start
            avgRtt, devrtt = calculate_rtt(samplertt, avgRtt, devrtt)
            TIMEOUT_VALUE = avgRtt + 4 * devrtt
            # print("SET TIMEOUT", TIMEOUT_VALUE)
            SOCK.settimeout(TIMEOUT_VALUE)
            ackDupCount = 0

            if nextSeq <= max_packets:
                # print("transfer", nextSeq)
                send_packet(packets[nextSeq])
                nextSeq += 1
        elif prevAck == ack:
            # 이전 ack랑 같은 경우 (중복)
            ackDupCount += 1
        else:
            # 이전 ack 보다 작은 경우
            # 일단 무시
            pass
        
        seq_arr = []
        for kseq, vals in packetTimeDict.items():
            if kseq <= ack:
                seq_arr.append(kseq)
        
        for dseq in seq_arr:
            del packetTimeDict[dseq]
        
        if ackDupCount == 3:
            # print("Duplicate!", ack)
            writePkt(ack, "3 duplicated ACKs")
            send_packet(packets[ack+1], "retransmitted")
            # print("retransmitted")
            while True:
                # seq_timeout = checkTimeout()

                # if seq_timeout:
                    # print("loop Timeout!", seq_timeout)
                #     send_packet(packets[seq_timeout])
                #     continue
                try:
                    ack = get_recieved_pkt()
                except:
                    send_packet(packets[ack+1], "retransmitted")
                    continue
                
                if ack > prevAck:
                    prevAck = ack
                    start, _ = packetTimeDict.get(ack)
                    samplertt = time.time() - start
                    avgRtt, devrtt = calculate_rtt(samplertt, avgRtt, devrtt)
                    TIMEOUT_VALUE = avgRtt + 4 * devrtt
                    # print("loop SET TIMEOUT", TIMEOUT_VALUE)
                    SOCK.settimeout(TIMEOUT_VALUE)

                    seq_arr = []
                    for kseq, vals in packetTimeDict.items():
                        if kseq <= ack:
                            seq_arr.append(kseq)
                    
                    for dseq in seq_arr:
                        del packetTimeDict[dseq]

                    ackDupCount = 0
                    sent_as_window(packets, windowSize, offset=ack+1)
                    nextSeq = ack + windowSize + 1
                    break

                else:
                    # send_packet(packets[ack+1], "retransmitted")
                    continue
            
        
            
    writeEnd((prevAck + 1) / (time.time() - startTime), avgRtt)
    # print("End")
    SOCK.close()


def checkTimeout():
    global packetTimeDict, startTime
    for seq, vals in packetTimeDict.items():
        if time.time() > (vals[-1] + vals[0]):
            # timeout!
            writePkt(seq, "timeout since {:1.3f}(timeout value {:1.3f})".format(vals[0]-startTime, vals[-1]))
            # print("timeout since {:1.3f}(timeout value {:1.3f})".format(vals[0]-startTime, vals[-1]))
            return seq
    return False
    



def log_file_init(filename):
    return open(filename + '_sending_log.txt' , 'w')

if __name__=='__main__':
    recvAddr = sys.argv[1]  #receiver IP address
    windowSize = int(sys.argv[2])   #window size
    srcFilename = sys.argv[3]   #source file name
    dstFilename = sys.argv[4]   #result file name

    logFile = log_file_init(srcFilename)
    fileSender(recvAddr, windowSize, srcFilename, dstFilename)