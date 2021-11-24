import requests
import hashlib
import bs4
from bs4 import BeautifulSoup
import binascii

login = 'https://ringzer0ctf.com/login'
uname = '*********' # <enter username here>
passwd = '***************' #<Enter password here>

session = requests.session()


loginData = dict(username=uname,password=passwd)
#print(loginData)

session.post(login,loginData)

req = session.get('https://ringzer0ctf.com/challenges/14')

text = BeautifulSoup(req.text, 'html.parser')

q = text.find_all("div", class_="message")

q1 = str(q[0])[59:]

quest = q1.split('<')

binary_input = quest[0]

int_ip = int(binary_input,2)

output = binascii.unhexlify('%x' % int_ip)

result = hashlib.sha512(output)
print(result.hexdigest())

response_data = "https://ringzer0ctf.com/challenges/14/" + str(result.hexdigest())

flag_page = session.post(response_data)

text = BeautifulSoup(flag_page.text, 'html.parser')

q = text.find_all("div", class_="alert alert-info")

#start = (flag_page.text.find('FLAG-'))

print(q)