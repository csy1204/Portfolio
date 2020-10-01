import threading
import time
import os

start_time = time.time()
global_lock = threading.Lock()
log_file = 'log.txt'
CHUNK_SIZE = 10*1000 # 10KB

def worker(input_file, output_file):
    """
    CHUNK_SIZE 단위로 파일 복사
    """
    # print("{} is start : {}".format(threading.currentThread().getName(), input_file))

    write_log(output_file, input_file)
    
    from_file = open(input_file, 'rb')
    to_file = open(output_file, 'ab')

    # 몇번 쪼개어 복사할지 결정
    chunk_time = os.path.getsize(input_file) // CHUNK_SIZE + 1
    
    while chunk_time:
        to_file.write(from_file.read(CHUNK_SIZE))
        chunk_time -= 1
    
    write_log(output_file)

    from_file.close()
    to_file.close()

    # print("{} is end: {}".format(threading.currentThread().getName(), output_file))

def create_worker(input_file, output_file):
    th = threading.Thread(target=worker, args=(input_file, output_file,))
    # th.setDaemon(True) # 백그라운드에서 돌리고 싶다면
    th.start()
    # th.join() # 프로그램 종료시 데몬 종류를 기다리게 하고 싶다면

def write_log(to_file, from_file=False):
    """
    log.txt 생성 및 작성
    - from_file_name 유무로 Complete 판단
    """
    log_msg = "{:<8.2f} | Start) [{}] ===> [{}] \n".format(time.time() - start_time, from_file, to_file) if from_file \
        else "{:<8.2f} | Complete) [{}] \n".format(time.time() - start_time, to_file)
    
    global_lock.acquire() # log file에 대한 Global Lock
    edit_log_file('a', log_msg)
    global_lock.release()

def edit_log_file(mode='a', msg=''):
    with open(log_file, mode) as f:
        f.write(msg)

def run():
    while True:
        input_file = input('Input the file name: ').strip()
        if input_file == 'exit':
            # Exit Condition
            break
        output_file = input('Input the new name: ').strip()
        create_worker(input_file, output_file)

if __name__ == "__main__":
    edit_log_file('w','') # Init Log File
    run()

