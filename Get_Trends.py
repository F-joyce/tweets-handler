from Get_Token_Reddit import headers
import requests
import json 

headers['limit'] = '100'

response = requests.get('https://oauth.reddit.com/r/all/comments/6uey5x', headers=headers)

data = response.json()

print(data)

def dump_in(namefile):
    with open(namefile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


