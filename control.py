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

@app.route('/edit_center', methods=['POST'])#TODO using center_profile_view.html create this view. will have to update db entry. render template should show center profile page
def edit_center_profile():
	u = flask_session['user'][0]

	# email = request.form['email']
	# primary_contact = request.form['primary_contact']
	biz_name = request.form['biz_name']
	# zipcode = request.form['zipcode']
	# neighborhood = request.form['neighborhood']
	# address = request.form['address']
	# phone = request.form['phone']
	# email = request.form['email']
	# web_url = request.form['web_url']
	# fb_url = request.form['fb_url']
	# yr_in_biz = request.form['yr_in_biz']
	# capacity = request.form['capacity']
	# num_staff = request.form['num_staff']
	# license_num = request.form['license_num']
	# about_us = request.form['about_us']

	center_obj = model.db_session.query(model.Center).filter_by(user_id = u).one()
	# center_obj.email = email
	# center_obj.primary_contact = primary_contact
	center_obj.biz_name = biz_name
	# center_obj.zipcode = zipcode
	# center_obj.neighborhood = neighborhood
	# center_obj.address = address
	# center_obj.phone = phone
	# center_obj.email = email
	# center_obj.web_url = web_url
	# center_obj.fb_url = fb_url
	# center_obj.yr_in_biz = yr_in_biz
	# center_obj.capacity = capacity
	# center_obj.num_staff = num_staff
	# center_obj.license_num = license_num
	# center_obj.about_us = about_us

	model.db_session.commit()
	return redirect(url_for('view_center_private', center_id = center_obj.id))

@app.route('/center_signup')
def center_signup():
	return render_template('dc_signup.html')

@app.route('/search_page', methods=['GET', 'POST']) #working Tues 11/11
def search_page(): 
	zipcode = request.form['zipcode']
	daycare_list = model.db_session.query(model.Center).filter_by(zipcode=zipcode).all()
	return render_template('daycare_list_results.html', zipcode=zipcode, daycare_obj_list = daycare_list)

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

@app.route('/viewcenterpri/<int:center_id>', methods=['GET','POST'])  
def view_center_private(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile_private.html', daycare_obj = daycare_obj)	

@app.route('/viewcenter/<int:center_id>', methods=['GET','POST']) #working Tues 11/11
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
