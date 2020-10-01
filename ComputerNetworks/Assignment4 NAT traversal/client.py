import sys
import time
import socket
import threading
import os

CLIENT_LIST_LOCK = threading.Lock()
CLIENT_LIST = {}
SERVER_PORT = 10080
CLIENT_PORT = 10081
serverIp = ''
clientId = ''
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

EXIT = False

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return addr_tuple_to_str((s.getsockname()[0], CLIENT_PORT))

def addr_tuple_to_str(addr):
    return "{}:{}".format(addr[0], addr[1])

def addr_str_to_tuplea(addr):
    ip_addr, port_num = addr.split(":")
    return (ip_addr, int(port_num))

def client_init():
    global SOCK, serverIp, clientId
    SOCK.bind(('',CLIENT_PORT))
    msg = "R{},{}".format(clientId, get_private_ip())
    # print(msg)
    SOCK.sendto(msg.encode(), (serverIp, SERVER_PORT))
    # print("Send!")

    reciver_thread = threading.Thread(target=receiver)
    reciver_thread.start()
    keep_thread = threading.Thread(target=send_keep_alive)
    keep_thread.start()

    return reciver_thread, keep_thread

    
def send_keep_alive():
    global EXIT, SOCK, serverIp, clientId
    msg_encode = "H{}".format(clientId).encode()
    while not EXIT:
        SOCK.sendto(msg_encode, (serverIp, SERVER_PORT))
        time.sleep(10)
    

def send_msg(toAddr, message):
    global clientId
    """
    Send Message to Other Client
    """
    # Extended Goal!
    private_addr_s = CLIENT_LIST.get(toAddr)[1]
    my_addr_s = CLIENT_LIST.get(clientId)[1]

    if check_same_nat(private_addr_s, my_addr_s):
        # In the same NAT
        target_ip = private_addr_s
    else:
        target_ip = CLIENT_LIST.get(toAddr)[0]
    
    msg = clientId + "|" + message
    # print("Chat) Send to ", target_ip)
    SOCK.sendto(msg.encode(),addr_str_to_tuplea(target_ip))

def check_same_nat(addr1, addr2):
    if addr1.split(".")[:3] == addr2.split(".")[:3]:
        return True
    return False



############################################################

def receiver():
    global EXIT, SOCK
    """
    Receive Messages from Other Clients and Server
    """
    SOCK.settimeout(3)
    while not EXIT:
        try:
            data, addr = SOCK.recvfrom(2048)
        except:
            continue
        data = data.decode()

        if addr[0] == serverIp and addr[1] == SERVER_PORT:
            # Server Msg
            parse_server_msg(data)
        else:
            # Client Msg
            parse_client_msg(data)


def parse_server_msg(data):
    """
    MSG Type:
        1. R
        2. U
    """
    flag = data[0]
    data = data[1:]
    # print("PARSE", flag, data)

    CLIENT_LIST_LOCK.acquire()

    if flag == 'R':
        # reegit
        for ip_info in data.split("|"):
            if not ip_info:
                continue
            _client_id, _ip, _private_ip = ip_info.split(",")
            CLIENT_LIST[_client_id] = (_ip, _private_ip)
            
    elif flag == 'U':
        #unregit
        client_id = data
        if CLIENT_LIST.get(client_id):
            del CLIENT_LIST[client_id]
    else:
        pass
    CLIENT_LIST_LOCK.release()
    # print(CLIENT_LIST)

def parse_client_msg(data):
    client, message = data.split("|")
    print("{}> {}".format(client, message))

def send_unreg():
    global SOCK
    SOCK.sendto(("U"+clientId).encode(), (serverIp, SERVER_PORT))
    # print("Send Unregister")


if __name__ =='__main__':
    clientId = input("Client ID>")
    serverIp = input("Server IP>")

    rThread, kThread = client_init()

    while True:
        input_text = input()
        command, *text = input_text.split(" ", 1)
        if command == "@show_list":
            CLIENT_LIST_LOCK.acquire()
            for cid, ipaddr in CLIENT_LIST.items():
                print("{} {} / {}".format(cid, ipaddr[0], ipaddr[1]))
            CLIENT_LIST_LOCK.release()
            
        elif command == "@chat":
            if text:
                toClient, *message = text[0].split(" ", 1)
                message = message[0] if message else ""
            
            send_msg(toClient, message)

        elif command == "@exit":
            # Exit
            send_unreg()
            EXIT = True
            SOCK.close()
            # sys.exit()
            # raise SystemExit
            break
        else:
            print("##### Wrong Command! Please Type Again. #####")

