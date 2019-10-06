import requests, json, os, webbrowser
from datetime import datetime

# Find everything between A and B
# (?<=A)(.*)(?=B)-
def pgbr(prcnt, dn='█', rm='░', length=100, hint=''):
    # dn: done
    # rm: remaining
    d = int(prcnt * length)
    r = length - d
    print(f'\r{hint} |{dn*d}{rm*r}| {int(prcnt*100)}%', end='\r')

def gtall(name, d):
    # api only shows 100 messages in api
    # i noticed thay when i scroll page
    # there is a new requests for the api with parameter (max_timestamp)
    # which each message on api has one
    # so i get the last message time stamp (message number 100) and substract 1
    # so the next request can get the rest <= 100 messages without repeating the
    # last message from the previous request
    # when n equals the static property of answers numbers the code stops
    add = lambda x, y: [f'\n\n{n+y}:\nTime: {datetime.utcfromtimestamp(post["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")}\nMessage: {post["comment"]}\nReply: {post["reply"]}' for n, post in enumerate(x)]
    dct, n, last = {}, 0, 0
    with open(f'{name}\\answers.txt','a', encoding='utf-8') as db:
        db.write(f'Name: {d["username"]}\nAnswers: {d["answers"]}\nFollowers: {d["followers"]}\nFollowing: {d["following"]}\nTwitter: https://twitter.com/intent/user?user_id={d["userData"]["twitterid"]}')
        if not d['posts']:
            db.write('\n\n[No Messages _/(0_0)\_]')
            return
        while True:
            try:
                dct = json.loads(
                        requests.get(
                f'https://curiouscat.me/api/v2/profile?username={name}&count=100' + f'&max_timestamp={last}' * (last != 0)
                                    ).content.decode()
                        )
                db.write(''.join(add(dct['posts'], n + 1)))
                n += len(dct['posts'])
                pgbr(n/dct["answers"], hint='Answers fetched:')
                if not dct['posts']:
                    break
                last = dct['posts'][-1]['timestamp'] - 1
            except:
                db.write('\n\n[Unexpected Error]')
                break

def foloDetail(name, identifier):
    fls = json.loads(requests.get(f'https://curiouscat.me/api/v2/profile/{identifier}?username={name}').content.decode())
    with open(f'{name}\\{identifier}.txt','w') as fs:
        for fn, flwr in enumerate(fls['result']):
            fs.write(f'\n\n{fn+1}:\n{flwr["username"]}\nhttps://curiouscat.me/{flwr["username"]}')

def cc():
    name = input('Username: ')
    dct = json.loads(requests.get(f'https://curiouscat.me/api/v2/profile?username={name}').content.decode())
    if 'error' in dct:
        print("\nProfile doesn't exist!")
        return
    os.makedirs(f'{name}', exist_ok=True)
    foloDetail(name, 'followers')
    foloDetail(name, 'following')
    with open(f'{name}\\avatar.jpg','wb') as img:
        img.write(requests.get(dct['avatar']).content)
    open(f'{name}\\answers.txt','w', encoding='utf-8')
    gtall(name, dct)
    webbrowser.open(f'{name}\\')

os.makedirs('DATA', exist_ok=True)
os.chdir('DATA')
while True:
    try:
        os.system('CLS')
        cc()
        input('\nNext?')
    except KeyboardInterrupt:
        input('Why Ctrl+C? (-_-)')
