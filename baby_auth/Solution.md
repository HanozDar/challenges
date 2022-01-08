# Solution for HacktheBox Challenge - Web - Retired - Baby Auth

This challenge was pretty straightforward
After trying several injections, both SQL and LDAP for an unreasonable amount of time, I saw there is a register button at the bottom
So I registered with the credentials
```text
admin1:1234
```
Now I logged in, and I see this message
```text
You are not an admin
```

Okay, rude.
So I'm going to try and see what data I can deal with
When I open cookies, I see this in PHPSESSID
```text
eyJ1c2VybmFtZSI6ImFkbWluMSJ9
```
Maybe its something I can decode?
It's base64 lol
```text
{"username":"admin1"}
```

Swimming, I can just change this to admin and base64 encode it again
```text
eyJ1c2VybmFtZSI6ImFkbWluIn0=
```

Cool, now I'll paste this as a new cookie value in Cookie Editor (tool on firefox) and refresh the page

And we have the flag!
