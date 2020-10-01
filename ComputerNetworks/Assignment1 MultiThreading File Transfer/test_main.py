import os
import builtins
import time
import subprocess
# os.system('python thread_example.py')
from main import *

filelist = [
            ('a_1GB.txt', 'a'*1000*1000*1000), # 1KB
            ('b_10MB.txt', 'b'*10*1000*1000), # 10MB
            ('c_100MB.txt', 'c'*100*1000*1000), # 100 MB
            ('d_1GB.txt', 'd'*1000*1000*1000), # 1GB
            ('e_1MB.txt', 'e'*1000*1000),  # 1MB
            ('f_365MB.txt', 'f'*365*1000*1000), # 365MB
        ]

def create_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def setUp():
    edit_log_file('w','') # Init Log File
    for filename, size in filelist:
        create_file(filename, size)
    
def tearDown():
    # Remove Test Data
    for filename, size in filelist:
        os.remove(filename)
        
    for filename, size in filelist:
        os.remove(f'copy_'+filename)

def test_main():
    user_inputs = []
    for filename, size in filelist:
        user_inputs.append((filename, 'copy_'+filename))
    # user_inputs.append('exit')

    # Input
    for input_file, new_file in user_inputs:
        create_worker(input_file, new_file)
        time.sleep(0.5)
    
    time.sleep(10)

    with open('log.txt','r') as f:
        results = f.read()
    
    print(results)

    # Accurancy Test
    for input_file, new_file in user_inputs:
        print("Check) {} --> {} ".format(input_file,new_file))
        with open(input_file,'r') as inputF, open(new_file,'r') as newF:
            assert inputF.read(1) == newF.read(1) # 내용 같은지 확인
            print('✔️ Input Content: {} == New Content: {}'.format(inputF.read(1),newF.read(1)))
        # Chekc File Size
        input_file_size = os.path.getsize(input_file)
        output_file_size = os.path.getsize(new_file)
        assert input_file_size == output_file_size
        print('✔️ Input Size: {} == New Size: {}'.format(input_file_size, output_file_size))
        print(); print('=='*30); print()


if __name__ == '__main__':
    setUp()
    test_main()
    tearDown()

