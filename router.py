import json
from flask import Flask, redirect, request

app = Flask('__name__')

url = 'http://64.226.78.151:'

f_en = open('enpoints.json')
f_us = open('users.json')

data = f_en.read()
data = json.loads(data)
users = f_us.read()
users = json.loads(users)

@app.route('/', defaults = {'path':''})
@app.route('/<path:path>')
def get(path):
    if path in data: 
        enpoint = data[path]['enpoint']
        necessary_per = data[path]['permissions']
        print(necessary_per)
        if (necessary_per != []):
            bearer = (request.headers).get('Authorization')
            token = bearer.split()[1]
            if token in users['token']: 
                user_per = users['permissions']
                check =  all(item in user_per for item in necessary_per)
                if check:
                    return redirect(url + enpoint, code=302)
                else: 
                    return 'unauthorized', 401
            else:
                return 'Invalid token', 498
        else:
            return redirect(url + enpoint, code=302)
    else:
        return 'Page does not exist', 404
    
f_en.close()
f_us.close()

if __name__ == '__main__' :
    app.run()



