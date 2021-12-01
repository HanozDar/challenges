import requests
import hashlib
import bs4
from bs4 import BeautifulSoup

login = 'https://ringzer0ctf.com/login'
uname = '**********' # <enter username here>
passwd = '******************' #<Enter password here>

session = requests.session()


loginData = dict(username=uname,password=passwd)
#print(loginData)

session.post(login,loginData)

req = session.get('https://ringzer0ctf.com/challenges/32')

text = BeautifulSoup(req.text, 'html.parser')

q = text.find_all("div", class_="message")

num1 = int(str(q[0])[59:63])

num_arr = str(q[0]).split(' ')

num2_str = num_arr[6][2:]
num2 = int(num2_str,16)

num3_str = num_arr[8]
num3 = int(num3_str,2)

sum = num1+num2-num3

#print(num1,num2,num3,num_arr)

response_data = "https://ringzer0ctf.com/challenges/32/" + str(sum)

flag_page = session.post(response_data)

text = BeautifulSoup(flag_page.text, 'html.parser')

q = text.find_all("div", class_="alert alert-info")

#start = (flag_page.text.find('FLAG-'))

print(q)