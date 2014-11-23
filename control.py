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

@app.route('/search_page', methods=['GET', 'POST']) #updated and working Tues 11/18
def search_page(): 
	if request.form['zipcode']: 
		zipcode = request.form['zipcode']		
		daycare_list = model.db_session.query(model.Center).filter_by(zipcode=zipcode).all()
		return render_template('daycare_list_results.html', daycare_obj_list = daycare_list)

	else:
		address = request.form['address']
		daycare_list = model.db_session.query(model.Center).filter_by(address=address).all()
		return render_template('daycare_list_results.html', daycare_obj_list = daycare_list)

@app.route('/adv_searchpage')
def advanced_search(): 
	return render_template('advanced_search.html')

@app.route('/process_search', methods=['POST'])
def process_search():

	langs = []
	dc_types = []
	sch = []
	center_lang_list = []
	s_need = []
	c_openings = []
	center_sch_list = []
	center_open_list = []
	center_needs_list = []
	center_zipcode_list = []
	center_type_list = []
	center_city_list = []
	results_dict = {}
	results_list = []
	match_all_list = []
	num_criteria_selected = 0
	no_matches = ""

	for key in request.form.keys():
		if key[0:4] == "lang":
			langs.append(key[4:])
		if key[0:4] == "dtyp":
			dc_types.append(key[4:])
		if key[0:4] == "sche":
			sch.append(key[4:])
		if key[0:4] == "need":
			s_need.append(key[4:])
		if key[0:4] == "cope":
			c_openings.append(key[4:])

	if request.form.get('zipcode'):
		num_criteria_selected += 1
		zipcode = request.form.get('zipcode')
		center_zipcode_list = model.db_session.query(model.Center).filter_by(zipcode = zipcode).all()
		for center in center_zipcode_list: 
		# 	print "center", center.id	
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if request.form.get('address'):
		num_criteria_selected += 1
		address = request.form.get('address')
		center_city_list = model.db_session.query(model.Center).filter_by(address = address).all()
		for center in center_city_list: 
		# 	print "center", center.id
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(langs) > 0: 
		num_criteria_selected += 1
		for lang in langs:
			center_tup_list = model.db_session.query(model.centers_languages).filter_by(language_id = lang).all()
			center_list = []
			for a_tuple in center_tup_list: 
				center_list.append(a_tuple[1])
		for center in center_list: 
			center_obj = model.db_session.query(model.Center).filter_by(id = center).one()
			center_lang_list.append(center_obj)
			for center in center_lang_list: 
			# 	print "center", center.id
				results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(dc_types) > 0: 
		num_criteria_selected += 1
		for item in dc_types: 
			center_type_list = model.db_session.query(model.Center).filter_by(type_of_center_id = item).all()
			for center in center_type_list: 
			# 	print "center", center.id
				results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(sch) > 0: 
		num_criteria_selected += 1
		for item in sch: 
			center_tup_list = model.db_session.query(model.centers_schedules).filter_by(schedule_id = item).all()
			center_list = []
			for a_tuple in center_tup_list: 
				center_list.append(a_tuple[1])
			print "center_list", center_list
		for center in center_list: 
		# 	print "center", center 
			center_obj = model.db_session.query(model.Center).filter_by(id = center).one()
			center_sch_list.append(center_obj)
		# 	print "list = ", center_sch_list
			# if len(center_sch_list) > 0: 
			# 	for center in center_sch_list: 
			# 		print "center", center 
			# 		results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(c_openings) > 0: 
		num_criteria_selected += 1	
		center_open_list = model.db_session.query(model.Center).filter_by(current_openings = True).all()
		for center in center_open_list: 
		# 	print "center", center.id	
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(s_need) > 0: 
		num_criteria_selected += 1		
		center_needs_list = model.db_session.query(model.Center).filter_by(special_needs = True).all()
		for center in center_needs_list: 
			# print "center", center.id
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	for key, value in results_dict.iteritems():
		results_list.append(key)

		if value == num_criteria_selected: 
			center_obj = model.db_session.query(model.Center).filter_by(id = key).one()	

			match_all_list.append(center_obj)

	if len(match_all_list) > 0: 
		no_matches = 1
		# no_matches = "No daycare centers match all of your criteria. Review the sections below to find daycares that meet some of your criteria."
		# print "results list", results_list	
	# print "dict", results_dict

	return render_template('adv_results.html', no_matches = no_matches, match_all_list = match_all_list, center_zip_list=center_zipcode_list, center_lang_list = center_lang_list, center_sch_list = center_sch_list, center_open_list=center_open_list, center_needs_list = center_needs_list, center_city_list=center_city_list, center_type_list = center_type_list)


@app.route('/processtype', methods=['POST']) 
def process_center_type():
	value = request.form.get('id')
	print "value", value
	centers = model.db_session.query(model.Center).filter_by(type_of_center_id= value).all()
	return render_template('daycare_list_results.html', daycare_obj_list = centers)

@app.route('/parent_worksheet')
def parent_worksheet(): 
	return render_template('parent_wksht.html')	

@app.route('/viewcenter/<int:center_id>', methods=['GET','POST']) #working Tues 11/11
def view_center(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile.html', daycare_obj = daycare_obj)

@app.route('/parent_wksht')
def process_par_wksht():
	u = flask_session['user']
	# name = request.form.get('interest')
	# element = request.form.get('id')
	# print "name", name
	wksht_obj = model.db_session.query(model.WorksheetRow).filter_by(id = u).one()
	if request.form.get('interest'):
		wksht_obj.level_of_interest = interest
	if request.form.get('notes'):
		wksht_obj.notes = notes
	if request.form.get('dc_name'):
		wksht_obj.daycare_name = dc_name		

	model.db_session.commit()
	return "Hi"



# @app.route('/wksht_daycare_name', methods=['POST']) #working Fri 11/21
# def select_daycare_name():
# 	u = flask_session['user']
# 	center_typeid = request.form.get('id')
# 	print "type id", center_typeid
# 	center_obj = model.db_session.query(model.Center).filter_by(id = u).one()
# 	center_obj.type_of_center_id = center_typeid

# 	model.db_session.commit()
# 	return "Hi"


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

# @app.route('/editlang', methods=['POST'])
# def edit_lang():
# 	u = flask_session['user']
# 	id = request.form.get('id')
# 	name = request.form.get('name')
# 	print "id", id
# 	print "name", name

# 	# center_obj = model.db_session.query(model.Center).filter_by(id = u).one()
# 	# for id in data: 
# 	# 	print "id", id
# 	# 	center_obj.languages = id 
# 	# model.db_session.commit()

# 	return "Hi"

@app.route('/edittype', methods=['POST']) #working Fri 11/21
def edit_center_type():
	u = flask_session['user']
	center_typeid = request.form.get('id')
	print "type id", center_typeid
	center_obj = model.db_session.query(model.Center).filter_by(id = u).one()
	center_obj.type_of_center_id = center_typeid

	model.db_session.commit()
	return "Hi"

@app.route('/endorse_form', methods=['POST'])
def write_endorse(): 
	print "request", request.form
	id = request.form.get('name')
	print "id", id
	# return "Hi"
	# center_obj = model.db_session.query(model.Center).filter_by(id = id).one()

	return render_template('endorsement_form.html')

@app.route('/process_endorse', methods=['POST'])
def process_endorsement(): 
	u = flask_session['user']
	name = request.form.get('name')
	endorsement= request.form.get('endorsement')

	e_obj = model.db_session.query(model.Endorsement).filter_by(id = name).one()

	e_obj.daycare_id = name
	e_obj.parent_id = u
	e_obj.endorsement = endorsement

	model.db_session.commit()
	return render_template('/')


if __name__ == "__main__":
    app.run(debug = True)
