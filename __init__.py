import json
import os
from random import randrange
from time import sleep
import pymysql
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from flask_recaptcha import ReCaptcha
import paypalrestsdk
import datetime

app = Flask(__name__)
app.secret_key = "Thisisasecretkeytosuccess"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECAPTCHA_SITE_KEY'] = '6LeuTW0eAAAAAHoCsv-IHdtjvMY4W4wnj7rl6qD9'  # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '6LeuTW0eAAAAADo0-OCkk4UfKnZnf0uQs1SxXcFA'  # <-- Add your secret key
recaptcha = ReCaptcha(app)  # Create a ReCaptcha object by passing in 'app' as parameter

paypalrestsdk.configure({
    "mode": "live",  # sandbox or live
    "client_id": "AZPgDn3JO8IRQf9chqZ_EJWziLRD-yjsg35SOVXrzyDn5rRZBX2rWZcV705tBVeSsNfnXBpUYCNyHXfp",
    "client_secret": "EJYyLKxLlVzX5_cbQ8RYNPVQ3xyZ7j4UrsMFN5OKH0XmRbCxdZN7k0TJgXSf--LcjBCdL5YrSkawBDqp"})


def connectMysql():
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='', db="measure",
                                 autocommit=True, max_allowed_packet=67108864)
    return connection


@app.route('/')
@app.route('/index')
def index():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    sliderList = []
    serviceList = []
    testimonialsList = []
    clientsList = []
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table intro_sliders
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM introsliders')
    sliderData = cur.fetchall()
    for row in sliderData:
        if row[5] == 1:
            sliderList.append(row)
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services WHERE isactive=1')
    services = cur.fetchall()
    for row in services:
        serviceList.append(row)
    cur.close()
    # table testimonials
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM testimonials')
    testimonials = cur.fetchall()
    for row in testimonials:
        testimonialsList.append(row)
    cur.close()
    # table clients
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients')
    clients = cur.fetchall()
    for row in clients:
        clientsList.append(row)
    cur.close()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []
    return render_template('index.html',
                           appname=appdata[1],
                           appmeta=appdata[2],
                           appmetakeyword=appdata[3],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           widgetonetitle=appdata[12],
                           widgetonedescription=appdata[13],
                           widgettwotitle=appdata[14],
                           widgettwodescription=appdata[15],
                           widgetthreetitle=appdata[16],
                           widgetthreedescription=appdata[17],
                           address=appdata[18],
                           appwhatsappnumber=appdata[20],
                           whatsappdefaulttext=appdata[21],
                           author=appdata[5],
                           sliderlist=sliderList,
                           servicelist=serviceList,
                           testimonialslist=testimonialsList,
                           clientslist=clientsList,
                           userlogedin=userLoggedIn,
                           username=username,
                           cartitems=cartitems
                           )


@app.route('/faq')
def faq():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table faq's
    cur = conn.cursor()
    cur.execute('SELECT * FROM faqs')
    faqs = cur.fetchall()
    return render_template('faq.html',
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           userlogedin=userLoggedIn,
                           username=username,
                           faqs=faqs
                           )


@app.route('/about/')
def about():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    servicelist = []
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table about
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM about')
    aboutdata = cur.fetchone()
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    for row in services:
        servicelist.append(row)
    cur.close()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []

    cur = conn.cursor()
    cur.execute('SELECT * FROM aboutservice')
    aboutservice = cur.fetchone()
    print(aboutservice)
    return render_template('about.html',
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           aboutpagetitle=aboutdata[1],
                           aboutpagemeta=aboutdata[2],
                           aboutpagemetakeyword=aboutdata[3],
                           about_title=aboutdata[4],
                           about_description=aboutdata[5],
                           runner1count=aboutdata[6],
                           runner1desc=aboutdata[7],
                           runner2count=aboutdata[8],
                           runner2desc=aboutdata[9],
                           runner3count=aboutdata[10],
                           runner3desc=aboutdata[11],
                           runner4count=aboutdata[12],
                           runner4desc=aboutdata[13],
                           aboutimage=aboutdata[14],
                           servicelist=servicelist,
                           userlogedin=userLoggedIn,
                           username=username,
                           cartitems=cartitems,
                           aboutservice=aboutservice
                           )


@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    servicelist = []
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    cur.close()
    for row in services:
        a = {
            'service_id': row[0],
            'service_price': row[6],
            'service_type': row[5],
            'service_name': row[1],
            'download': row[4]
        }
        cur = conn.cursor()
        cur.execute('SELECT * FROM pricingparams WHERE service_id = %s', row[0])
        pricingparams = cur.fetchall()
        a['pricingparams'] = pricingparams
        servicelist.append(a)
    # table pricing_page
    print(servicelist)
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pricingpage')
    pricingpagedata = cur.fetchone()
    cur.close()
    # table params
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []

    return render_template('pricing.html',
                           pricingpagetitle=pricingpagedata[1],
                           pricingpagemeta=pricingpagedata[2],
                           pricingpagemetakeyword=pricingpagedata[3],
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           servicelist=servicelist,
                           userlogedin=userLoggedIn,
                           username=username,
                           cartitems=cartitems,
                           )


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    servicelist = []
    blogslist = []
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    for row in services:
        servicelist.append(row)
    cur.close()
    # table blog page
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blogpageinfo')
    blogpageinfo = cur.fetchone()
    cur.close()
    # table blog
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog ORDER BY created_at DESC')
    blogs = cur.fetchall()
    for row in blogs:
        blogslist.append(row)
    cur.close()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []
    return render_template('blog.html',
                           blogpage_title=blogpageinfo[1],
                           blogpagepagemeta=blogpageinfo[2],
                           blogpagepagemetakeyword=blogpageinfo[3],
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           servicelist=servicelist,
                           blogslist=blogslist,
                           userlogedin=userLoggedIn,
                           username=username,
                           cartitems=cartitems
                           )


@app.route('/blogread', methods=['GET', 'POST'])
def blogread():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    servicelist = []
    blogslist = []
    blogdata = []
    res = []
    blogid = request.args.get("id")
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table blog single
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog WHERE id = %s', blogid)
    blogdetail = cur.fetchall()
    for row in blogdetail:
        blogdata = row
        if row[4]:
            res = row[4]
    cur.close()
    # table blog
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog ORDER BY created_at DESC')
    blogs = cur.fetchall()
    for row in blogs:
        blogslist.append(row)
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    for row in services:
        servicelist.append(row)
    cur.close()
    return render_template('blog-single.html',
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           iframe=appdata[19],
                           author=appdata[5],
                           blogdata=blogdata,
                           blogslist=blogslist,
                           servicelist=servicelist,
                           userlogedin=userLoggedIn,
                           username=username,
                           res=res
                           )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False

    servicelist = []
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    # table services
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    services = cur.fetchall()
    for row in services:
        servicelist.append(row)
    cur.close()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []
    return render_template('contact.html',
                           appname=appdata[1],
                           appmeta=appdata[2],
                           appmetakeyword=appdata[3],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           iframe=appdata[19],
                           author=appdata[5],
                           servicelist=servicelist,
                           userlogedin=userLoggedIn,
                           username=username,
                           cartitems=cartitems
                           )


@app.route('/postcontact', methods=['GET', 'POST'])
def contactrequest():
    if request.method == 'POST':
        name = request.values.get('name')
        email = request.values.get('email')
        subject = request.values.get('subject')
        message = request.values.get('message')
        # insert into contactrequests
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute("INSERT INTO contactrequests(name,email,subject,message) VALUES (%s,%s,%s,%s)",
                    (name, email, subject, message))
        return "OK"


@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    # Login Function
    if request.method == 'POST':
        if recaptcha.verify():
            email = request.values.get('email')
            password = request.values.get('password')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            account = cur.fetchone()
            if account:
                session['_is_user_logged_in'] = True
                session['firstname'] = account[0]
                session['lastname'] = account[1]
                session['email'] = account[2]
                session['password'] = account[3]
                cur.close()
                sleep(2)
                return redirect(url_for('index'))
            else:
                cur.close()
                return render_template('/login.html', msg="Invalid Credentials")
        else:
            message = 'Please fill out the ReCaptcha!'
            return render_template('login.html', message=message)

    return render_template('login.html')


@app.route('/userregister', methods=['GET', 'POST'])
def userregister():
    if request.method == 'POST':
        firstname = request.values.get('fname')
        lastname = request.values.get('lname')
        email = request.values.get('email')
        password = request.values.get('password')
        # insert into table user
        if recaptcha.verify():  # Use verify() method to see if ReCaptcha is filled out
            try:
                conn = connectMysql()
                cur = conn.cursor()
                cur.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                            (firstname, lastname, email, password))
                cur.close()
                # Login Function
                conn = connectMysql()
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
                account = cur.fetchone()
                if account:
                    session['_is_user_logged_in'] = True
                    session['firstname'] = account[0]
                    session['lastname'] = account[1]
                    session['email'] = account[2]
                    session['password'] = account[3]
                    cur.close()
                    sleep(2)
                    return redirect(url_for('index'))
            except pymysql.Error as e:
                print("************error****************")
                print(e)
                if e.args[0] == 1062:
                    return render_template('register.html', msg="Email address is already registered")
        else:
            message = 'Please fill out the ReCaptcha!'  # Send error message
            render_template('register.html', message=message)

    return render_template('register.html')


@app.route('/ordernew', methods=['GET', 'POST'])
def ordernewpage():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()

    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
        cartitems = cur.fetchall()
    except pymysql.Error:
        cartitems = []

    servicelist = []
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services WHERE isactive=1')
    services = cur.fetchall()
    for row in services:
        servicelist.append(row)
    cur.close()
    return render_template('ordernew.html', servicelist=servicelist,
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           username=username,
                           userlogedin=userLoggedIn,
                           cartitems=cartitems
                           )


@app.route('/order', methods=['GET', 'POST'])
def orderpage():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    servicelist = []
    if session.get('_is_user_logged_in') is True:
        # table app_config
        if request.method == 'GET':

            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM app_config')
            appdata = cur.fetchone()
            cur.close()
            # table services
            cur = conn.cursor()
            cur.execute('SELECT * FROM services')
            services = cur.fetchall()
            for row in services:
                servicelist.append(row)
            cur.close()
            if request.method == 'GET':
                serviceid = request.args.get('id')
                servicename = request.args.get('servicename')
                cur = conn.cursor()
                cur.execute('SELECT * FROM services WHERE id = %s', serviceid)
                detail = cur.fetchone()
                servicedetails = {
                    "service_id": serviceid,
                    "service_name": servicename,
                    "service_price": detail[6],
                    "service_params": "",
                }
                if serviceid is not None:
                    paramlist = []
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM serviceparams WHERE id=%s', serviceid)
                    allparams = cur.fetchall()
                    paramheading = []
                    for row in allparams:
                        paramheading.append(row[3])
                        paramlist.append(
                            {
                                "param": row[1],
                                "param_type": row[2],
                                "param_heading": row[3],
                                "param_price": row[7],
                            }
                        )
                        servicedetails['service_params'] = paramlist
                    param_heading_list = []
                    for i in paramheading:
                        if i not in param_heading_list:
                            param_heading_list.append(i)
                    try:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
                        cartitems = cur.fetchall()
                    except pymysql.Error:
                        cartitems = []

                    try:
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM userlogos WHERE user_id =%s', session.get('email'))
                        userlogos = cur.fetchall()
                    except pymysql.Error:
                        userlogos = []
                    return render_template('order.html',
                                           appname=appdata[1],
                                           appmeta=appdata[2],
                                           appmetakeyword=appdata[3],
                                           applogo=appdata[4],
                                           companymail=appdata[6],
                                           companyphone=appdata[7],
                                           companytwitter=appdata[8],
                                           companyfacebook=appdata[9],
                                           companyinstagram=appdata[10],
                                           companylinkedin=appdata[11],
                                           servicelist=servicelist,
                                           address=appdata[18],
                                           author=appdata[5],
                                           userlogedin=userLoggedIn,
                                           username=username,
                                           servicename=servicename,
                                           serviceid=serviceid,
                                           servicedetails=servicedetails,
                                           param_heading_list=param_heading_list,
                                           cartitems=cartitems,
                                           userlogos=userlogos
                                           )
            else:
                print("no service id")
        if request.method == 'POST':
            sub_price = 0
            postdata = request.form
            # pdfplan = request.files['Upload Pdf Plan']
            # dounloadurl = ""
            # if pdfplan.filename:
            #     print(pdfplan)
            #     path = os.path.join(app.config['UPLOAD_FOLDER'], 'blueprintuploads', pdfplan.filename)
            #     dounloadurl = "../static/img/blueprintuploads/" + pdfplan.filename
            #     pdfplan.save(path)
            #     print(dounloadurl)

            ser_id = request.args.get('ser_id')
            useremail = session.get('email')
            cart_id = "AER_EST-" + str(randrange(111111, 999999))
            conn = connectMysql()
            for key in postdata.keys():
                cur = conn.cursor()
                cur.execute('SELECT price from serviceparams WHERE param_heading = %s and id=%s', (key, ser_id))
                price = cur.fetchone()
                if price is not None:
                    sub_price = sub_price + price[0]
            a = json.dumps(postdata)
            jsons = json.loads(a)
            jsons['Optional Deliverables'] = postdata.getlist('Optional Deliverables')
            a = json.dumps(jsons)
            try:
                qty = json.loads(a)['quantity']
                cur = conn.cursor()
                cur.execute('SELECT price from services WHERE id = %s', ser_id)
                service_price = cur.fetchone()
                totalprice = (service_price[0] + sub_price) * int(qty)
                a = json.loads(a)
                a['price'] = totalprice
            except pymysql.Error:
                cur = conn.cursor()
                cur.execute('SELECT price from services WHERE id = %s', ser_id)
                service_price = cur.fetchone()
                totalprice = service_price[0] + sub_price
                a = json.loads(a)
                a['price'] = totalprice
            cur = conn.cursor()
            cur.execute('INSERT INTO cart_table (id,user_id,service_id,service_param) VALUES(%s,%s,%s,%s)',
                        (cart_id, useremail, ser_id, json.dumps(a)))
            cur.close()
            return redirect(url_for('cart'))
    else:
        return redirect(url_for('userlogin'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
        servicelist = []
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()
        # table about
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM about')
        aboutdata = cur.fetchone()
        cur.close()
        # table services
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM services')
        services = cur.fetchall()
        for row in services:
            servicelist.append(row)
        cur.close()
        useremail = session.get('email')
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM cart_table JOIN services ON cart_table.service_id=services.id WHERE cart_table.user_id=%s',
            useremail)
        cartitems = cur.fetchall()
        paramlist = []
        for i in range(len(cartitems)):
            paramlist.append(json.loads(cartitems[i][3]))
        cur.close()
        # check price breakup

        return render_template('cart.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               aboutpagetitle=aboutdata[1],
                               aboutpagemeta=aboutdata[2],
                               aboutpagemetakeyword=aboutdata[3],
                               servicelist=servicelist,
                               userlogedin=userLoggedIn,
                               username=username,
                               cartitems=cartitems,
                               paramlist=paramlist
                               )
    else:
        return redirect(url_for('userlogin'))


@app.route('/deletecart', methods=['GET', 'POST'])
def cont_deletecart():
    id = request.args.get('id')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('DELETE FROM cart_table WHERE id=%s', id)
    cur.close()
    return redirect(url_for('cart'))


def orderinsert(params, order_id, service_id, i):
    username = session.get('email')
    conn = connectMysql()
    try:
        cur = conn.cursor()
        cur.execute('SELECT service_title FROM services WHERE id =%s', service_id)
        service_name = cur.fetchone()
        service_name = service_name[0]
        cur.close()
        a = {
            "service_id": service_id,
            "service_name": service_name,
            "service_param": params
        }
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO order_table(order_id,user_id,progress,items,order_sub_id)VALUES(%s,%s,%s,%s,%s)',
                        (order_id, username, 0, json.dumps(a), i))
        except pymysql.Error as e:
            print(e)
        cur.close()
    except pymysql.Error as e:
        return {
                   "msg": str(e)
               }, 202


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # order_id = "AER_EST_ORDER-" + str(randrange(10000, 90000))
        order_id = generatingOrder()
        data = request.get_json()
        type = data.get('type')
        couponcode_isapplied = data.get('couponcode_isapplied')
        autodiscount_applied = data.get('autodiscount_applied')
        autodiscount_percentage = data.get('autodiscount_percentage')
        couponcode_percentage = data.get('couponcode_percentage')
        username = session.get('email')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id=%s', username)
        items = cur.fetchall()
        cur.close()
        for i in range(len(items)):
            a = json.loads(items[i][3])
            a['payment_mode'] = type
            if autodiscount_applied:
                discounted_amount = json.loads(items[i][3])['price'] - (
                        (autodiscount_percentage / 100) * json.loads(items[i][3])['price'])
                a['autodiscountedprice'] = discounted_amount
            if couponcode_isapplied:
                try:
                    a['couponcode_discountedprice'] = a['autodiscountedprice'] - (
                            (couponcode_percentage / 100) * a['autodiscountedprice'])
                    orderinsert(a, order_id, items[i][2], i)
                except pymysql.Error:
                    a['couponcode_discountedprice'] = a['price'] - (
                            (couponcode_percentage / 100) * json.loads(items[i][3])['price'])
                    orderinsert(a, order_id, items[i][2], i)
            else:
                orderinsert(a, order_id, items[i][2], i)
        return order_id, 200
    if request.method == 'GET':
        itemlist = []
        totalp = 0
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        # table app_config
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()

        useremail = session.get('email')
        cur = conn.cursor()
        cur.execute('SELECT * FROM cart_table WHERE user_id=%s', useremail)
        items = cur.fetchall()
        cur.close()
        for ro in items:
            cur = conn.cursor()
            cur.execute('SELECT service_title FROM services WHERE id =%s', ro[2])
            ser_title = cur.fetchone()
            ser_title = ser_title[0]
            cur.close()
            totalp = totalp + json.loads(ro[3])['price']
            try:
                qty = json.loads(ro[3])['quantity']
            except pymysql.Error:
                qty = 1
            itemlist.append(
                {
                    "title": ser_title,
                    "qty": qty,
                    "price": json.loads(ro[3])['price']
                }
            )
        groupswallet_list = []
        cur = conn.cursor()
        cur.execute('SELECT * FROM discount_group_users WHERE discount_group_user_id=%s', useremail)
        discount_details = cur.fetchone()
        cur.close()
        if discount_details:
            discount_group_id = discount_details[0]
            cur = conn.cursor()
            cur.execute('SELECT * FROM discount_group WHERE id=%s', discount_group_id)
            grpdetails = cur.fetchone()
            discamount = totalp * (grpdetails[2] / 100)
            payable = totalp - discamount
        else:
            grpdetails = None
            discamount = None
            payable = totalp

        cur = conn.cursor()
        cur.execute('SELECT * FROM coupon_code WHERE for_user=%s', useremail)
        coupons = cur.fetchone()

        cur = conn.cursor()
        cur.execute('SELECT * FROM user_groups WHERE user_id=%s', useremail)
        groups = cur.fetchall()
        for rows in groups:
            cur = conn.cursor()
            cur.execute('SELECT * FROM group_wallet WHERE group_id=%s', rows[0])
            groupmoney = cur.fetchone()
            groupswallet_list.append(groupmoney)

        cur = conn.cursor()
        cur.execute('SELECT wallet_amount FROM users WHERE email=%s', useremail)
        pwalletamount = cur.fetchone()
        pwalletamount = pwalletamount[0]
        return render_template('checkout.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               itemlist=itemlist,
                               totalp=totalp,
                               grpdetails=grpdetails,
                               discamount=discamount,
                               payable=payable,
                               coupons=coupons,
                               groupswalletlist=groupswallet_list,
                               pwalletamount=pwalletamount
                               )


def generatingOrder():
    conn = connectMysql()
    cur = conn.cursor()
    idList = []
    date = datetime.datetime.today().strftime("%y") + datetime.datetime.today().strftime("%m")
    cmd = "SELECT order_id FROM order_table where order_id LIKE '2312%';"
    cmd = "SELECT order_id FROM order_table WHERE order_id LIKE '{}'".format(date + '%')
    cur.execute(cmd)
    data = cur.fetchall()
    cur.close()

    if data:
        for da in data:
            if da[0].startswith(date):
                idList.append(da[0])
        if idList:
            max_ = max([int(x) for x in idList])
            return str(max_ + 1)
    else:
        return date + '001'


@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    payable = data.get('payable')
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "/payment/execute",
            "cancel_url": "/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": payable,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": payable,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        i = 0
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
    else:
        print(payment.error)

    return jsonify({'success': success})


@app.route('/success', methods=['GET', 'POST'])
def success():
    id = request.args.get('id')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM order_table WHERE order_id = %s', id)
    orders = cur.fetchall()
    return render_template('success.html', orders=orders)


@app.route('/myorders', methods=['GET', 'POST'])
def my_orders():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()

    cur = conn.cursor()
    cur.execute('SELECT * FROM order_table WHERE user_id =%s ORDER BY DATE(created_at) DESC', session.get('email'))
    myorders = cur.fetchall()
    cur.close()
    servicename = []
    paramlist = []
    pricelist = []
    commentlist = []
    for i in range(len(myorders)):
        paramlist.append(json.loads(myorders[i][3])['service_param'])
        servicename.append(json.loads(myorders[i][3])['service_name'])
        a = {
            'cart_total': json.loads(myorders[i][3])['service_param']['price'],
            'paidamount': json.loads(myorders[i][3])['service_param']['price']
        }
        try:
            autodiscountedprice = json.loads(myorders[i][3])['service_param']['autodiscountedprice']
            a['autodiscountedprice'] = round(json.loads(myorders[i][3])['service_param']['price'] - autodiscountedprice,
                                             4)
            a['paidamount'] = json.loads(myorders[i][3])['service_param']['autodiscountedprice']
        except pymysql.Error:
            a['autodiscountedprice'] = 0

        try:
            couponcode_discountedprice = json.loads(myorders[i][3])['service_param']['couponcode_discountedprice']
            a['paidamount'] = json.loads(myorders[i][3])['service_param']['couponcode_discountedprice']
            a['couponcode_discountedprice'] = round(
                json.loads(myorders[i][3])['service_param']['price'] - couponcode_discountedprice, 4)
        except pymysql.Error:
            a['couponcode_discountedprice'] = 0

        pricelist.append(a)
        cur = conn.cursor()
        cur.execute('SELECT * FROM chats WHERE order_id = %s ORDER BY created_at DESC', myorders[i][0])
        commentlist.append(cur.fetchone())
    return render_template('myorders.html',
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           userlogedin=userLoggedIn,
                           username=username,
                           myorders=myorders,
                           paramlist=paramlist,
                           servicename=servicename,
                           pricelist=pricelist,
                           commentlist=commentlist
                           )


@app.route('/vieworder', methods=['GET', 'POST'])
def vieworder():
    if request.method == 'GET':
        orderid = request.args.get('id')
        subid = request.args.get('subid')
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()

        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM order_table WHERE user_id =%s AND order_id = %s AND order_sub_id=%s ORDER BY DATE('
            'created_at) DESC',
            (session.get('email'), orderid, subid))
        myorders = cur.fetchall()
        cur.close()
        servicename = []
        paramlist = []
        pricelist = []
        for i in range(len(myorders)):
            paramlist.append(json.loads(myorders[i][3])['service_param'])
            servicename.append(json.loads(myorders[i][3])['service_name'])
            a = {
                'cart_total': json.loads(myorders[i][3])['service_param']['price'],
                'paidamount': json.loads(myorders[i][3])['service_param']['price']
            }
            try:
                autodiscountedprice = json.loads(myorders[i][3])['service_param']['autodiscountedprice']
                a['autodiscountedprice'] = round(
                    json.loads(myorders[i][3])['service_param']['price'] - autodiscountedprice, 4)
                a['paidamount'] = json.loads(myorders[i][3])['service_param']['autodiscountedprice']
            except pymysql.Error:
                a['autodiscountedprice'] = 0

            try:
                couponcode_discountedprice = json.loads(myorders[i][3])['service_param']['couponcode_discountedprice']
                a['paidamount'] = json.loads(myorders[i][3])['service_param']['couponcode_discountedprice']
                a['couponcode_discountedprice'] = round(
                    json.loads(myorders[i][3])['service_param']['price'] - couponcode_discountedprice, 4)
            except pymysql.Error:
                a['couponcode_discountedprice'] = 0

            pricelist.append(a)
        return render_template('vieworder.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               myorders=myorders,
                               paramlist=paramlist,
                               servicename=servicename,
                               pricelist=pricelist
                               )
    else:
        return 'METHOD NOT ALLOWED'


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        # table app_config
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()
        id = request.args['id']
        sub_id = request.args['sub_id']
        session['selected_id_for_chat'] = id
        session['selected_sub_id_for_chat'] = sub_id
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM chats WHERE order_id = %s AND order_sub_id = %s ORDER BY created_at DESC',
                    (id, sub_id))
        chats = cur.fetchall()
        return render_template('chat.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               chats=chats
                               )
    if request.method == 'POST':
        orderid = session.get('selected_id_for_chat')
        order_sub_id = session.get('selected_sub_id_for_chat')
        subject = request.form.get('subject')
        message = request.form.get('message')
        aboutimage = request.files['file']
        dounloadurl = ""
        if aboutimage.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'chatuploads', aboutimage.filename)
            dounloadurl = "../static/img/chatuploads/" + aboutimage.filename
            aboutimage.save(path)
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO chats (order_id,sender_id,replyer_id,subject,message,document_url,from_who,to_who,'
            'order_sub_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (orderid, session.get('email'), "", subject, message, dounloadurl, 1, 0, order_sub_id))
        cur.close()
        return redirect(url_for('chat') + '?id=' + orderid + '&sub_id=' + order_sub_id)


@app.route('/deliverables', methods=['GET', 'POST'])
def deliverables():
    username = ""
    if session.get('_is_user_logged_in') is True:
        userLoggedIn = True
        username = session.get('firstname') + " " + session.get('lastname')
    else:
        userLoggedIn = False
    # table app_config
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM app_config')
    appdata = cur.fetchone()
    cur.close()
    id = request.args['id']
    sub_id = request.args['sub_id']

    cur = conn.cursor()
    cur.execute('SELECT * FROM order_table')
    # orders = cur.fetchall()
    cur = conn.cursor()
    cur.execute('SELECT * FROM deliverables WHERE order_id = %s AND order_sub_id = %s ORDER BY created_at DESC',
                (id, sub_id))
    deliverables = cur.fetchall()

    return render_template('deliverables.html',
                           appname=appdata[1],
                           applogo=appdata[4],
                           companymail=appdata[6],
                           companyphone=appdata[7],
                           companytwitter=appdata[8],
                           companyfacebook=appdata[9],
                           companyinstagram=appdata[10],
                           companylinkedin=appdata[11],
                           address=appdata[18],
                           author=appdata[5],
                           userlogedin=userLoggedIn,
                           username=username,
                           deliverables=deliverables
                           )


@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()

        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email =%s', session.get('email'))
        user = cur.fetchone()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
            cartitems = cur.fetchall()
        except pymysql.Error:
            cartitems = []

        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM userlogos WHERE user_id =%s', session.get('email'))
            userlogos = cur.fetchall()
        except pymysql.Error:
            userlogos = []

        return render_template('myaccount.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               user=user,
                               cartitems=cartitems,
                               userlogos=userlogos
                               )
    if request.method == 'POST':
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        secemail = request.form.get('sec_email')
        country = request.form.get('country')
        states = request.form.get('states')
        hno = request.form.get('hno')
        street = request.form.get('street')
        city = request.form.get('city')
        zip = request.form.get('Zip')
        phone = request.form.get('Phone')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(
            'UPDATE users SET first_name = %s,last_name=%s,sec_email=%s,country=%s,state=%s,houseno=%s,street=%s,'
            'city=%s,zipcode=%s,phone=%s WHERE email=%s',
            (fname, lname, secemail, country, states, hno, street, city, zip, phone, email,))
        cur.close()
        return redirect(url_for('myaccount'))


@app.route('/deleteuserlogo', methods=['GET', 'POST'])
def deleteuserlogo():
    if request.method == 'GET':
        logoid = request.args.get("id")
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM userlogos WHERE id = %s', logoid)
        cur.close()
        return redirect(url_for('myaccount'))


@app.route('/uploaduserlogo', methods=['GET', 'POST'])
def userlogoupload():
    if request.method == 'POST':
        dounloadurl = ""
        userlogo = request.files['file']
        if userlogo.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'userlogouploads', userlogo.filename)
            dounloadurl = "/static/img/userlogouploads/" + userlogo.filename
            userlogo.save(path)
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('INSERT INTO userlogos (user_id,logo_url) VALUES (%s,%s)', (session.get('email'), dounloadurl))
        cur.close()
        return redirect(url_for('myaccount'))
    else:
        return redirect(url_for('myaccount'))


@app.route('/mywallet', methods=['GET', 'POST'])
def mywallet():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()
        cur = conn.cursor()
        cur.execute('SELECT * FROM transaction WHERE user_id = %s', session.get('email'))
        transactions = cur.fetchall()
        cur = conn.cursor()
        cur.execute('SELECT wallet_amount FROM users WHERE email = %s', session.get('email'))
        currbal = cur.fetchone()
        cur.close()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
            cartitems = cur.fetchall()
        except pymysql.Error:
            cartitems = []
        return render_template('mywallet.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               transactions=transactions,
                               currbal=currbal,
                               cartitems=cartitems
                               )
    if request.method == 'POST':
        amount = request.form.get('amount')
        transaction_type = '0'
        conn = connectMysql()
        transaction_id = "AER_EST_TRANS_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO transaction(transaction_id,user_id,amount_details,transaction_type)VALUES (%s,%s,%s,%s)',
                (transaction_id, session.get('email'), amount, transaction_type))
            cur.close()
            if transaction_type == "0":
                cur = conn.cursor()
                cur.execute('SELECT wallet_amount FROM users WHERE email = %s', session.get('email'))
                examount = cur.fetchone()
                cur.close()
                upamount = examount[0] + int(amount)
                cur = conn.cursor()
                cur.execute('UPDATE users SET wallet_amount=%s WHERE email=%s', (upamount, session.get('email'),))
                cur.close()
            elif transaction_type == "1":
                cur = conn.cursor()
                cur.execute('SELECT wallet_amount FROM users WHERE email = %s', (session.get('email')))
                examount = cur.fetchone()
                cur.close()
                upamount = examount[0] - int(amount)
                cur = conn.cursor()
                cur.execute('UPDATE users SET wallet_amount=%s WHERE email = %s', (upamount, session.get('email'),))
                cur.close()
        except pymysql.Error as e:
            return {
                       "msg": str(e)
                   }, 202
        return redirect(url_for('mywallet'))


@app.route('/mygroups', methods=['GET', 'POST'])
def mygroups():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart_table WHERE user_id =%s', session.get('email'))
            cartitems = cur.fetchall()
        except pymysql.Error:
            cartitems = []
        grp_list = []
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM user_groups WHERE user_id=%s', (session.get('email')))
            usergrp = cur.fetchall()
            if usergrp:
                for row in usergrp:
                    cur = conn.cursor()
                    cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', (row[0]))
                    grp_amount = cur.fetchone()
                    grp_list.append({
                        "group_id": row[0],
                        "group_name": row[1],
                        "role": row[3],
                        "amount": grp_amount[0]}
                    )
        except pymysql.Error as e:
            return {
                       "msg": e
                   }, 202
        return render_template('mygroups.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               grp_list=grp_list,
                               cartitems=cartitems
                               )


@app.route('/viewgroup', methods=['GET', 'POST'])
def viewgroup():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()
        grpid = request.args.get('id')
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_groups WHERE group_id = %s', grpid)
        users = cur.fetchall()

        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        allusers = cur.fetchall()
        return render_template('viewgroup.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               users=users,
                               allusers=allusers
                               )
    if request.method == 'POST':
        id = request.form.get('groupid')
        user = request.form.get('employee')
        grpname = request.form.get('groupname')

        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO user_groups (user_id,group_id,group_name,role) VALUES (%s,%s,%s,%s)',
                        (user, id, grpname, "0"))
            cur.close()
            return redirect(url_for('viewgroup') + '?id=' + id + '&grpname=' + grpname)
        except pymysql.Error as e:
            return {
                       "msg": str(e)
                   }, 202


@app.route('/deleteuserfromgrp', methods=['GET'])
def deleteuserfromgrp():
    grpid = request.args.get('grpid')
    grpname = request.args.get('grpname')
    userid = request.args.get('userid')
    conn = connectMysql()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM user_groups WHERE user_id=%s AND group_id=%s ', (userid, grpid))
        cur.close()
        return redirect(url_for('viewgroup') + '?id=' + grpid + '&grpname=' + grpname)
    except pymysql.Error as e:
        return {
                   "msg": e
               }, 202


@app.route('/viewgrouptransactions', methods=['GET', 'POST'])
def viewgrouptransactions():
    if request.method == 'GET':
        username = ""
        if session.get('_is_user_logged_in') is True:
            userLoggedIn = True
            username = session.get('firstname') + " " + session.get('lastname')
        else:
            userLoggedIn = False
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM app_config')
        appdata = cur.fetchone()
        cur.close()

        grpid = request.args.get('id')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM group_wallet_transacctions WHERE group_id = %s', grpid)
        transactions = cur.fetchall()
        cur = conn.cursor()
        cur.execute('SELECT amount FROM group_wallet WHERE group_id = %s', grpid)
        currbal = cur.fetchone()
        return render_template('viewgrouptransactions.html',
                               appname=appdata[1],
                               applogo=appdata[4],
                               companymail=appdata[6],
                               companyphone=appdata[7],
                               companytwitter=appdata[8],
                               companyfacebook=appdata[9],
                               companyinstagram=appdata[10],
                               companylinkedin=appdata[11],
                               address=appdata[18],
                               author=appdata[5],
                               userlogedin=userLoggedIn,
                               username=username,
                               transactions=transactions,
                               currbal=currbal
                               )
    if request.method == 'POST':
        grpid = request.form.get('grpid')
        amount = request.form.get('amount')
        conn = connectMysql()
        group_transaction_id = "AER_EST_GRP_TRANS_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM  user_groups WHERE user_id=%s AND role=1', (session.get('email')))
            user = cur.fetchone()
            cur.close()
            if user:
                cur = conn.cursor()
                cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', grpid)
                amt = cur.fetchone()
                upamount = amt[0] + int(amount)
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, grpid))
                cur.close()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,transaction_type,'
                    'group_user_id) VALUES(%s,%s,%s,%s,%s)',
                    (group_transaction_id, grpid, amount, 1, session.get('email')))
                cur.close()
                return redirect(url_for('viewgrouptransactions') + '?id=' + grpid)
        except pymysql.Error as e:
            return {
                       "msg": str(e)
                   }, 202


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'GET':
        return render_template('forgotpassword.html')
    if request.method == 'POST':
        email = request.form.get('email')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', email)
        user = cur.fetchone()
        if user:
            # content = "Greetings from aerial estimation, Please find password Reset Link for your account : " + email
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + email + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:reset password\n'
            # mail.sendmail("devsandy12@gmail.com", email, content)
            # mail.close()
            msg = 'Link for password reset is sent to your email.'
        else:
            msg = 'No user found with this email'
        return render_template('forgotpassword.html', msg=msg)


@app.route('/addgroup', methods=['GET', 'POST'])
def creategrp():
    if request.method == 'POST':
        group_name = request.values.get('groupname')
        user_id = session.get('email')
        conn = connectMysql()
        group_id = "AER_EST_GRP_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO user_groups (group_id,group_name,user_id,role) VALUES(%s,%s,%s,%s)',
                        (group_id, group_name, user_id, 1))
            cur.close()
            cur = conn.cursor()
            cur.execute('INSERT INTO group_wallet (group_id,amount) VALUES (%s,%s)', (group_id, 0))
            cur.close()
            return redirect(url_for('mygroups'))
        except pymysql.Error as e:
            return {
                       "msg": str(e)
                   }, 202


# -------------------------------------------------------------------------
# Admin panel section starts here
# -------------------------------------------------------------------------

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':

        username = request.values.get('username')
        password = request.values.get('password')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        account = cur.fetchone()
        if account:
            session['_is_logged_in'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['role'] = account[3]
            session['name'] = account[4]
            cur.close()
            return redirect(url_for('admin_dash'))
        else:
            cur.close()
            return render_template('Admin/pages/samples/login.html', msg="Invalid Credentials")
    if request.method == 'GET':
        if session.get('_is_logged_in') is True:
            return redirect(url_for('admin_dash'))

    return render_template('Admin/pages/samples/login.html')


@app.route('/admin/')
@app.route('/admin/dashboard')
def admin_dash():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        cur = conn.cursor()
        cur.execute('SELECT * FROM admin')
        employees = cur.fetchall()
        cur.close()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table')
        orders = cur.fetchall()
        cur.close()
        revenuechart = {
            "jan": 0,
            "feb": 0,
            "mar": 0,
            "apr": 0,
            "may": 0,
            "jun": 0,
            "july": 0,
            "aug": 0,
            "sept": 0,
            "oct": 0,
            "nov": 0,
            "dec": 0,
        }
        chartcount = {
            "jan": 0,
            "feb": 0,
            "mar": 0,
            "apr": 0,
            "may": 0,
            "jun": 0,
            "july": 0,
            "aug": 0,
            "sept": 0,
            "oct": 0,
            "nov": 0,
            "dec": 0,
        }
        for i in range(len(orders)):
            if orders[i][4].month == 1:
                chartcount['jan'] = chartcount['jan'] + 1
                revenuechart['jan'] = revenuechart['jan'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 2:
                chartcount['feb'] = chartcount['feb'] + 1
                revenuechart['feb'] = revenuechart['feb'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 3:
                chartcount['mar'] = chartcount['mar'] + 1
                revenuechart['mar'] = revenuechart['mar'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 4:
                chartcount['apr'] = chartcount['apr'] + 1
                revenuechart['apr'] = revenuechart['apr'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 5:
                chartcount['may'] = chartcount['may'] + 1
                revenuechart['may'] = revenuechart['may'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 6:
                chartcount['jun'] = chartcount['jun'] + 1
                revenuechart['jun'] = revenuechart['jun'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 7:
                chartcount['july'] = chartcount['july'] + 1
                revenuechart['july'] = revenuechart['july'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 8:
                chartcount['aug'] = chartcount['aug'] + 1
                revenuechart['aug'] = revenuechart['aug'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 9:
                chartcount['sept'] = chartcount['sept'] + 1
                revenuechart['sept'] = revenuechart['sept'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 10:
                chartcount['oct'] = chartcount['oct'] + 1
                revenuechart['oct'] = revenuechart['oct'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 11:
                chartcount['nov'] = chartcount['nov'] + 1
                revenuechart['nov'] = revenuechart['nov'] + int(json.loads(orders[i][3])['service_param']['price'])
            if orders[i][4].month == 12:
                chartcount['dec'] = chartcount['dec'] + 1
                revenuechart['dec'] = revenuechart['dec'] + int(json.loads(orders[i][3])['service_param']['price'])
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = 0')
        porders = cur.fetchall()
        cur.close()
        totalsales = revenuechart['jan'] + revenuechart['feb'] + revenuechart['mar'] + revenuechart['apr'] + \
                     revenuechart['may'] + revenuechart['jun'] + revenuechart['july'] + revenuechart['aug'] + \
                     revenuechart['sept'] + revenuechart['oct'] + revenuechart['nov'] + revenuechart['dec']
        return render_template('Admin/index.html', users=users, employees=employees, orders=orders, porders=porders,
                               chartcount=chartcount, totalsales=totalsales, revenuechart=revenuechart)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/sitesettings/', methods=['GET', 'POST'])
def admin_site_settings():
    if session.get('_is_logged_in') is True:
        if request.method == 'POST':
            sitename = request.values.get('sitename')
            sitemeta = request.values.get('sitemeta')
            sitemetakeywords = request.values.get('sitemetakeywords')
            siteemail = request.values.get('siteemail')
            sitephone = request.values.get('sitephone')
            sitetwitter = request.values.get('sitetwitter')
            sitefacebook = request.values.get('sitefacebook')
            siteinstagram = request.values.get('siteinstagram')
            sitelinkedin = request.values.get('sitelinkedin')
            siteAddress = request.values.get('siteAddress')
            sitelocation = request.values.get('sitelocation')
            sitewhatsappnumber = request.values.get('sitewhatsappnumber')
            sitewhatsappdefaulttext = request.values.get('sitewhatsappdefaulttext')
            file1 = request.files['img[]']
            if file1.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], "logo.png")
                file1.save(path)
                # update into table app_config
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute(
                'UPDATE app_config SET appname=%s, appmeta=%s, appmetakeyword=%s, companymail=%s,companyphone=%s,'
                'companytwitter =%s,companyfacebook=%s,companyinstagram = %s, companylinkedin=%s, address	= %s, '
                'iframe= %s, appwhatsappnumber	= %s, whatsappdefaulttext= %s ,applogo = %s WHERE id=1',
                (sitename, sitemeta, sitemetakeywords, siteemail, sitephone, sitetwitter, sitefacebook, siteinstagram,
                 sitelinkedin, siteAddress, sitelocation, sitewhatsappnumber, sitewhatsappdefaulttext,
                 "http://aerialestimation.doczapp.in/static/img/logo.png"))
            cur.close()
            # table app_config
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM app_config')
            appdata = cur.fetchone()
            cur.close()
            return render_template('Admin/sitesettings.html', appdata=appdata)
        elif request.method == 'GET':
            # table app_config
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM app_config')
            appdata = cur.fetchone()
            cur.close()
            return render_template('Admin/sitesettings.html', appdata=appdata)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/edithomepage/', methods=['GET', 'POST'])
def admin_crm_home_edit():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('select * from app_config')
        appdata = cur.fetchone()
        cur.close()
        return render_template('Admin/Home_edit.html', appdata=appdata)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/edithomepagepost/', methods=['GET', 'POST'])
def admin_crm_home_edit_post():
    if request.method == 'POST':

        widget1title = request.values.get('widget1title')
        widget1desc = request.values.get('widget1desc')
        widget2title = request.values.get('widget2title')
        widget2desc = request.values.get('widget2desc')
        widget3title = request.values.get('widget3title')
        widget3desc = request.values.get('widget3desc')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(
            'UPDATE app_config SET widgetonetitle=%s, widgetonedescription=%s, widgettwotitle=%s, '
            'widgettwodescription=%s,widgetthreetitle=%s,widgetthreedescription =%s WHERE id=1',
            (widget1title, widget1desc, widget2title, widget2desc, widget3title, widget3desc))
        cur.close()
        return redirect(url_for('admin_crm_home_edit'))
    else:
        return redirect(url_for('admin_crm_home_edit'))


@app.route('/admin/editaboutpage/')
def admin_crm_about_edit():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('select * from about')
        aboutdata = cur.fetchone()
        cur.close()
        return render_template('Admin/About_edit.html', aboutdata=aboutdata)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/editfaqpage/', methods=['GET', 'POST'])
def admin_crm_faq_edit():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('select * from faqs')
        faqs = cur.fetchall()
        cur.close()
        return render_template('Admin/faq_edit.html', faqs=faqs)


@app.route('/admin/addfaq', methods=['GET', 'POST'])
def addfaq():
    if request.method == 'POST':
        question = request.values.get('question')
        answer = request.values.get('answer')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('INSERT INTO faqs (question,answer) VALUES (%s,%s)', (question, answer))
        cur.close()
        return redirect(url_for('admin_crm_faq_edit'))
    else:
        return redirect(url_for('admin_crm_faq_edit'))


@app.route('/admin/deletefaq', methods=['GET', 'POST'])
def delfaq():
    if request.method == 'GET':
        id = request.values.get('id')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM faqs WHERE id = %s', id)
        cur.close()
        return redirect(url_for('admin_crm_faq_edit'))


@app.route('/admin/editaboutpagepost/', methods=['GET', 'POST'])
def admin_crm_about_edit_post():
    if request.method == 'POST':
        pagetitle = request.values.get('pagetitle')
        pagemeta = request.values.get('pagemeta')
        pagemetakeywords = request.values.get('pagemetakeywords')
        abouttitle = request.values.get('abouttitle')
        aboutdesc = request.values.get('aboutdesc')
        run1count = request.values.get('run1count')
        run1desc = request.values.get('run1desc')
        run2count = request.values.get('run2count')
        run2desc = request.values.get('run2desc')
        run3count = request.values.get('run3count')
        run3desc = request.values.get('run3desc')
        run4count = request.values.get('run4count')
        run4desc = request.values.get('run4desc')
        aboutimage = request.files['file']
        if aboutimage.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], "about.png")
            aboutimage.save(path)
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(
            'UPDATE about SET aboutpagetitle=%s, aboutpagemeta=%s, aboutpagemetakeyword=%s, about_title=%s,'
            'about_description=%s,runner1count =%s,runner1desc =%s,runner2count=%s,runner2desc=%s,runner3count=%s,'
            'runner3desc=%s,runner4count=%s,runner4desc=%s, aboutimage=%s WHERE id=1',
            (pagetitle, pagemeta, pagemetakeywords, abouttitle, aboutdesc, run1count, run1desc, run2count, run2desc,
             run3count, run3desc, run4count, run4desc, "http://127.0.0.1:5000/static/img/about.png"))
        cur.close()
        return redirect(url_for('admin_crm_about_edit'))
    else:
        return redirect(url_for('admin_crm_about_edit'))


@app.route('/admin/editservicespage/')
def admin_crm_services_edit():
    if session.get('_is_logged_in') is True:
        return render_template('Admin/Services_edit.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/editpricingpage/')
def admin_crm_pricing_edit():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM services')
        service = cur.fetchall()
        cur.close()
        return render_template('Admin/Pricing_edit.html', service=service)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/managepricingparams/', methods=['GET', 'POST'])
def managepricingparams():
    if request.method == 'GET':
        if session.get('_is_logged_in') is True:
            id = request.args.get('id')
            # name = request.args.get('name')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM pricingparams WHERE service_id= %s', id)
            pricingparams = cur.fetchall()
            cur.close()
            return render_template('Admin/Pricing_params_edit.html', pricingparams=pricingparams)
        else:
            return redirect(url_for('admin_login'))
    if request.method == 'POST':
        serid = request.form.get('serid')
        sername = request.form.get('sername')
        param = request.form.get('param')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('INSERT INTO pricingparams (service_id,serviceparam) VALUES (%s,%s)', (serid, param))
        cur.close()
        return redirect(url_for('managepricingparams') + '?id=' + serid + '&name=' + sername)


@app.route('/admin/deletepricingparams/')
def deletepricingparam():
    if session.get('_is_logged_in') is True:
        id = request.args.get('id')
        serid = request.args.get('serid')
        name = request.args.get('name')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM pricingparams WHERE slno = %s', id)
        cur.close()
        return redirect(url_for('managepricingparams') + '?id=' + serid + '&name=' + name)


@app.route('/admin/manageblog/', methods=['GET', 'POST'])
def manageblog():
    blgid = request.args.get('id')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog WHERE id =%s', blgid)
    blgdata = cur.fetchone()
    return render_template('/Admin/manageblog.html', blgdata=blgdata)


@app.route('/admin/manageaboutservices/', methods=['GET', 'POST'])
def aboutservicemanage():
    if request.method == 'GET':
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM aboutservice')
        aboutservice = cur.fetchone()
        return render_template('/Admin/manageaboutservices.html', aboutservice=aboutservice)
    if request.method == 'POST':
        description = request.form.get('description')
        conn = connectMysql()
        cur = conn.cursor()
        try:
            cur.execute('UPDATE aboutservice SET data = %s WHERE slno = 1', description)
            cur.close()
        except pymysql.Error as e:
            print(e)
        return redirect(url_for('aboutservicemanage'))


@app.route('/admin/deleteblog/', methods=['GET', 'POST'])
def delblog():
    blgid = request.args.get('id')
    conn = connectMysql()
    cur = conn.cursor()
    cur.execute('DELETE FROM blog WHERE id = %s', blgid)
    cur.close()
    return redirect(url_for('admin_crm_blog_edit'))


@app.route('/admin/addblog/', methods=['GET', 'POST'])
def addblog():
    if request.method == 'GET':
        if session.get('_is_logged_in') is True:
            return render_template('/admin/addblog.html')
        else:
            return redirect(url_for('admin_login'))
    if request.method == 'POST':
        blogimage = request.files['image']
        if blogimage.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'bloguploads', blogimage.filename)
            dounloadurl = "/static/img/bloguploads/" + blogimage.filename
            blogimage.save(path)
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('INSERT INTO blog (blog_title,blog_description,blog_image,blog_seo_tags) VALUES (%s,%s,%s,%s)',
                        (request.form.get('title'), request.form.get('description'), dounloadurl,
                         request.form.get('tags')))
            cur.close()
            return {
                       'status': 'added success'
                   }, 200


@app.route('/admin/editblogpage/')
def admin_crm_blog_edit():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM blog')
        blogs = cur.fetchall()
        return render_template('Admin/Blog_edit.html', blogs=blogs)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/editcontactpage/')
def admin_crm_contact_edit():
    if session.get('_is_logged_in') is True:
        return render_template('Admin/Contact_edit.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/logout')
def admin_logout():
    session['_is_logged_in'] = False
    session['id'] = None
    session['username'] = ""
    session['name'] = ""
    return redirect(url_for('admin_login'))


@app.route('/userlogout')
def user_logout():
    session['_is_user_logged_in'] = False
    session['firstname'] = None
    session['lastname'] = ""
    session['email'] = ""
    session['password'] = ""
    return redirect(url_for('index'))


@app.route('/admin/orders')
def Orders_admin():
    if session.get('_is_logged_in') is True:
        usernames = []
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table')
        orders = cur.fetchall()
        for row in orders:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users where email = %s', row[1])
            username = cur.fetchone()
            usernames.append(username)
        return render_template('/Admin/Orders.html', orders=orders, usernames=usernames)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/custorders')
def custorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        id = request.args.get('id')
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE user_id = %s', id)
        orders = cur.fetchall()
        return render_template('/Admin/custorders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/pendingorders')
def pending_orders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = %s', 0)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/processingorders')
def processingorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = %s', 1)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/completedorders')
def completedorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = %s', 2)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/cancelledorders')
def cancelledorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = %s', 3)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/verificationorders')
def verificationorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE progress = %s', 4)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/unassignedorders')
def unassignedorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE assigned = %s', 0)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/myassignedorders')
def myassignedorders_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        myid = session.get('username')
        myfname = session.get('name')
        assignedto = myid + " (" + myfname + ")"
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE assigned_to = %s', assignedto)
        orders = cur.fetchall()
        return render_template('/Admin/Orders.html', orders=orders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/users')
def Users_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        return render_template('/Admin/Users.html', users=users)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deleteuser')
def deleteuser():
    if session.get('_is_logged_in') is True:
        id = request.args['id']
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE email = %s', id)
        return redirect(url_for('Users_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/Employees')
def Admin_Employees():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM admin')
        employees = cur.fetchall()
        return render_template('/Admin/employees.html', employees=employees)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deleteemployee')
def admin_deleteemployee():
    if session.get('_is_logged_in') is True:
        id = request.args['id']
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM admin WHERE username=%s', id)
        return redirect(url_for('Admin_Employees'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/add_employee')
def admin_add_employee():
    if session.get('_is_logged_in') is True:
        # conn = connectMysql()
        return render_template('/Admin/addemployee.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/add_employee_admin', methods=['GET', 'POST'])
def admin_add_employee_controller():
    if session.get('_is_logged_in') is True:
        if request.method == 'POST':
            name = request.values.get('name')
            email = request.values.get('email')
            password = request.values.get('password')
            role = request.values.get('role')
            if role == "Admin":
                role = 1
            elif role == "Team Lead":
                role = 2
            elif role == "Employee":
                role = 3
            elif role == "SEO":
                role = 4
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('INSERT INTO admin (username,password,role,name) VALUES (%s,%s,%s,%s)',
                        (email, password, role, name))
            return redirect(url_for('admin_add_employee'))
        else:
            return "METHOD NOT ALLOWED"
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/vieworder')
def admin_vieworder():
    if session.get('_is_logged_in') is True:
        id = request.args['id']
        ordereduser = request.args['ordered_user']
        ordersubid = request.args['order_sub_id']
        session['recent_order_id'] = id
        session['recent_ordered_user_id'] = ordereduser
        session['recent_order_sub_id'] = ordersubid
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM order_table WHERE order_id=%s AND order_sub_id=%s', (id, ordersubid))
        orders = cur.fetchone()
        a = json.loads(orders[3])
        cur = conn.cursor()
        cur.execute('SELECT * FROM admin WHERE role=%s', 3)
        employees = cur.fetchall()
        return render_template('/Admin/vieworders.html', orders=orders, items=a, employees=employees)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/updateorderstatus', methods=['GET', 'POST'])
def admin_updateorderstatus():
    if session.get('_is_logged_in') is True:
        if request.method == 'POST':
            ordereduser = session.get('recent_ordered_user_id')
            ordersubid = session.get('recent_order_sub_id')
            status = request.values.get('status')
            message = request.values.get('message')
            employeeid = request.values.get('employee')
            id = session.get('recent_order_id')
            assignee = session.get('username')
            if status == "Pending":
                status = 0
            elif status == "Processing":
                status = 1
            elif status == "completed":
                status = 2
            elif status == "Cancelled":
                status = 3
            elif status == "Verification Needed":
                status = 4

            if employeeid == "Un-assign":
                assigned = 0
                employeeid = ""
                assignee = ""
            elif employeeid == "Not Assigned":
                assigned = 0
                employeeid = ""
                assignee = ""
            else:
                assigned = 1

            conn = connectMysql()
            cur = conn.cursor()
            cur.execute(
                'UPDATE order_table SET progress = %s,assigned = %s,assigned_to=%s,assigned_by=%s,message=%s WHERE '
                'order_id=%s AND order_sub_id=%s',
                (status, assigned, employeeid, assignee, message, id, ordersubid))
            cur.close()
            # send mail
            # content = "Greetings from aerial estimation,\nStatus for your order with ID
            # :"+id+" is changed to "+request.values.get('status')
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + ordereduser + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:Order Update\n'
            # content = header + content
            # mail.sendmail("devsandy12@gmail.com", ordereduser, content)
            # mail.close()
            return redirect(
                "/admin/vieworder?id=" + id + "&ordered_user=" + ordereduser + "&order_sub_id=" + ordersubid)
        else:
            return "METHOD NOT ALLOWED"
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/editservicepage')
def Admin_editservicepage():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM services')
        service = cur.fetchall()
        return render_template('/Admin/editservice.html', service=service)


@app.route('/admin/add_service', methods=['GET', 'POST'])
def admin_add_service():
    if session.get('_is_logged_in') is True:
        if request.method == "POST":
            title = request.values.get('title')
            desc = request.values.get('description')
            price = request.values.get('price')
            aboutimage = request.files['file']
            if aboutimage.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'serviceuploads', aboutimage.filename)
                dounloadurl = "../static/img/serviceuploads/" + aboutimage.filename
                aboutimage.save(path)
            if request.values.get('multi_enabled') == "Yes":
                multienabled = 1
            else:
                multienabled = 0
            if request.values.get('service_enabled') == "Yes":
                serviceenabled = 1
            else:
                serviceenabled = 0
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO services (service_title,service_desc,isactive,image_url,ismulti,price) VALUES (%s,%s,%s,'
                '%s,%s,%s)',
                (title, desc, serviceenabled, dounloadurl, multienabled, price))
            cur.close()
            return redirect(url_for('Admin_editservicepage'))
        else:

            return render_template('/Admin/addservice.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deleteservice', methods=['GET'])
def admin_deleteservice():
    if session.get('_is_logged_in') is True:
        id = request.args['id']
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('DELETE FROM services WHERE id=%s', id)
        cur.close()
        cur = conn.cursor()
        cur.execute('DELETE FROM serviceparams WHERE id=%s', id)
        cur.close()
        return redirect(url_for('Admin_editservicepage'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/updateservice', methods=['GET', 'POST'])
def admin_updateservice():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            id = request.args['id']
            session['last_selected_service_id_to_update'] = id
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM services WHERE id=%s', id)
            servicedetails = cur.fetchone()
            cur.close()
            return render_template('/Admin/Updateservice.html', servicedetails=servicedetails)
        else:
            id = session.get('last_selected_service_id_to_update')
            title = request.values.get('title')
            desc = request.values.get('description')
            price = request.values.get('price')
            aboutimage = request.files['file']
            if aboutimage.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'serviceuploads', aboutimage.filename)
                dounloadurl = "../static/img/serviceuploads/" + aboutimage.filename
                aboutimage.save(path)
            if request.values.get('multi_enabled') == "Yes":
                multienabled = 1
            else:
                multienabled = 0
            if request.values.get('service_enabled') == "Yes":
                serviceenabled = 1
            else:
                serviceenabled = 0
            conn = connectMysql()
            if aboutimage.filename:
                cur = conn.cursor()
                cur.execute(
                    'UPDATE services SET service_title=%s,service_desc=%s,isactive=%s,image_url=%s,ismulti=%s,'
                    'price=%s WHERE id=%s',
                    (title, desc, serviceenabled, dounloadurl, multienabled, price, id))
                cur.close()
            else:
                cur = conn.cursor()
                cur.execute(
                    'UPDATE services SET service_title=%s,service_desc=%s,isactive=%s,ismulti=%s,price=%s WHERE id=%s',
                    (title, desc, serviceenabled, multienabled, price, id))
                cur.close()
            return redirect(url_for('Admin_editservicepage'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/manageserviceparams', methods=['GET', 'POST'])
def admin_manageserviceparams():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            id = request.args['id']
            session['last_selected_service_id_to_update'] = id
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM serviceparams WHERE id=%s', id)
            serviceparams = cur.fetchall()
            cur.close()
            return render_template('/Admin/manageserviceparams.html', serviceparams=serviceparams)
        else:
            id = session.get('last_selected_service_id_to_update')
            paramid = request.form.get('id')
            parameter = request.form.get('parameter')
            parameterheading = request.form.get('parameterheading')
            type = request.form.get('type')
            Price = request.form.get('price')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('UPDATE serviceparams SET param=%s,paramtype=%s,param_heading=%s,price=%s WHERE slno=%s',
                        (parameter, type, parameterheading, Price, paramid))
            cur.close()
            return redirect('/admin/manageserviceparams?id=' + id)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/add_service_param', methods=['GET', 'POST'])
def admin_add_service_param():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            id = session.get('last_selected_service_id_to_update')
            conn = connectMysql()
            return render_template('/Admin/addserviceparams.html')
        else:
            id = session.get('last_selected_service_id_to_update')
            param_heading = request.values.get('param_heading')
            param = request.values.get('param')
            price = request.values.get('price')
            if request.values.get('param_type') == 'Radio':
                param_type = 0
            if request.values.get('param_type') == 'Text Area(Big)':
                param_type = 1
            if request.values.get('param_type') == 'Upload':
                param_type = 2
            if request.values.get('param_type') == 'Text Field':
                param_type = 3
            if request.values.get('param_type') == 'Check Box':
                param_type = 4
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('INSERT INTO serviceparams (id,param,paramtype,param_heading,price) VALUES (%s,%s,%s,%s,%s)',
                        (id, param, param_type, param_heading, price))
            cur.close()
            return redirect('/admin/manageserviceparams?id=' + id)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deleteserviceparam', methods=['GET', 'POST'])
def admin_deleteserviceparam():
    if session.get('_is_logged_in') is True:
        id = session.get('last_selected_service_id_to_update')
        if request.method == 'GET':
            paramid = request.args['id']
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('DELETE FROM serviceparams WHERE slno=%s', paramid)
            cur.close()
            return redirect('/admin/manageserviceparams?id=' + id)
        else:
            return redirect('/admin/manageserviceparams?id=' + id)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/Usergroups')
def Usergroups_admin():
    if session.get('_is_logged_in') is True:
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM user_groups JOIN group_wallet ON group_wallet.group_id=user_groups.group_id WHERE '
            'user_groups.role=1')
        groups = cur.fetchall()
        return render_template('/Admin/Usergroups.html', groups=groups)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/viewgroup')
def viewgroupUser_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            grpid = request.args.get('id')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM user_groups WHERE group_id = %s', grpid)
            users = cur.fetchall()
            return render_template('/Admin/viewgroupusers.html', users=users)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/viewgrouptransactions', methods=['POST', 'GET'])
def vviewgrouptransactions_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            grpid = request.args.get('id')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM group_wallet_transacctions WHERE group_id = %s', grpid)
            transactions = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT amount FROM group_wallet WHERE group_id = %s', grpid)
            currbal = cur.fetchone()
            return render_template('/Admin/UsergroupsTransactions.html', transactions=transactions, currbal=currbal,
                                   grpid=grpid)
        if request.method == 'POST':
            group_id = request.form.get('userid')
            amount = request.form.get('amount')
            transaction_type = request.form.get('type')
            conn = connectMysql()
            group_transaction_id = "AER_EST_GRP_TRANS_ID-" + str(randrange(111111, 999999))
            try:
                if transaction_type == "1":
                    cur = conn.cursor()
                    cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', group_id)
                    amt = cur.fetchone()
                    upamount = amt[0] + int(amount)
                    cur.close()
                    cur = conn.cursor()
                    cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, group_id))
                    cur.close()
                    cur = conn.cursor()
                    cur.execute(
                        'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,'
                        'transaction_type,group_user_id) VALUES(%s,%s,%s,%s,%s)',
                        (group_transaction_id, group_id, amount, 1, "Admin"))
                    cur.close()
                    return redirect(url_for('vviewgrouptransactions_admin') + "?id=" + group_id)
                if transaction_type == "0":
                    cur = conn.cursor()
                    cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', group_id)
                    amt = cur.fetchone()
                    upamount = amt[0] - int(amount)
                    cur.close()
                    cur = conn.cursor()
                    cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, group_id))
                    cur.close()
                    cur = conn.cursor()
                    cur.execute(
                        'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,'
                        'transaction_type,group_user_id) VALUES(%s,%s,%s,%s,%s)',
                        (group_transaction_id, group_id, amount, 0, "Admin"))
                    cur.close()
                    return redirect(url_for('vviewgrouptransactions_admin') + "?id=" + group_id)
            except pymysql.Error as e:
                return {
                           "msg": str(e)
                       }, 202

    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/transactions', methods=['GET', 'POST'])
def transactions_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            userid = request.args.get('id')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM transaction WHERE user_id = %s', userid)
            transactions = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT wallet_amount FROM users WHERE email = %s', userid)
            currbal = cur.fetchone()
            return render_template('/Admin/transactions.html', transactions=transactions, currbal=currbal,
                                   userid=userid)
        if request.method == 'POST':
            userid = request.form.get('userid')
            amount = request.form.get('amount')
            transaction_type = request.form.get('type')
            conn = connectMysql()
            transaction_id = "AER_EST_TRANS_ID-" + str(randrange(111111, 999999))
            try:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO transaction(transaction_id,user_id,amount_details,transaction_type)VALUES (%s,%s,%s,'
                    '%s)',
                    (transaction_id, userid, amount, transaction_type))
                cur.close()
                if transaction_type == "0":
                    cur = conn.cursor()
                    cur.execute('SELECT wallet_amount FROM users WHERE email = %s', userid)
                    examount = cur.fetchone()
                    cur.close()
                    upamount = examount[0] + int(amount)
                    cur = conn.cursor()
                    cur.execute('UPDATE users SET wallet_amount=%s WHERE email=%s', (upamount, userid,))
                    cur.close()
                    return redirect(url_for('transactions_admin') + "?id=" + userid)
                elif transaction_type == "1":
                    cur = conn.cursor()
                    cur.execute('SELECT wallet_amount FROM users WHERE email = %s', userid)
                    examount = cur.fetchone()
                    cur.close()
                    upamount = examount[0] - int(amount)
                    cur = conn.cursor()
                    cur.execute('UPDATE users SET wallet_amount=%s WHERE email = %s', (upamount, userid,))
                    cur.close()
                    return redirect(url_for('transactions_admin') + "?id=" + userid)
            except pymysql.Error as e:
                return {
                           "msg": str(e)
                       }, 202
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/contactrequests')
def contactrequests_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM contactrequests')
            contactreq = cur.fetchall()
            return render_template('/Admin/contactrequests.html', contactreq=contactreq)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/chat')
def chat_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            id = request.args['id']
            sub_id = request.args['order_sub_id']
            session['selected_id_for_chat'] = id
            session['selected_sub_id_for_chat'] = sub_id
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM order_table')
            orders = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT * FROM chats WHERE order_id = %s AND order_sub_id = %s ORDER BY created_at DESC',
                        (id, sub_id))
            chats = cur.fetchall()
            return render_template('/Admin/chat.html', orders=orders, chats=chats)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/chatinsert', methods=['POST'])
def chatinsert_admin():
    if session.get('_is_logged_in') is True:
        id = session.get('selected_id_for_chat')
        subid = session.get('selected_sub_id_for_chat')
        if request.method == 'POST':
            id = session.get('selected_id_for_chat')
            myusername = session.get('username')
            ordereduser = session.get('recent_ordered_user_id')
            subject = request.form.get('subject')
            message = request.form.get('message')
            aboutimage = request.files['file']
            dounloadurl = ""
            if aboutimage.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'chatuploads', aboutimage.filename)
                dounloadurl = "../static/img/chatuploads/" + aboutimage.filename
                aboutimage.save(path)
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO chats (order_id,sender_id,replyer_id,subject,message,document_url,from_who,to_who,'
                'order_sub_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (id, ordereduser, myusername, subject, message, dounloadurl, 1, 0, subid))
            cur.close()
            # send mail
            # content = "Greetings from aerial estimation,\nYou have a new message for your order with ID
            # :" + id + "\nSubject : " + subject+"\nMessage : "+message+"\nAttachment : "+aboutimage.filename
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + ordereduser + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:New Message\n'
            # content = header + content
            # mail.sendmail("devsandy12@gmail.com", ordereduser, content)
            # mail.close()
            return redirect(
                url_for('chat_admin') + "?id=" + id + "&ordered_user=" + ordereduser + "&order_sub_id=" + subid)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deliverables')
def deliverables_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            id = request.args['id']
            sub_id = request.args['order_sub_id']
            session['selected_id_for_chat'] = id
            session['selected_sub_id_for_chat'] = sub_id
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM order_table')
            orders = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT * FROM deliverables WHERE order_id = %s AND order_sub_id = %s ORDER BY created_at DESC',
                        (id, sub_id))
            deliverables = cur.fetchall()
            return render_template('/Admin/deliverables.html', orders=orders, deliverables=deliverables)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deliverableinsert', methods=['POST'])
def deliverableinsert_admin():
    if session.get('_is_logged_in') is True:
        id = session.get('selected_id_for_chat')
        subid = session.get('selected_sub_id_for_chat')
        if request.method == 'POST':
            id = session.get('selected_id_for_chat')
            myusername = session.get('username')
            ordereduser = session.get('recent_ordered_user_id')
            title = request.form.get('title')
            # addemail = request.form.get('addemail')
            aboutimage = request.files['file']
            dounloadurl = ""
            if aboutimage.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'deliverableuploads', aboutimage.filename)
                dounloadurl = "../static/img/deliverableuploads/" + aboutimage.filename
                aboutimage.save(path)
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO deliverables (order_id,order_sub_id,doc_name,doc_url,uploaded_by) VALUES (%s,%s,%s,%s,%s)',
                (id, subid, title, dounloadurl, myusername))
            cur.close()
            # send mail
            # content = "Greetings from aerial estimation,\nDeliverables for your order with ID :" \
            #           + id + "is delivered please login to finf attachments"
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + ordereduser + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:Deliverables\n'
            # content = header + content
            # mail.sendmail("devsandy12@gmail.com", ordereduser, content)
            # mail.close()
            # if addemail!="" or addemail!=None:
            # content = "Greetings from aerial estimation,\nDeliverables for your order with ID :" + id
            # + "is delivered please login to finf attachments"
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + addemail + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:Deliverables\n'
            # content = header + content
            # mail.sendmail("devsandy12@gmail.com", ordereduser, content)
            # mail.close()
            return redirect(
                url_for('deliverables_admin') + "?id=" + id + "&ordered_user=" + ordereduser + "&order_sub_id=" + subid)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deletedeliverable')
def deletedeliverable_admin():
    if session.get('_is_logged_in') is True:
        delid = request.args.get('id')
        subid = session.get('selected_sub_id_for_chat')
        if request.method == 'GET':
            id = session.get('selected_id_for_chat')
            ordereduser = session.get('recent_ordered_user_id')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('DELETE FROM deliverables WHERE id=%s', delid)
            cur.close()
            return redirect(
                url_for('deliverables_admin') + "?id=" + id + "&ordered_user=" + ordereduser + "&order_sub_id=" + subid)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/coupon', methods=['GET', 'POST'])
def coupon_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM coupon_code')
            coupons = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()
            return render_template('/Admin/coupons.html', coupons=coupons, users=users)
        if request.method == 'POST':
            couponname = request.form.get('couponname')
            couponcode = request.form.get('couponcode')
            discountrate = request.form.get('discountrate')
            enabled = request.form.get('enabled')
            unlimited = request.form.get('unlimited')
            qty = request.form.get('qty')
            usernames = request.form.get('usernames')
            conn = connectMysql()
            try:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO coupon_code (for_user,coupon_name,coupon_code,discount_rate,is_enabled,qty,'
                    'is_unlimited) VALUES(%s,%s,%s,%s,%s,%s,%s)',
                    (usernames, couponname, couponcode, discountrate, enabled, qty, unlimited))
                cur.close()
            except pymysql.Error:
                flash('User already given a code')
            cur = conn.cursor()
            cur.execute('SELECT * FROM coupon_code')
            coupons = cur.fetchall()
            cur.close()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()
            return render_template('/Admin/coupons.html', coupons=coupons, users=users)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deletecoupon', methods=['GET', 'POST'])
def deletecoupon_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            uid = request.args.get('id')
            cur = conn.cursor()
            cur.execute('DELETE FROM coupon_code WHERE for_user = %s', uid)
            cur.close()
            return redirect(url_for('coupon_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/changecouponstatus', methods=['GET', 'POST'])
def changecouponstatus_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            uid = request.args.get('id')
            cur = conn.cursor()
            cur.execute('SELECT is_enabled FROM coupon_code WHERE for_user = %s', uid)
            enabledstatus = cur.fetchone()
            cur.close()
            if enabledstatus[0] == 1:
                enabledstatustoup = 0
            else:
                enabledstatustoup = 1
            cur = conn.cursor()
            cur.execute('UPDATE coupon_code SET is_enabled = %s WHERE for_user=%s', (enabledstatustoup, uid))
            cur.close()
            return redirect(url_for('coupon_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/autodiscount', methods=['GET', 'POST'])
def autodiscount_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM discount_group')
            discount_groups = cur.fetchall()
            return render_template('/Admin/autodiscount.html', discountgroups=discount_groups)
        if request.method == 'POST':
            conn = connectMysql()
            groupname = request.form.get('groupname')
            discountrate = request.form.get('discountrate')
            enabled = request.form.get('enabled')
            message = request.form.get('message')
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO discount_group (group_name,offer_percentage,isenabled,message) VALUES (%s,%s,%s,%s)',
                (groupname, discountrate, enabled, message))
            cur.close()
            return redirect(url_for('autodiscount_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/autodiscountsearch', methods=['GET', 'POST'])
def autodiscountsearch_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            search = request.args.get('search')
            conn = connectMysql()
            cur = conn.cursor()
            query = (
                    "SELECT * FROM `discount_group_users` JOIN discount_group ON "
                    "discount_group_users.discount_group_id=discount_group.id WHERE discount_group_user_id LIKE '" +
                    search + "%';")
            cur.execute(query)
            discount_groups = cur.fetchall()
            return render_template('/Admin/autodiscountsearch.html', discountgroups=discount_groups)
        if request.method == 'POST':
            conn = connectMysql()
            groupname = request.form.get('groupname')
            discountrate = request.form.get('discountrate')
            enabled = request.form.get('enabled')
            message = request.form.get('message')
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO discount_group (group_name,offer_percentage,isenabled,message) VALUES (%s,%s,%s,%s)',
                (groupname, discountrate, enabled, message))
            cur.close()
            return redirect(url_for('autodiscount_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/changedgroupstatus', methods=['GET', 'POST'])
def changedgroupstatus_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            gid = request.args.get('id')
            cur = conn.cursor()
            cur.execute('SELECT isenabled FROM discount_group WHERE id = %s', gid)
            enabledstatus = cur.fetchone()
            cur.close()
            if enabledstatus[0] == 1:
                enabledstatustoup = 0
            else:
                enabledstatustoup = 1
            cur = conn.cursor()
            cur.execute('UPDATE discount_group SET isenabled = %s WHERE id=%s', (enabledstatustoup, gid))
            cur.close()
            return redirect(url_for('autodiscount_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deletedgroup', methods=['GET', 'POST'])
def deletedgroup_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            uid = request.args.get('id')
            cur = conn.cursor()
            cur.execute('DELETE FROM discount_group WHERE id = %s', uid)
            cur.close()
            return redirect(url_for('autodiscount_admin'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/manageusersdgroup', methods=['GET', 'POST'])
def manageusersdgroup_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            dgrpid = request.args.get('id')
            cur = conn.cursor()
            cur.execute(
                'SELECT * FROM discount_group_users JOIN users ON '
                'discount_group_users.discount_group_user_id=users.email WHERE discount_group_id=%s',
                dgrpid)
            users = cur.fetchall()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            usersall = cur.fetchall()
            return render_template('/Admin/manageusersdgroup.html', users=users, usersall=usersall)
        if request.method == 'POST':
            conn = connectMysql()
            dgrpid = request.form.get('groupid')
            dgrpuserid = request.form.get('dgrpuserid')
            grpname = request.form.get('grpname')
            try:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO discount_group_users (discount_group_id,discount_group_user_id) VALUES (%s,%s)',
                    (dgrpid, dgrpuserid))
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE users SET discount_group=%s WHERE email=%s', (grpname, dgrpuserid))
                cur.close()
            except pymysql.Error as e:
                print(e)
            return redirect(url_for('manageusersdgroup_admin') + "?id=" + dgrpid + "&grpname=" + grpname)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deletedgroupuser', methods=['GET', 'POST'])
def deletedgroupuser_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            uid = request.args.get('id')
            userid = request.args.get('userid')
            try:
                cur = conn.cursor()
                cur.execute(
                    'DELETE FROM discount_group_users WHERE discount_group_id = %s AND discount_group_user_id=%s',
                    (uid, userid))
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE users SET discount_group=%s WHERE email=%s', (None, userid))
                cur.close()
            except pymysql.Error as e:
                print(e)
            return redirect(url_for('manageusersdgroup_admin') + "?id=" + uid)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/managecustomers', methods=['GET', 'POST'])
def managecustomers_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            uid = request.args.get('id')
            try:
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE email = %s', uid)
                userdetails = cur.fetchone()
                cur.close()
                cur = conn.cursor()
                cur.execute('SELECT * FROM order_table WHERE user_id = %s', uid)
                userorders = cur.fetchall()
                cur.close()
            except pymysql.Error as e:
                print(e)
            return render_template('/Admin/managecustomers.html', userdetails=userdetails, userorders=userorders)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/wallettransactions', methods=['GET', 'POST'])
def wallettransactions_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            conn = connectMysql()
            totalspent = 0
            listspent = []
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            user = cur.fetchall()
            for i in range(len(user)):
                cur = conn.cursor()
                cur.execute('SELECT amount_details FROM transaction WHERE user_id=%s AND transaction_type=%s',
                            (user[i][2], 0))
                spentmoney = cur.fetchall()
                for j in range(len(spentmoney)):
                    totalspent = totalspent + spentmoney[j][0]
                listspent.append(totalspent)
                totalspent = 0
            return render_template('/Admin/wallettransactions.html', user=user, listspent=listspent)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/viewtransactionsingle', methods=['GET', 'POST'])
def viewtransactionsingle_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            tranid = request.args.get('id')
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('SELECT * FROM transaction WHERE transaction_id = %s', tranid)
            transactions = cur.fetchone()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s', transactions[1])
            userdetails = cur.fetchone()
            return render_template('/Admin/viewtransactionsingle.html', transactions=transactions,
                                   userdetails=userdetails)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/updatecustomer', methods=['GET', 'POST'])
def updatecustomer_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'POST':
            conn = connectMysql()
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            secondarymail = request.form.get('secondarymail')
            billingaddress = request.form.get('billingaddress')
            cur = conn.cursor()
            cur.execute(
                'UPDATE users SET first_name=%s,last_name=%s,password=%s,sec_email=%s,shipping_address=%s WHERE '
                'email=%s',
                (firstname, lastname, password, secondarymail, billingaddress, email))
            cur.close()
            return redirect(url_for('managecustomers_admin') + "?id=" + email)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/resetpasswordlink', methods=['GET', 'POST'])
def resetpasswordlink_admin():
    if session.get('_is_logged_in') is True:
        if request.method == 'GET':
            # conn = connectMysql()
            id = request.args.get('id')
            # cur = conn.cursor()
            # cur.execute('SELECT * FROM users WHERE email = %s', id)
            # account = cur.fetchone()
            # cur.close()
            # if account:
            # content = "Greetings from aerial estimation, Please find password Reset Link for your account : "+id
            # mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            # mail.starttls()
            # mail.login("devsandy12@gmail.com", "sandy@#1234")
            # header = 'To:' + id + '\n' + 'From:' \
            #          + "devsandy12@gmail.com" + '\n' + 'subject:reset password\n'
            # content = header + content
            # mail.sendmail("devsandy12@gmail.com", id, content)
            # mail.close()
            return redirect(url_for('managecustomers_admin') + "?id=" + id)
    else:
        return redirect(url_for('admin_login'))


# *****************************************************************************************************************
# Apis section starts here
# *******************************************************************************************************************
@app.route('/api/create_transaction_grp', methods=['GET', 'POST'])
def create_grp_transaction():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        group_id = data.get('grpid')
        amount = data.get('amount')
        transaction_type = '0'
        conn = connectMysql()
        group_transaction_id = "AER_EST_GRP_TRANS_ID-" + str(randrange(111111, 999999))
        try:
            if transaction_type == "1":
                cur = conn.cursor()
                cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', group_id)
                amt = cur.fetchone()
                upamount = amt[0] + int(amount)
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, group_id))
                cur.close()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,transaction_type,'
                    'group_user_id) VALUES(%s,%s,%s,%s,%s)',
                    (group_transaction_id, group_id, amount, 1, "Admin"))
                cur.close()
                return redirect(url_for('vviewgrouptransactions_admin') + "?id=" + group_id)
            if transaction_type == "0":
                cur = conn.cursor()
                cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', group_id)
                amt = cur.fetchone()
                upamount = amt[0] - int(amount)
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, group_id))
                cur.close()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,transaction_type,'
                    'group_user_id) VALUES(%s,%s,%s,%s,%s)',
                    (group_transaction_id, group_id, amount, 0, user_id))
                cur.close()
                return jsonify(
                    {
                        "message": "ok"
                    }
                ), 200
        except pymysql.Error as e:
            return jsonify(
                {
                    "msg": str(e)
                }
            ), 202


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users(first_name,last_name,email,password)VALUES(%s,%s,%s,%s)',
                        (first_name, last_name, email, password))
            cur.close()
            return jsonify({
                "msg": " REGISTER SUCCESS",
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e.args[1]
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            acct = cur.fetchone()
            cur.close()
            if acct:
                return jsonify({
                    "msg": " LOGIN SUCCESS",
                    "user_details": {
                        "first_name": acct[0],
                        "last_name": acct[1],
                        "email": acct[2],
                        "wallet": acct[5],
                        "secondary_email": acct[7],
                        "billing_address": acct[8],
                    }
                }), 200
            else:
                return jsonify({
                    "msg": "NO USER FOUND"
                }), 202

        except pymysql.Error as e:
            return str(e), 400
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 402


@app.route('/api/getuserprofile', methods=['GET', 'POST'])
def getuserprofile():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s', email)
            acct = cur.fetchone()
            cur.close()
            if acct:
                cur = conn.cursor()
                cur.execute('SELECT * FROM user_groups WHERE user_id = %s', email)
                groups = cur.fetchall()
                cur.close()
                return jsonify({
                    "user_details": {
                        "first_name": acct[0],
                        "last_name": acct[1],
                        "email": acct[2],
                        "wallet": acct[5],
                        "secondaryMail": acct[7],
                        "shipping_address": acct[8],
                        "groups_count": len(groups),
                    }
                }), 200
            else:
                return jsonify({
                    "msg": "NO USER FOUND"
                }), 202

        except pymysql.Error as e:
            return str(e), 400
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 402


@app.route('/api/updateuser', methods=['GET', 'POST'])
def updateuser():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        sec_email = data.get('sec_email')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET first_name=%s,last_name=%s,sec_email=%s WHERE email=%s',
                        (first_name, last_name, sec_email, email))
            cur.close()
            return jsonify({
                "msg": "USER UPDATED",
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e.args[1]
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/updateshippingaddress', methods=['GET', 'POST'])
def updateshippingaddress():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        shipping_address = data.get('shipping_address')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET shipping_address=%s WHERE email=%s', (shipping_address, email))
            cur.close()
            return jsonify({
                "msg": "Shipping address updated",
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e.args[1]
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/updatepassword', methods=['GET', 'POST'])
def updatepassword():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", email)
            acct = cur.fetchone()
            cur.close()
            if acct:
                # content = "Greetings from aerial estimation, Please find your credentials for
                # login\n" + "Username : "\
                #           + acct[2] + "\nPassword : " + acct[3]
                # mail = smtplib.SMTP('smtp.gmail.com', 587)
                # mail.ehlo()
                # mail.starttls()
                # mail.login("devsandy12@gmail.com", "sandy@#1234")
                # header ='To:' + email +'\n' + 'From:'\
                #        +"chandanagowda974@gmail.com" + '\n' + 'subject:resetpassword\n'
                # content = header+content
                # mail.sendmail("devsandy12@gmail.com", email, content)
                # mail.close()
                return "success", 200
            else:
                return "User not exist", 201
        except Exception as ex:
            return str(ex), 205
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallslider', methods=['GET', 'POST'])
def getallslider():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT  * FROM  cart_table WHERE user_id = %s', user_id)
            cartlen = cur.fetchall()
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
        try:
            cur = conn.cursor()
            cur.execute('SELECT  * FROM  introsliders')
            acct = cur.fetchall()
            cur.close()
            d = []
            for row in acct:
                d.append({
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "description": row[3],
                    "image url": row[4],
                })
            return jsonify({
                "msg": d,
                "cartlen": len(cartlen)
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallservices', methods=['GET', 'POST'])
def getallservices():
    if request.method == 'POST':
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT  * FROM  services WHERE isactive=1')
            acct = cur.fetchall()
            cur.close()
            d = []
            paramlist = []
            for row in acct:
                a = {
                    "id": row[0],
                    "service_title": row[1],
                    "service_desc": row[2],
                    "isactive": row[3],
                    "image_url": row[4],
                    "is_multi": row[5],
                    "service_price": row[6]
                }
                cur = conn.cursor()
                cur.execute('SELECT * FROM serviceparams WHERE id =%s', (row[0]))
                params = cur.fetchall()
                cur.close()
                for rows in params:
                    if rows[2] == 0:
                        paramtype = "radio"
                    elif rows[2] == 1:
                        paramtype = "text_area"
                    elif rows[2] == 2:
                        paramtype = "upload"
                    elif rows[2] == 3:
                        paramtype = "text_field"
                    elif rows[2] == 4:
                        paramtype = "check_box"
                    b = {
                        "param_heading": rows[3],
                        "paramtype": paramtype,
                        "param": rows[1],
                        "param_url": rows[4],
                        "param_price": rows[7]
                    }
                    paramlist.append(b)
                    a["params"] = paramlist
                paramlist = []
                d.append(a)
            return jsonify({
                "msg": d
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallpaymentmethods', methods=['GET', 'POST'])
def getallpaymentmethods():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        a = {}
        grp_list = []
        try:
            cur = conn.cursor()
            cur.execute('SELECT pay_pal FROM app_config')
            paypal = cur.fetchone()
            a['paypal_key'] = paypal[0]
            cur = conn.cursor()
            cur.execute('SELECT wallet_amount,first_name,last_name FROM users WHERE email = %s', user_id)
            personal_wallet_amt = cur.fetchone()
            a['user_wallet'] = personal_wallet_amt[0]
            a['username'] = personal_wallet_amt[1] + " " + personal_wallet_amt[2]
            cur.close()
            cur = conn.cursor()
            cur.execute('SELECT group_id , group_name,role FROM user_groups WHERE user_id=%s', user_id)
            usergrp = cur.fetchall()
            if usergrp:
                for row in usergrp:
                    cur = conn.cursor()
                    cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', (row[0]))
                    grp_amount = cur.fetchone()
                    grp_list.append({
                        "group_id": row[0],
                        "group_name": row[1],
                        "role": row[2],
                        "amount": grp_amount[0]}
                    )
            a['group_wallets'] = grp_list
            return a, 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallusergroups', methods=['GET', 'POST'])
def getallusergroups():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        grp_list = []
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM user_groups WHERE user_id=%s', user_id)
            usergrp = cur.fetchall()
            if usergrp:
                for row in usergrp:
                    cur = conn.cursor()
                    cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', (row[0]))
                    grp_amount = cur.fetchone()
                    grp_list.append({
                        "group_id": row[0],
                        "group_name": row[1],
                        "role": row[3],
                        "amount": grp_amount[0]}
                    )
            return jsonify({
                "group_list": grp_list
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/createcart', methods=['GET', 'POST'])
def createcart():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        service_id = data.get('service_id')
        service_param = data.get('service_param')
        service_param = json.dumps(service_param)
        conn = connectMysql()
        cart_id = "AER_EST-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO cart_table(id,user_id,service_id,service_param)VALUES(%s,%s,%s,%s)',
                        (cart_id, user_id, service_id, service_param))
            cur.close()
            return jsonify({
                "msg": "CART CREATED",
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e.args[1]
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallcart', methods=['GET', 'POST'])
def getallcart():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart_table WHERE user_id=%s', user_id)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                cur = conn.cursor()
                cur.execute('SELECT service_title FROM services WHERE id=%s', (row[2]))
                servicename = cur.fetchone()
                cur.close()
                b.append({
                    "id": row[0],
                    "user_id": row[1],
                    "service_id": row[2],
                    "service_name": servicename[0],
                    "service_param": json.loads(row[3]),
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/createorder', methods=['GET', 'POST'])
def createorder():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        progress = data.get('progress')
        items = data.get('items')
        conn = connectMysql()
        order_id = "AER_EST_ORDER-" + str(randrange(10000, 90000))
        for i in range(len(items)):
            try:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO order_table(order_id,user_id,progress,items,order_sub_id)VALUES(%s,%s,%s,%s,%s)',
                    (order_id, user_id, progress, json.dumps(items[i]), i))
                cur.close()
            except pymysql.Error as e:
                return jsonify({
                    "msg": e.args[1]
                }), 202
        return jsonify({
            "msg": "ORDER CREATED"
        }), 200
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/searchuser', methods=['GET', 'POST'])
def searchuser():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            query = ("SELECT * FROM `users` WHERE first_name LIKE '" + email + "%' OR email LIKE '" + email + "';")
            cur.execute(query)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                b.append({
                    "first_name": row[0],
                    "last_name": row[1],
                    "email": row[2],
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return {
                       "msg": e
                   }, 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/creategroup', methods=['GET', 'POST'])
def creategroup():
    if request.method == 'POST':
        data = request.get_json()
        group_name = data.get('group_name')
        user_id = data.get('user_id')
        conn = connectMysql()
        group_id = "AER_EST_GRP_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO user_groups (group_id,group_name,user_id,role) VALUES(%s,%s,%s,%s)',
                        (group_id, group_name, user_id, 1))
            cur.close()
            cur = conn.cursor()
            cur.execute('INSERT INTO group_wallet (group_id,amount) VALUES (%s,%s)', (group_id, 0))
            cur.close()
            return jsonify({
                "msg": " GROUP SUCESSFULLY CREATED"
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": str(e)
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallusersingroup', methods=['GET', 'POST'])
def getallusersingroup():
    if request.method == 'POST':
        data = request.get_json()
        group_id = data.get('group_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM user_groups WHERE group_id=%s', group_id)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                b.append({
                    "group_id": row[0],
                    "group_name": row[1],
                    "user_id": row[2],
                    "role": row[3],
                    "is_added": True,
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/add_user_into_group', methods=['GET', 'POST'])
def add_user_into_group():
    if request.method == 'POST':
        data = request.get_json()
        group_id = data.get('group_id')
        group_name = data.get('group_name')
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO user_groups (user_id,group_id,group_name,role) VALUES (%s,%s,%s,%s)',
                        (user_id, group_id, group_name, "0"))
            cur.close()
            return jsonify({
                "msg": "USER ADDED SUCCESSFULLY INTO GROUPS"
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": str(e)
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/deleteusersingroup', methods=['GET', 'POST'])
def deleteusersingroup():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        group_id = data.get('group_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM user_groups WHERE user_id=%s AND group_id=%s ', (user_id, group_id))
            cur.close()
            return jsonify({
                "msg": "USER DELETED IN GROUP"
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/deletegroup', methods=['GET', 'POST'])
def deletegroup():
    if request.method == 'POST':
        data = request.get_json()
        group_id = data.get('group_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM user_groups WHERE group_id =%s', group_id)
            cur.fetchone()
            cur.close()
            return jsonify({
                "msg": "SUCESS"
            })
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/addmoneyforgroup', methods=['GET', 'POST'])
def addmoneyforgroup():
    if request.method == 'POST':
        data = request.get_json()
        group_id = data.get('group_id')
        amount = data.get('amount')
        user_id = data.get('user_id')
        conn = connectMysql()
        group_transaction_id = "AER_EST_GRP_TRANS_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM  user_groups WHERE user_id=%s AND role=1', user_id)
            user = cur.fetchone()
            cur.close()
            if user:
                cur = conn.cursor()
                cur.execute('SELECT amount FROM group_wallet WHERE group_id=%s', group_id)
                amt = cur.fetchone()
                upamount = amt[0] + int(amount)
                cur.close()
                cur = conn.cursor()
                cur.execute('UPDATE group_wallet SET amount=%s WHERE group_id=%s', (upamount, group_id))
                cur.close()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO group_wallet_transacctions (group_transaction_id,group_id,amount,transaction_type,'
                    'group_user_id) VALUES(%s,%s,%s,%s,%s)',
                    (group_transaction_id, group_id, amount, 1, user_id))
                cur.close()
                return jsonify({
                    "msg": "MONEY ADDED TO THE WALLET SUCCESSFULLY"
                }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": str(e)
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallwallettransaction', methods=['GET', 'POST'])
def getallwallettransaction():
    if request.method == 'POST':
        data = request.get_json()
        group_id = data.get('group_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM group_wallet_transacctions WHERE group_id=%s', group_id)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                b.append({
                    "group_id": row[0],
                    "group_transaction_id": row[1],
                    "amount": row[2],
                    "transaction_type": row[3],
                    "group_user_id": row[5],
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getalltransaction', methods=['GET', 'POST'])
def getalltransaction():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM transaction WHERE user_id=%s', user_id)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                b.append({
                    "transaction_id": row[0],
                    "user_id": row[1],
                    "amount_details": row[2],
                    "transaction_type": row[3],
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/create_transaction', methods=['GET', 'POST'])
def createtransaction():
    if request.method == 'POST':
        data = request.get_json()
        userid = data.get('user_id')
        transaction_type = data.get('transaction_type')
        amount = data.get('amount')
        conn = connectMysql()
        transaction_id = "AER_EST_TRANS_ID-" + str(randrange(111111, 999999))
        try:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO transaction(transaction_id,user_id,amount_details,transaction_type)VALUES (%s,%s,%s,%s)',
                (transaction_id, userid, amount, transaction_type))
            cur.close()
            if transaction_type == 0:
                cur = conn.cursor()
                cur.execute('SELECT wallet_amount FROM users WHERE email = %s', userid)
                examount = cur.fetchone()
                cur.close()
                upamount = examount[0] + int(amount)
                cur = conn.cursor()
                cur.execute('UPDATE users SET wallet_amount=%s WHERE email=%s', (upamount, userid,))
                cur.close()
                return jsonify(
                    {
                        "msg": "MONEY ADDED TO  WALLET SUCCESSFULLY"
                    }
                ), 200
            elif transaction_type == 1:
                cur = conn.cursor()
                cur.execute('SELECT wallet_amount FROM users WHERE email = %s', userid)
                examount = cur.fetchone()
                cur.close()
                upamount = examount[0] - int(amount)
                cur = conn.cursor()
                cur.execute('UPDATE users SET wallet_amount=%s WHERE email = %s', (upamount, userid,))
                cur.close()
                return jsonify(
                    {
                        "msg": "TRANSACTION SUCCESSFULL"
                    }
                ), 200
        except pymysql.Error as e:
            return jsonify(
                {
                    "msg": str(e)
                }
            ), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/deletecart', methods=['GET', 'POST'])
def deletecart():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM cart_table WHERE id =%s', user_id)
            cur.fetchone()
            cur.close()
            return jsonify({
                "msg": "CART DELETED SUCCESSFULLY"
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/detetecartall', methods=['GET', 'POST'])
def deletecartall():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM cart_table WHERE user_id =%s', user_id)
            cur.fetchone()
            cur.close()
            return jsonify({
                "msg": "CART DELETED SUCCESSFULLY"
            })
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202

    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getallorder', methods=['GET', 'POST'])
def getallorder():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM order_table WHERE user_id=%s', user_id)
            user = cur.fetchall()
            cur.close()
            b = []
            for row in user:
                b.append({
                    "order_id": row[0],
                    "user_id": row[1],
                    "progress": row[2],
                    "params": json.loads(row[3]),
                    "created_at": row[4],
                })
            return jsonify({
                "msg": b
            }), 200
        except pymysql.Error as e:
            return jsonify({
                "msg": e
            }), 202
    else:
        return jsonify({
            "msg": "METHOD NOT ALLOWED"
        }), 400


@app.route('/api/getuserlogos', methods=['GET', 'POST'])
def getuserlogos():
    if request.method == 'POST':
        logolist = []
        data = request.get_json()
        user_id = data.get('user_id')
        conn = connectMysql()
        cur = conn.cursor()
        cur.execute('SELECT * FROM userlogos WHERE user_id = %s', user_id)
        logos = cur.fetchall()
        for row in logos:
            logolist.append(row[1])
        return jsonify({
            'logos': logolist
        }), 200


@app.route('/api/uploaduserlogo', methods=['GET', 'POST'])
def uploaduserlogo():
    if request.method == 'POST':
        userid = request.form.get('user')
        logoimage = request.files['logo']
        dounloadurl = ""
        if logoimage.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'userlogouploads', logoimage.filename)
            dounloadurl = "../static/img/userlogouploads/" + logoimage.filename
            logoimage.save(path)
            conn = connectMysql()
            cur = conn.cursor()
            cur.execute('INSERT INTO userlogos (user_id,logo_url) VALUES (%s,%s)', (userid, dounloadurl))
            cur.close()
        return dounloadurl, 200


if __name__ == '__main__':
    app.run(host='127.0.0.1')
