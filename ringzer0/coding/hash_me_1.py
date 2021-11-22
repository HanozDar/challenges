import requests
import hashlib
import bs4
from bs4 import BeautifulSoup

login = 'https://ringzer0ctf.com/login'
uname = '*******' # <enter username here>
passwd = '*********************' #<Enter password here>

session = requests.session()


loginData = dict(username=uname,password=passwd)
#print(loginData)

session.post(login,loginData)

req = session.get('https://ringzer0ctf.com/challenges/13')

text = BeautifulSoup(req.text, 'html.parser')

q = text.find_all("div", class_="message")

q1 = str(q[0])[59:1083]

result = hashlib.sha512(q1.encode())

#print(result.hexdigest())
#print(q1)

response_data = "https://ringzer0ctf.com/challenges/13/" + str(result.hexdigest())
#print(response_data)

flag_page = session.post(response_data)

#print(flag_page.text)

'''
start = (flag_page.text.find('FLAG-'))
print(flag_page.text[start-50:])

print(flag_page.text[start:])
'''

text = BeautifulSoup(flag_page.text, 'html.parser')

q = text.find_all("div", class_="alert alert-info")
print(q)