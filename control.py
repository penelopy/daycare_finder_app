from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


# @app.before_request
# def check_login():
# 	user_data = flask_session.get('user')
# 	if user_data and len(user_data) > 1:
# 		g.user_id = user_data[0]
# 		g.user_email = user_data[1]

@app.route('/')
def home_page(): 
	return render_template("login.html")		

@app.route('/parent', methods=['POST'])
def login_p(): 
	username = request.form['username']
	password = request.form['password']
	user = model.db_session.query(model.Parent).filter_by(username=username).filter_by(password=password).first()
	if user: 
		flask_session['user'] = user.id
		flash("Login successful")
		return redirect(url_for('search_page'))
	else: 
		flash("Username/password is invalid")
		# return redirect(url_for('home_page'))

@app.route('/center', methods=['POST'])
def login_d(): 
	username = request.form['username']
	password = request.form['password']
	user_obj = model.db_session.query(model.Center).filter_by(username=username).filter_by(password=password).first()
	if user_obj: 
		flask_session['user'] = user_obj.id
		return redirect(url_for('view_center', user_id=user_obj.id))
		# return redirect(url_for('search_page'))
	else: 
		flash("Username/password is invalid")
		return redirect(url_for('home_page'))



@app.route('/new_parent', methods=['POST'])
def new_parent():
	username = request.form['username']
	password = request.form['password']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']
	new_parent = model.Parent(username = username, password = password, zipcode = zipcode, neighborhood = neighborhood)
	model.db_session.add(new_parent)
	model.db_session.commit()
	print "new parent added: ", new_parent
	return render_template('testing.html', username = username)

@app.route('/par_signup')
def par_signup():
	return render_template('par_signup.html')


@app.route('/new_center', methods=['POST'])
def new_center():
	username = request.form['username']
	password = request.form['password']
	biz_name = request.form['biz_name']
	primary_contact = request.form['primary_contact']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']
	address = request.form['address']
	phone = request.form['phone']
	email = request.form['email']
	web_url = request.form['web_url']
	fb_url = request.form['fb_url']
	yr_in_biz = request.form['yr_in_biz']
	capacity = request.form['capacity']
	num_staff = request.form['num_staff']
	license_num = request.form['license_num']
	about_us = request.form['about_us']

	new_center = model.Center(username = username, password = password, biz_name = biz_name, primary_contact = primary_contact, zipcode = zipcode, neighborhood = neighborhood, address = address, phone = phone, email = email, web_url = web_url, fb_url = fb_url, yr_in_biz = yr_in_biz, capacity = capacity, num_staff = num_staff, license_num = license_num, about_us = about_us)
	model.db_session.add(new_center)
	model.db_session.commit()
	return render_template('testing.html', username = username)

@app.route('/center_signup')
def center_signup():
	return render_template('dc_signup.html')

@app.route('/search_page', methods=['POST'])
def search_page(): 
	zipcode = request.form['zipcode']
	daycare_list = model.db_session.query(model.Center).filter_by(zipcode=zipcode).all()
	return render_template('daycare_list_results.html', daycare_obj_list = daycare_list)

@app.route('/c_register', methods=['POST'])
def process_c_registration(): 
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	primary_contact = request.form['primary_contact']
	biz_name = request.form['biz_name']

	new_center = model.Center(username=username, password=password, email=email, primary_contact=primary_contact, biz_name=biz_name)
	model.db_session.add(new_center)
	model.db_session.commit()	
	return redirect(url_for('view_center', center_id=new_center.id))

@app.route('/viewcenter/<int:center_id>', methods=['GET','POST'])
def view_center(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile.html', daycare_obj = daycare_obj)


# def upload_photo(): 
# 	photo= Photo()


# 	class Photo(Base):
# 	__tablename__ = "photos" 
# 	id = Column(Integer, primary_key = True, nullable=False)
# 	center_id = Column(Integer, ForeignKey('centers.id'), nullable=False)
# 	photo_link = Column(String(100), nullable=False)


if __name__ == "__main__":
    app.run(debug = True)
