# Creating an account and registering
Credentials used 
```text
username: abc@abc.com
password: abcdef
```
Emails harvested
```text
admin@juice-sh.op
bender@juice-sh.op
jim@juice-sh.op
```

# 01 Finding the score board
To find the score board, we can inspect the links of the page and we see that /score-board isn't linked yet. With this, when we visit 
http://IP_ADDRESS/score-board, we can solve the challenge
![Score Board](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/score-board.png)

# 02 Finding a confidencial Document
To find a confidential document, we go to the Terms and Conditions in the about page. There, while reading the source code we see an interesting link.
![Finding Document](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/finding-document-1.png)
Here we see an interesting link to download the ToS, /ftp. So we visit the site
This is what we get. 
![Finding Document 2](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/finding-document-2.png)
Here, we see an acquisitions.md file and when we open it, we see this line 
```text
┌──(hanoz㉿kali)-[~/…/htb/challenges/owasp-js/images]
└─$ cat acquisitions.md            
# Planned Acquisitions

> This document is confidential! Do not distribute!
```
Thus, we have found it!

# 03 Finding an Instance of Improper error handling

When in /ftp, we see some other documents too, like gg files, bak files and yaml files. When we try to open these files, we see the following error. 
![Improper Error Handling](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/improper-error-handling.png)

Here, it is just directly outputting the Node error, rather than sanitizing it, revealing some potentially dangerous information. 
Thus, this challenge is completed. 

