from flask import Flask,render_template,request,make_response,redirect
import requests
import json

DEBUG_MODE = True

def dbugmsg(msg):
    if DEBUG_MODE:
        return msg
    else:
        return "可能发生了异常。请联系系统管理员开启调试模式。"

app = Flask(__name__)

@app.route('/')
def mainpg():
    return render_template('index.html')

@app.route('/sign')
def tks():
    try:
        url = "http://127.0.0.1:7788/list"
        response = requests.post(url,data=None)
        ul = json.loads(response.text)
        return render_template('neofp.html',number=ul[-1]["id"])
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))


@app.route('/sign/list')
def listall():
    try:
        url = "http://127.0.0.1:7788/list"
        response = requests.post(url,data=None)
        ul = json.loads(response.text)
        return render_template('list_all.html',users=ul)
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))

@app.route("/sign/sbu/",methods=["POST"])
def sbu():
    try:
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
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))

@app.route("/sign/sbi/",methods=["POST"])
def sbi():
    try:
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
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))

@app.route('/sign/add')
def add():
    return render_template('add.html')

@app.route('/sign/add_backend',methods=['POST'])
def add_be():
    try:
        usr = request.form.get("username")
        url = f"http://127.0.0.1:7788/add"
        form_data = {'username': usr}
        response = requests.post(url,data=form_data)
        rest = response.text
        rest = json.loads(rest)
        return render_template('result.html',user=rest,msg="添加结果")
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))
    
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
        msg = dbugmsg(f"删除失败！原因：{e}，处理相关数据时发生异常。")
    return render_template('result.html',user=None,msg=msg)

@app.route('/check')
def check_mpg():
    try:
        url = "http://127.0.0.1:7788/list"
        response = requests.post(url,data=None)
        ul = json.loads(response.text)
        bnum=ul[-1]["id"]
        url = f"http://127.0.0.1:7788/getnum/1"
        response = requests.get(url)
        ul = json.loads(response.text)
        cnum = ul[0]['numbers']
        url = f"http://127.0.0.1:7788/getnum/2"
        response = requests.get(url)
        ul = json.loads(response.text)
        nnum = ul[0]['numbers']
        arate = cnum/bnum * 100
        return render_template('check_mp.html',bnum=bnum,cnum=cnum,nnum=nnum,arate=arate)
    except Exception as e:
        return render_template('result.html',user=None,msg=dbugmsg(f"操作失败，发生了{e}"))

if __name__ == '__main__':
    app.run(port=7789)
