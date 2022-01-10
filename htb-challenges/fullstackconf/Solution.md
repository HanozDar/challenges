# Solution for FullStackConf - Hackthebox - Challenges - Retired - Web

This box is also pretty straightforward. 
When we open the page, we see a sign up newsletter form
We see there is some text above that
![ Instruction for getting flag](https://github.com/HanozDar/challenges/blob/master/fullstackconf/images/instructions.png)

Now that we know that there is something simulating a stored XSS vulnerability, but it isn't being rendered on our page, we can easily get the flag with this payload!
![Payload for flag](https://github.com/HanozDar/challenges/blob/master/fullstackconf/images/payload.png)

Click sign up and you have flag!
