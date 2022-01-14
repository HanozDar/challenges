import requests
import hashlib
import bs4
from bs4 import BeautifulSoup
import re

login = 'https://ringzer0ctf.com/login'
uname = '************' # <enter username here>
passwd = '********************' #<Enter password here>

session = requests.session()

loginData = dict(username=uname,password=passwd)
#print(loginData)

session.post(login,loginData)

req = session.get('https://ringzer0ctf.com/challenges/119')

# So earlier, I had solved this challenge with beautifulsoup. While I was getting some answer, it didn't seem like an accurate answer and I kept not getting the flag. 
# After a while I decided that it is what is causing my problems. I need to see how to raw request looks

# Now the problem here is that the resulting stuff we get is not of consistent size. It is sometimes smaller and sometimes larger. 

start = req.text.find('----- BEGIN MESSAGE -----<br />')
end = req.text.find('----- END MESSAGE -----<br />')

# I can iterate through to end message once I get the value?

message = req.text[start+41:end-3]

#print(message)

# Now I have the message after faffing around way too much. 

new_message = message.split("<br /><br />")
#print(new_message)

# Cool now I can just render stuff normally.

art_four = "&nbsp;x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;&nbsp;&nbsp;x"
art_two = "&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x&nbsp;<br />&nbsp;&nbsp;xx&nbsp;<br />&nbsp;x&nbsp;&nbsp;&nbsp;<br />xxxxx"
art_zero = "&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;"
art_one = "&nbsp;xx&nbsp;&nbsp;<br />x&nbsp;x&nbsp;&nbsp;<br />&nbsp;&nbsp;x&nbsp;&nbsp;<br />&nbsp;&nbsp;x&nbsp;&nbsp;<br />xxxxx"
art_three = "&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;xx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;"
art_five = "xxxxx<br />x&nbsp;&nbsp;&nbsp;&nbsp;<br />&nbsp;xxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;x<br />xxxxx<br />"

# Now an interesting thing about 5 is that it doesn't have a double br after it. So in our list, five is usually paired with one or two numbers. It renders as 5x or 55x or 555x etc. (5*x) -> RE
# This is the idea behind checking if 5 string is there. I know this isn't a perfect solution, but it works so I'm not complaining
final_ans = []
for i in new_message:
    if(art_five in i):
        final_ans.append('5')
    if(art_zero in i):
        final_ans.append('0')
    if(art_one in i):
        final_ans.append('1')
    if(art_two in i):
        final_ans.append('2')
    if(art_three in i):
        final_ans.append('3')
    if(art_four in i):
        final_ans.append('4')

final_ans_str = ''.join(final_ans)
print(final_ans_str,len(final_ans_str))
    
response_data = "https://ringzer0ctf.com/challenges/119/" + final_ans_str

flag_page = session.post(response_data)
start = (flag_page.text.find('FLAG-'))
print(flag_page.text[start:]) 

