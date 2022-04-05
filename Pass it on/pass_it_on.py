import subprocess
import time

# Execute name
exe_name="Pass_it_on.exe"

# Using a custom pritable for performence
PRINTABLE="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!()*+-=?@[]_{}"

# Open pipe to communicate with pass_it_on.exe
# Piping stdout and in, strerr to stdout
process = subprocess.Popen([exe_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
pin = process.stdin
pout = process.stdout

# Reading first row of :"Please enter your password to log in:\r\n" which is 39 bytes len
output=pout.read(39)
print(output)

# Sends a new message, return the response time
def sendMessage(message):
    pin.write(f"{message}\n".encode())
    pin.flush()
    start = time.time()
    output = pout.read(71) ## message is 71 bytes length
    next = time.time()
    diff = next - start
    return diff

# Global vars
flag_len=27
max_message="CSA"
max_time=0

# Performing a timing attack, each letter at a time
# If the response time is greater then max response time, append the current asci char to the password
for i in range(len(max_message),flag_len):
    for c in PRINTABLE:
        message=max_message[:i] + c + "a"*(flag_len-i-1)
        diff=sendMessage(message)
        if diff>max_time:
            if diff==None:
                continue
            max_time=diff
            max_message=message
    message=max_message
    print(max_message,i)

print(max_message)
