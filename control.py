from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


@app.before_request
def check_login(): #working Thurs 11/13
	user_data = flask_session.get('user')
	if user_data:
		g.user_id = user_data

@app.route('/') #working 
def home_page(): 
	return render_template("index2.html")

@app.route('/login')
def login():
	return render_template("login.html")	

#PARENT PAGES	

@app.route('/par_signup') #working Tues 11/11
def par_signup():
	return render_template('par_signup.html')

@app.route('/p_register', methods=['POST']) #working Tues 11/11
def new_par_registration():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']	

	new_parent = model.Parent(first_name = first_name, last_name = last_name, username = username, password = password, email = email, zipcode = zipcode, neighborhood = neighborhood)
	model.db_session.add(new_parent)
	model.db_session.commit()
	return render_template('landing_pg.html', username = new_parent.first_name)

@app.route('/parent', methods=['POST']) #working Tues 11/11
def login_p(): 
	username = request.form['username']
	password = request.form['password']
	user = model.db_session.query(model.Parent).filter_by(username=username).filter_by(password=password).first()
	if user: 
		flask_session['user'] = user.id
		flash("Login successful")
		return render_template('landing_pg.html', username = user.username)
	else: 
		flash("Username/password is invalid")
		# return redirect(url_for('home_page'))

@app.route('/search')
def search():
	return render_template('landing_pg.html')

@app.route('/search_page', methods=['GET', 'POST']) #working Tues 11/11
def search_page(): 
	zipcode = request.form['zipcode']
	daycare_list = model.db_session.query(model.Center).filter_by(zipcode=zipcode).all()
	return render_template('daycare_list_results.html', zipcode=zipcode, daycare_obj_list = daycare_list)

@app.route('/adv_searchpage', methods=['GET', 'POST'])
def advanced_search(): 
	return render_template('advanced_search.html')

@app.route('/process_adv_search')
def process_search():
	pass

@app.route('/parent_worksheet')
def parent_worksheet(): 
	return render_template('parent_wksht.html')	

@app.route('/viewcenter/<int:center_id>', methods=['GET','POST']) #working Tues 11/11
def view_center(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile.html', daycare_obj = daycare_obj)


# USER - DAYCARE CENTER

@app.route('/center_signup') #working Sat 11/15
def center_signup():
	return render_template('dc_signup.html')

@app.route('/c_register', methods=['POST']) # working Tues 11/11
def process_c_registration(): 
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	primary_contact = request.form['primary_contact']
	biz_name = request.form['biz_name']

	new_center = model.Center(username=username, password=password, email=email, primary_contact=primary_contact, biz_name=biz_name)
	model.db_session.add(new_center)
	model.db_session.commit()	
	return redirect(url_for('view_center_private', center_id=new_center.id))	

@app.route('/center', methods=['POST']) #working Tues 11/11
def login_d(): 
	username = request.form['username']
	password = request.form['password']
	center_obj = model.db_session.query(model.Center).filter_by(username=username).filter_by(password=password).first()
	if center_obj: 
		flask_session['user'] = center_obj.id
		return redirect(url_for('view_center_private', center_id = center_obj.id))
	else: 
		flash("Username/password is invalid")
		return redirect(url_for('home_page'))	

@app.route('/viewcenterpri/<int:center_id>', methods=['GET','POST'])  #working Sat 11/15
def view_center_private(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	# return render_template('jedit.html', daycare_obj = daycare_obj)	

	return render_template('center_profile_private.html', daycare_obj = daycare_obj)	

@app.route('/edit_center', methods=['POST'])#working Sat 11/15
def edit_center_profile():

	u = flask_session['user']
	name = request.form.get('name')
	element = request.form.get('id')
	center_obj = model.db_session.query(model.Center).filter_by(id = u).one()
	if element == "email": 
		center_obj.email = name
	elif element == "primary_contact": 
		center_obj.primary_contact = name
	elif element == "zipcode": 
		center_obj.zipcode = name
	elif element == "neighborhood": 
		center_obj.neighborhood = name
	elif element == "hours": 
		center_obj.opening_time = name
	elif element == "phone": 
		center_obj.phone = name
	elif element == "website": 
		center_obj.web_url = name
	elif element == "fb_url": 
		center_obj.fb_url = name
	elif element == "capacity": 
		center_obj.capacity = name  
	elif element == "license_num": 
		center_obj.license_num = name
	elif element == "about_us": 
		center_obj.about_us = name  		
	model.db_session.commit()
	return name

@app.route('/edittype', methods=['POST']) #TODO - incomplete
def edit_center_type():
	u = flask_session['user']
	center_typeid = request.form.get('id')
	print "type id", center_typeid
	center_obj = model.db_session.query(model.Center).filter_by(id = u).one()
	center_obj.type_of_center_id = center_typeid

	model.db_session.commit()
	return "Hi"




if __name__ == "__main__":
    app.run(debug = True)
