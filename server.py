# coding:utf-8

from flask import Flask
from flask import render_template
from os import popen
import MySQLdb #没有的话yum装一下即可

app = Flask(__name__)

# 针对url做出响应
@app.route('/')
def index():
    result = 'click the button,execute the command'
    return render_template('index.html',content=result)

@app.route('/iostat')
@app.route('/iostat/<option>')
def iostat(option=''):
    ''' 查看IO状态，支持传参'''
    result = execute('iostat'+' '+option)
    return render_template('index.html',content=result)

@app.route('/uptime')
def uptime():
    ''' 查看当前开机时间，不支持传参'''
    result = execute('uptime')
    return render_template('index.html',content=result)

@app.route('/who')
def who():
    ''' 查看当前登录用户，不支持传参'''
    result = execute('who')
    return render_template('index.html',content=result)

@app.route('/db_db')
def db_db():
    '''查看数据库里有哪些用户'''
    sql = 'select host,db,user from db'
    result = select(sql)
    return render_template('index.html',content=result)

@app.route('/db_help')
def db_help():
    '''查看数据库里有哪些用户'''
    sql = 'select * from help_category'
    result = select(sql)
    return render_template('index.html',content=result)

# 依赖的包
def select(sql):
    '''查询一个sql语句'''
    conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mysql",charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    string = format_db_output(result)
    return string

def format_db_output(datas):
    keys = datas[0].keys()
    string = '<table class="table table-striped table-hover">'

    string += '<tr>'
    for key in keys:
        string += '<th>' +key +'</th>'
    string += '</tr>'

    for row in datas:
        string += '<tr>'
        for call in row.values():
            string += '<td>' +str(call) +'</td>'
        string += '</tr>'
    string += '</table>'

    return string
    
def execute(command):
    ''' 执行系统命令，并将命令的输出进行格式化'''
    result = popen(command).readlines()
    string = ''.join(result)
    string = format_os_output(string)
    return string

def format_os_output(string):
    return '<pre>' + string + '</pre>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
