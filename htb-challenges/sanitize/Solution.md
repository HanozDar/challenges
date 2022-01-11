# Solution for HTB - Challenges - Web - Retired - Sanitize

The title of this challenge is SQLi
So that's kinda what we have to do, pretty easy

When we view /debug we can see that there's a straightforward SQL query

Even when we try to put normal credentials, we get the query echo'd back to us

Trying admin:admin
We get a meme
![Meme](https://github.com/HanozDar/challenges/blob/master/sanitize/images/meme.png)

We also see thq query echoed at the bottom

![Query echo](https://github.com/HanozDar/challenges/blob/master/htb-challenges/sanitize/images/query_at_bottom.png)


Now if we send this payload
```text
'or 1=1;--
```

The flag is sent to us

