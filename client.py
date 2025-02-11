from flask import Flask,render_template,request,make_response,redirect
import requests
import json


app = Flask(__name__)

@app.route('/')
def mainpg():
    return render_template('index.html')

@app.route('/sign')
def tks():
    return render_template('neofp.html')


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
    return render_template('result.html',user=rest[0],msg="查找结果")

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
    return render_template('result.html',user=rest[0],msg="查找结果")

@app.route('/sign/add')
def add():
    return render_template('add.html')

@app.route('/sign/add_backend',methods=['POST'])
def add_be():
    usr = request.form.get("username")
    url = f"http://127.0.0.1:7788/add"
    form_data = {'username': usr}
    response = requests.post(url,data=form_data)
    rest = response.text
    rest = json.loads(rest)
    return render_template('result.html',user=rest,msg="添加结果")
    
@app.route('/sign/delete')
def delete():
    return render_template("delete.html")

@app.route('/sign/delete_backend',methods=['POST'])
def del_backend():
    try:
        uid = request.form.get('id')
        url = f"http://127.0.0.1:7788/remove"
        form_data = {'id': uid}
        response = requests.post(url,data=form_data)
        rest = response.text
        rest = json.loads(rest)
        msg="删除成功！"
    except Exception as e:
        msg = f"删除失败！原因：{e}，处理{response.text}时发生异常。"
    return render_template('result.html',user=None,msg=msg)

if __name__ == '__main__':
    app.run(port=7789)
