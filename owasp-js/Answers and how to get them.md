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

# 04 Reading the Privacy Policy
This was a challenge similar to finding the scoreboard, we find a link with 
/privacy-security.
So we find the Privacy Policy in there and when we click on it, the challenge will appear solved.
```text
http://192.168.24.143:3000/#/privacy-security/privacy-policy
```

# 05 XSS Tier 1
Here, we simply find forms where we can input data. We see there is a search bar at the top of the page, so we go there and we input the parameter needed to get reflected XSS

![XSS Tier 1](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/xss-tier-1.png)

Hence, the challenge is marked solved

# 06 Redirects Tier 1
We need to find a link that is redirecting us to another website. After scouring the website, I found something interesting in main.js
![Redirect crypto wallet](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/redirect-crypto-wallet.png)

Now, lets go there
And the challenge is marked as solved!

# 07 0-star Feedback

