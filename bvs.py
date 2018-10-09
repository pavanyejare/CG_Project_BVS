#!/usr/bin/python
from flask import Flask, render_template,request, url_for
import os
import datetime
import search
import db
import save_finger

app = Flask(__name__)
@app.route("/")
def home():
	return render_template('home.html')

@app.route("/vote")
def vote():
	return render_template('vote.html')


@app.route('/scan',methods=['POST'])
def scan():
    s = save_finger.write()
    s1 = s[0]
    id= request.form['id']
    acc = request.form['acc']
    vill = request.form['vill']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    data = {'scan' : s[1], 'id' : id, 'acc' : acc, 'vill' : vill, 'name' : name, 'age' : age, 'gender' : gender}
    data1 = { 0 : id, 1 : acc, 2 : vill, 3 : name, 4 : age, 5 : gender, 6 : s1}
    db.store(data1)
    return render_template('regi.html', **data)

@app.route('/find', methods=['POST'])
def find():
        s2 = search.write()
	id = s2[1]
	status = s2[0]
	ack = s2[2]
        if (ack == 0x09):
	  data = {'status' : status , 'ack' : ack, 'msg' : ' You are Not Valid User ! '}
	  return render_template('vote.html', **data)
        elif ack == 0 :
          ser =  db.search(id)
	  status = ser['status']
	  if status == 1 : 
		msg = {'msg' : 'You Are Allready Attempt for Vote !'}
		return render_template('duplicate.html', **msg)
	  else :
 	    return render_template('govote.html', **ser)


if __name__ == "__main__":
     app.run(host="0.0.0.0",port=8080, debug=True)

