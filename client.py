from flask import Flask,render_template,request,make_response,redirect
import requests
import json


app = Flask(__name__)

@app.route('/')
def mainpg():
    return render_template('index.html')

@app.route('/sign')
def tks():
    return render_template('fp.html')


@app.route('/sign/list')
def listall():
    url = "http://127.0.0.1:7788/list"
    response = requests.post(url,data=None)
    ul = json.loads(response.text)
    return render_template('list_all.html',users=ul)

@app.route("/sign/sbu/",methods=["POST"])
def sbu():
    un = request.form.get('username')
    url = f"http://127.0.0.1:7788/search/username/{un}"
    res = requests.get(url)
    rest = f"[{res.text}]"
    print(rest)
    if rest == "None":
        rest = None
    else:
        rest = json.loads(rest)
    return render_template('result.html',user=rest[0])

@app.route("/sign/sbi/",methods=["POST"])
def sbi():
    un = request.form.get('id')
    url = f"http://127.0.0.1:7788/search/id/{un}"
    res = requests.get(url)
    rest = f"[{res.text}]"
    print(rest)
    if rest == "None":
        rest = None
    else:
        rest = json.loads(rest)
    return render_template('result.html',user=rest[0])

if __name__ == '__main__':
    app.run(port=7789)
