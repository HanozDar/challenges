# After using the hint, I got the idea that maybe it is not using the standard UTF-8 decoding because this isn't ascii, and it is using UTF 16. So I just stored the value in a string and sent it as incoded to UTF-16
flag = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸彥ㄴㅡて㝽"

print(flag.encode('utf-16-be'))
