# coding:utf-8

from flask import Flask
from flask import render_template
from os import popen

app = Flask(__name__)

@app.route('/')
def index():
    result = 'click the button,execute the command'
    return render_template('index.html',content=result)

@app.route('/iostat')
def iostat():
    result = execute('iostat')
    return render_template('index.html',content=result)

@app.route('/iostat-d')
def iostat_d():
    result = execute('iostat -d')
    return render_template('index.html',content=result)

@app.route('/iostat-c')
def iostat_c():
    result = execute('iostat -c')
    return render_template('index.html',content=result)

@app.route('/uptime')
def uptime():
    result = execute('uptime')
    return render_template('index.html',content=result)

@app.route('/who')
def who():
    result = execute('who')
    return render_template('index.html',content=result)

def execute(command):
    result = popen(command).readlines()
    string = ''.join(result)
    string = format(string)
    return string

def format(string):
    string = string.replace("\n","<br>");
    string = string.replace(" ","&nbsp;");
    return string

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
