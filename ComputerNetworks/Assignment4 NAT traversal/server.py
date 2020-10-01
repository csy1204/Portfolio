import sys
import time
import socket
import threading

CLIENT_DICT_LOCK = threading.Lock()
global CLIENT_DICT
CLIENT_DICT = {}
TIMEOUT_SEC = 30

CLIENT_TIME_LOCK = threading.Lock()
CLIENT_TIME_DICT = {}

SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def addr_tuple_to_str(addr):
    return "{}:{}".format(addr[0], addr[1])

def addr_str_to_tuple(addr):
    ip_addr, port_num = addr.split(":")
    return (ip_addr, int(port_num))


def receiver():
    global SOCK
    while True:
        try:
            data, addr = SOCK.recvfrom(1024)
            # print(data.decode('utf-8'))
            # print(addr)
            broker(data.decode('utf-8'), addr_tuple_to_str(addr))

        except:
            pass

def broker(data, public_ip_s):
    global CLIENT_DICT
    """
    MSG Type:
        1. R egister
        2. U nregister
        3. H eartbeat
    """
    flag = data[0]
    data = data[1:]
    # print(flag, data)

    if flag == 'R':
        _client_id, _private_ip_s = data.split(",")
        new_client = "{},{},{}".format(_client_id,public_ip_s,_private_ip_s)
        send_all(new_client)
        # print("Send All!")
        CLIENT_DICT_LOCK.acquire()
        CLIENT_DICT[_client_id] = (public_ip_s, _private_ip_s)
        CLIENT_DICT_LOCK.release()
        # print("INSERT!", _client_id, )
        print("{} {} / {}".format(_client_id, CLIENT_DICT[_client_id][0], CLIENT_DICT[_client_id][1]))
        send_msg(public_ip_s) # send all client info to register client

    elif flag == 'U':
        print("{} is unregistered   {}".format(data, CLIENT_DICT[data][0]))
        
        CLIENT_DICT_LOCK.acquire()
        del CLIENT_DICT[data]
        CLIENT_DICT_LOCK.release()

        CLIENT_TIME_LOCK.acquire()
        del CLIENT_TIME_DICT[data]
        CLIENT_TIME_LOCK.release()

        send_all(data, context="U")

    elif flag == 'H':
        CLIENT_TIME_LOCK.acquire()
        CLIENT_TIME_DICT[data] = time.time()
        CLIENT_TIME_LOCK.release()
        
    else:
        pass

    # print(CLIENT_DICT)

def generate_all_client_info():
    CLIENT_DICT_LOCK.acquire()
    info = "|".join([
        "{},{},{}".format(cid, addrs[0], addrs[1])
        for cid, addrs in CLIENT_DICT.items()
    ])
    CLIENT_DICT_LOCK.release()
    return info


def send_all(msg, context="R"):
    for cid in CLIENT_DICT.keys():
        send_msg(cid, msg, context)
    


def send_msg(toClient, info=False, context="R"):
    """
    toClient = ClientId
    Context = [R, U]
    """
    global SOCK

    if context=="R" and info:
        # new register
        # info = "clientid,pubIP,privateIP"
        msg = "R" + info

    elif context=="U" and info:
        # unregit
        # info = "CLIENTID"
        msg = "U" + info 

    elif context == "R" and not info:
        # send all
        info = generate_all_client_info()
        msg = "R" + info
    
    to_addr = addr_str_to_tuple(CLIENT_DICT.get(toClient)[0]) if CLIENT_DICT.get(toClient) else addr_str_to_tuple(toClient)
    # print("SENDMSG", to_addr, msg)
    SOCK.sendto(msg.encode(), to_addr)


def checkTimeout():
    # print(CLIENT_TIME_DICT)

    timeout_client = [
        client_id
        for client_id, alive_time in CLIENT_TIME_DICT.items()
        if (time.time() - alive_time) > TIMEOUT_SEC
    ]
    
    for client_id in timeout_client:
        if CLIENT_DICT.get(client_id):
            print(client_id, "is Off-line   ", CLIENT_DICT.get(client_id)[0])
            CLIENT_DICT_LOCK.acquire()
            del CLIENT_DICT[client_id]
            CLIENT_DICT_LOCK.release()
        
        if CLIENT_TIME_DICT.get(client_id):
            CLIENT_TIME_LOCK.acquire()
            del CLIENT_TIME_DICT[client_id]
            CLIENT_TIME_LOCK.release()
        
        send_all(client_id, context="U")
    

if __name__ == '__main__':
    SOCK.bind(('', 10080))
    # SOCK.settimeout(5)

    rec_thread = threading.Thread(target=receiver)
    rec_thread.start()
    # print("checkTimeout!!")
    while True:
        checkTimeout()
        time.sleep(1) 

