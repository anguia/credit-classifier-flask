#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, flash
from flask import render_template
from flask import redirect, url_for
from flask import request, session
from flask import make_response
from flask import g, abort
from wtforms import Form, validators
from wtforms import BooleanField, RadioField, StringField, SubmitField
import time
import subprocess

app = Flask(__name__)

app.secret_key = '123456'

class InvalidUsage(Exception):
    status_code = 400
 
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
    
class CreditForm(Form):
    #1.checking_account_status = StringField('支票账户状态', default='A14', validators=[optional()])
    duration = StringField(u'账号持续月数', default=36,  validators=[Length(min=1, max=72)])
    #duration = StringField('账号持续月数', validators=[Length(min=1, max=72)])

    credit_history = RadioField(u'以往信用记录', default='A30', choices=[
                        ('A30',u'准时还款'),
                        ('A31',u'本行内准时还款'),
                        ('A32',u'所有信用贷款已还清'),
                        ('A33',u'存在延期还款记录'),
                        ('A34',u'危机账户')])
                        
    #4.purpose = StringField('贷款用途', default='A43', validators=[DataRequired()])
    credit_amount = StringField(u'信用贷款额度', default=300, validators=[Length(min=200, max=2000)])
    saving_account = RadioField(u'存款', default='A63', choices=[
                        ('A61',u'小于100'),
                        ('A62',u'100~500'),
                        ('A63',u'500~1000'),
                        ('A64',u'大于1000'),
                        ('A65',u'未知或没有')])
    employment_status = RadioField(u'就业时间', default='A74', choices=[
                        ('A71',u'无业'),
                        ('A72',u'小于1年'),
                        ('A73',u'1~4年'),
                        ('A74',u'4~7年'),
                        ('A75',u'大于7年')])
    rate_income = StringField(u'分期占收入比', default=3, validators=[Length(min=1, max=4)])
    personal_status = RadioField(u'个人信息', default='A91', choices=[
                        ('A91',u'男：离婚/分居'),
                        ('A92',u'女：离婚/分居/已婚'),
                        ('A93',u'男：单身'),
                        ('A94',u'男：已婚/丧偶'),
                        ('A95',u'女：单身')])
    #10.other_guarantors = StringField('其它担保人', default='A101', validators=[DataRequired()])
    #11.residence_status = StringField('未知属性', default='2', validators=[Length(min=1, max=4)])
    #12.propert = StringField('未知属性', default='A123', validators=[DataRequired()])
    age = StringField(u'责任人数', default=30, validators=[Length(min=18, max=75)])
    #14.plans = StringField('分期计划', default='A143', validators=[DataRequired()])
    housing_type = RadioField(u'住房类型', default='A152', choices=[
                        ('A151',u'租房'),
                        ('A152',u'商品房'),
                        ('A153',u'福利房')])
    load_num = StringField(u'信贷数量', default=3, validators=[Length(min=1, max=4)])     
    job_type = RadioField(u'工作性质', default='A173', choices=[
                        ('A171',u'失业/不熟练-非本地居民'),
                        ('A172',u'不熟练-本地居民'),
                        ('A173',u'熟练的员工/官员'),
                        ('A174',u'管理/个体经营')])
    #18.num_maintenance = StringField('责任人数', default='1', validators=[Length(min=1, max=2)])
    #19.tel = BooleanField('有无联系电话', default='A192', validators=[DataRequired()])
    #20.foreign = BooleanField('是否是外商', default='A202', validators=[DataRequired()])
    predict_ret = StringField(u'结果', default=1, validators=[Length(min=1, max=2)])
    # Submit按钮
    submit = SubmitField(u'提交')
@app.route('/')
def index():
    return '<h1>Credit Classifier Demo!!!</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    if request.method == 'POST':
        if request.form['user'] == 'admin':
            session['user'] = request.form['user']
            response = make_response('Admin login successfully!')
            response.set_cookie('login_tim',time.strftime('%Y-%m-%d %H:%M:%s'))
        else:
            response = make_response('No such user!')
    else:
        if 'user' in session:
            login_time = request.cookies.get('login_time')
            response = make_response('Hello %s, you logged in on %s' % (session['user'], login_time))
        else:
            title = request.args.get('title', 'Default')
            response = make_response(render_template('login.html', title=title),200)
    return response

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)

@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response

@app.route('/exception')
def exception():
    raise InvalidUsage('No privilege to access the resource', status_code=403)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        cmd = ["python", "./tf/clientCredit.py", "999", "1000", "./tf/newTest.csv","./tf/model/credit"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        exitCode = p.returncode
        ret = output.split()[81:]        
        return render_template('predict.html', infos=ret)

@app.route('/credit', methods=('GET', 'POST'))
def credit():
    form = CreditForm()
    return render_template('credit.html', form=form)

@app.route('/classifer', methods=('GET', 'POST'))
def classifer():
    if request.method == 'POST':
        user = ['A14',                                  #1
                request.form.get('duration'),           #2
                request.form.get('credit_history'),     #3
                'A43',                                  #4
                request.form.get('credit_amount'),      #5
                request.form.get('saving_account'),     #6
                request.form.get('employment_status'),  #7
                request.form.get('rate_income'),        #8
                request.form.get('personal_status'),    #9
                'A101','2','A123',                      #10,11,12
                request.form.get('age'),                #13
                'A143',                                 #14
                request.form.get('housing_type'),       #15
                request.form.get('load_num'),           #16
                request.form.get('job_type'),           #17
                '1','A192','A202','1'                   #18,19,20,21
        ]
              
        content = ' '.join(user)
        print content
        cmd1 = ["wc", "-l", "./tf/test.txt"]
        cmd2 = ["sed", "-i", "1000d", "./tf/test.txt"]
        cmd3 = ["python", "./tf/handleData.py", "./tf/test.txt", "./tf/newTest.csv"]
        p1 = subprocess.Popen(cmd1, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
        output1 = p1.communicate()[0]
        exitCode1 = p1.returncode
        ret1 = output1.split()
        while int(ret1[0]) > 999:
            print("删除第1000行!!!")
            p2 = subprocess.Popen(cmd2, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
            output2 = p2.communicate()[0]
            exitCode2 = p2.returncode
            print output2
            print exitCode2
            
            p1 = subprocess.Popen(cmd1, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
            output1 = p1.communicate()[0]
            exitCode1 = p1.returncode
            ret1 = output1.split()
            print int(ret1[0])

        with open("./tf/test.txt","a") as f:
            print("###写用户信息到第1000行")
            f.write(content)
            f.write('\r\n')
            
        p3 = subprocess.Popen(cmd3, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
        output3 = p3.communicate()[0]
        exitCode3 = p3.returncode
        print output3
        print exitCode3          
        return render_template('classifer.html',user=user)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
