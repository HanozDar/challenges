import requests
import bs4
from bs4 import BeautifulSoup
import hashlib

session = requests.session()
req = session.get('http://167.99.89.198:32333/')

text = BeautifulSoup(req.text, 'html.parser')

#print(text)

question = text.find_all("h3")
problem = str(question[0])
to_hash = problem[19:39]

result = hashlib.md5(to_hash.encode()).hexdigest()

#print(final_result)

data_tosend = dict(hash=result)

flag = session.post('http://167.99.89.198:32333/',data_tosend)

print(flag.text)

'''
The challenge was pretty straightforward. Used beautifulsoup to get the string where the text that needed to be encoded was stored, converted to md5 and sent it back in a post request
'''
