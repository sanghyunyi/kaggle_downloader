# -*- coding: utf-8 -*-
import shutil
import requests
import sys
import getpass


sys.stdout.write("Download url: ")
sys.stdout.flush()
download_url = sys.stdin.readline()[:-1]

filename = download_url.split('/')[-1]

sys.stdout.write("UserName: ")
sys.stdout.flush()
usr_name = sys.stdin.readline()[:-1]

pwd = getpass.getpass("Password: ")

login_data = {'UserName': usr_name,
             'Password': pwd}

login_url = 'https://www.kaggle.com/account/login'

with requests.session() as s, open(filename, 'w') as f:
    s.post(login_url, data=login_data)
    response = s.get(download_url, stream=True)
    total_length = response.headers.get('content-length')
    if total_length is None:
        shutil.copyfileobj(response.raw, f)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 *dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()
