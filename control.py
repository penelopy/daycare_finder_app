"""control.py contains all the main functions for this app"""

from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def home_page(): 
	return render_template("index2.html")

################################################################
"""LOG IN FUNCTIONS"""

@app.before_request
def check_login(): 
	"""Checks flask session for currently logged in users and 
		sets global variables"""
	g.daycare_center_id = flask_session.get('daycare_center_id')
	g.parent_id = flask_session.get('parent_id')
	g.logged_in = flask_session.get('logged_in', False)

@app.route('/logout')
def logout():
	"""Checks flask session for specific user, resets global 
		variables and redirects to homepage"""
	flask_session['logged_in'] = False
	if "daycare_center_id" in flask_session: 
		del flask_session['daycare_center_id']
	if "parent_id" in flask_session:
		del flask_session['parent_id']	
	return redirect(url_for('home_page'))


@app.route('/login')
def login():
	"""Renders login page or flashes message if user is already logged in"""
	if g.logged_in:
		flash("Already signed in. Signout to change user profiles.")
		return redirect(url_for('home_page'))
	else:
		return render_template("login.html")

#PARENT PAGES##############################################################

@app.route('/par_signup')
def par_signup():
	"""Renders parent signup/registration page"""
	return render_template('par_signup.html')

@app.route('/p_register', methods=['POST'])
def new_par_registration():
	"""Processes html form information from parent registration page and 
	saves data to parent table in database.
	Redirects user to search page to locate daycares"""

	first_name = request.form['first_name']
	last_name = request.form['last_name']
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']

	new_parent = model.Parent(first_name = first_name, 
							  last_name = last_name, 
							  username = username, 
							  password = password, 
							  email = email, 
							  zipcode = zipcode, 
							  neighborhood = neighborhood)
	model.db_session.add(new_parent)
	model.db_session.commit()
	return redirect(url_for('search'))

@app.route('/parent', methods=['POST'])
def login_p(): 
	"""Receives username and password, queries 'parent' table in database and   
		either saves user into flask session or flashes screen to indicate
		invalid user/password input"""

	username = request.form['username']
	password = request.form['password']
	user = model.db_session.query(model.Parent).filter_by(username=username
				).filter_by(password=password).first()
	if user: 
		flask_session['parent_id'] = user.id
		flask_session['logged_in'] = True
		return redirect(url_for('parent_worksheet'))
	else: 
		flash("Username/password is invalid")

@app.route('/search')
def search():
	"""Displays location-based search page"""
	return render_template('landing_pg.html')

@app.route('/search_page', methods=['GET', 'POST'])
def search_page(): 
	"""Processes location-based search request by querying database
		and displays daycare listings"""

	if request.form['zipcode']: 
		zipcode = request.form['zipcode']		
		daycare_list = model.db_session.query(model.Center).filter_by(
			zipcode=zipcode).all()
		if daycare_list == []: 
			flash("No results match your search criteria")
			return redirect(url_for('search'))
		else:
			return render_template('alt_search_results.html', daycare_obj_list = daycare_list)

	elif request.form['address']:
		address = request.form['address']
		daycare_list = model.db_session.query(model.Center).filter_by(
			address=address).all()
		if daycare_list == []: 
			flash("No results match your search criteria")
			return redirect(url_for('search'))
		else:	
			return render_template('alt_search_results.html', daycare_obj_list = daycare_list)


@app.route('/adv_searchpage')
def advanced_search(): 
	"""Displays advanced search page"""
	return render_template('advanced_search.html')

@app.route('/process_search', methods=['POST'])
def process_search():
	"""Processes search input from AJAX or HTML form, queries 'center' table in 
	database, complies and renders a results list page"""
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
	# match_all_list = []
	# final_match_list = []
	values_list = []
	num_criteria_selected = 0

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
		center_zipcode_list = model.db_session.query(model.Center).filter_by(
			zipcode = zipcode).all()
		for center in center_zipcode_list: 
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if request.form.get('address'):
		num_criteria_selected += 1
		address = request.form.get('address')
		center_city_list = model.db_session.query(model.Center).filter_by(
			address = address).all()
		for center in center_city_list: 
		# 	print "center", center.id
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(langs) > 0: 
		num_criteria_selected += 1
		for lang in langs:
			center_tup_list = model.db_session.query(model.centers_languages
				).filter_by(language_id = lang).all()
			center_list = []
			for a_tuple in center_tup_list: 
				center_list.append(a_tuple[1])
		for center in center_list: 
			center_obj = model.db_session.query(model.Center).filter_by(id = center).one()
			center_lang_list.append(center_obj)
		for center in center_lang_list: 
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(dc_types) > 0: 
		num_criteria_selected += 1
		for item in dc_types: 
			center_type_list = model.db_session.query(model.Center).filter_by(
				type_of_center_id = item).all()
			for center in center_type_list: 
				results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(sch) > 0: 
		num_criteria_selected += 1
		for item in sch: 
			center_tup_list = model.db_session.query(model.centers_schedules).filter_by(
				schedule_id = item).all()
			center_list = []
			for a_tuple in center_tup_list: 
				center_list.append(a_tuple[1])
		for center in center_list: 
			center_obj = model.db_session.query(model.Center).filter_by(id = center).one()
			center_sch_list.append(center_obj)
		for center in center_sch_list: 
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(c_openings) > 0: 
		num_criteria_selected += 1	
		center_open_list = model.db_session.query(model.Center).filter_by(
			current_openings = True).all()
		for center in center_open_list: 
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	if len(s_need) > 0: 
		num_criteria_selected += 1		
		center_needs_list = model.db_session.query(model.Center).filter_by(
			special_needs = True).all()
		for center in center_needs_list: 
			results_dict[center.id] = results_dict.setdefault(center.id , 0) + 1

	output_tup_list= sorted(results_dict.items(), key=lambda x: x[1], reverse=True)
	print output_tup_list

	for i in range(len(output_tup_list)):
		center_obj = model.db_session.query(model.Center).filter_by(
			id = output_tup_list[i][0]).one()	
		results_list.append(center_obj)

	print "results list", results_list
	print "results dict", results_dict
	return render_template('adv_results_ext.html', results_list=results_list)


@app.route('/processtype', methods=['POST']) 
def process_center_type():
	""" """
	value = request.form.get('id')
	centers = model.db_session.query(model.Center).filter_by(type_of_center_id= value).all()
	return render_template('daycare_list_results.html', daycare_obj_list = centers)

@app.route('/parent_worksheet')
def parent_worksheet(): 
	"""Displays the private parent worksheet page"""
	p = g.parent_id
	wksht_rows = model.db_session.query(model.WorksheetRow).filter_by(parent_id=p).all()
	endorsements = model.db_session.query(model.Endorsement).filter_by(parent_id=p).all()

	if len(wksht_rows) > 0: 
		return render_template('parent_wksht.html', wksht_rows = wksht_rows, 
			endorsements=endorsements)
	else: 
		return render_template('parent_wksht.html')

@app.route('/viewcenter/<int:center_id>', methods=['GET','POST'])
def view_center(center_id):
	"""Processes user selection (click) by querying database and displays 
	individual daycare page"""
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile.html', daycare_obj = daycare_obj)

@app.route('/sendwksht', methods=['POST'])
def send_to_worksheet():
	"""Processes selected daycare id by querying database and either adds daycare 
	to parent worksheet or flashes message to screen that the daycare 
	already exists on worksheet"""
	p = g.parent_id
	daycare_id = request.form.get('daycare_id')
	daycare_list = model.db_session.query(model.WorksheetRow).filter_by(
		parent_id = p).filter_by(daycare_id = daycare_id).all()
	if len(daycare_list) >0:
		flash("This daycare already exists on your worksheet")
		return redirect(url_for('parent_worksheet'))		
	else: 	
		new_row = model.WorksheetRow(parent_id = p, daycare_id = daycare_id)
		model.db_session.add(new_row)
		model.db_session.commit()
		return redirect(url_for('parent_worksheet'))

@app.route('/parent_wksht', methods=['POST'])
def process_par_wksht():
	"""Uses AJAX (see 'custom_editing.js' file) to create user on-screen 
	editing of parent worksheet fields. Saves new information to database and 
	displays edited information on-screen"""
	p = g.parent_id
	value = request.form.get('value')
	element = request.form.get('id')
	daycareid = element[1:]
	wksht_obj = model.db_session.query(model.WorksheetRow).filter_by(
		parent_id = p).filter_by(daycare_id=daycareid).one()
	if element[0] == "i":
		wksht_obj.level_of_interest = value
	if element[0] == "n":
		wksht_obj.notes = value
	model.db_session.commit()
	return value

@app.route('/delete_daycare', methods=['POST'])
def delete_daycare():
	"""Works with AJAX (see 'custom_editing.js' file) and deletes daycare from 
	parent worksheet"""
	if g.parent_id: 
		wkshtid = request.form.get('wkshtid')
		daycare = model.db_session.query(model.WorksheetRow).filter_by(id = wkshtid).all()
		if daycare == []:
			return "No record"
		daycare = daycare[0]
		model.db_session.delete(daycare)
		model.db_session.commit()
		return "OK"
	else: 
		flash("Log in to use this feature.")
		return redirect(url_for('login_p'))

#DAYCARE CENTER USERS ###########################################################

@app.route('/center_signup')
def center_signup():
	"""Renders daycare center signup page"""
	return render_template('dc_signup.html')

@app.route('/c_register', methods=['POST'])
def process_c_registration(): 
	"""Processes daycare registration items from HTML form, queries database and 
	returns private and editable daycare center page"""
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	primary_contact = request.form['primary_contact']
	biz_name = request.form['biz_name']

	new_center = model.Center(username=username, 
							  password=password, 
							  email=email, 
							  primary_contact=primary_contact, 
							  biz_name=biz_name)
	model.db_session.add(new_center)
	model.db_session.commit()	
	return redirect(url_for('view_center_private', center_id=new_center.id))	

@app.route('/center', methods=['POST'])
def login_d(): 
	"""Processes username/password from HTML form, queries database and returns
	private and editable daycare center page"""
	username = request.form['username']
	password = request.form['password']
	center_obj = model.db_session.query(model.Center).filter_by(username=username
		).filter_by(password=password).first()
	if center_obj: 
		flask_session['daycare_center_id'] = center_obj.id
		flask_session['logged_in'] = True
		return redirect(url_for('view_center_private', center_id = center_obj.id))
	else: 
		flash("Username/password is invalid")
		return redirect(url_for('home_page'))	

@app.route('/viewcenterpri/<int:center_id>', methods=['GET','POST'])  
def view_center_private(center_id):
	d = center_id
	daycare_obj = model.db_session.query(model.Center).get(d)
	return render_template('center_profile_private.html', daycare_obj = daycare_obj)	

@app.route('/edit_center', methods=['POST'])
def edit_center_profile():

	u = flask_session['daycare_center_id']
	name = request.form.get('name')
	element = request.form.get('id')
	print "name=", name
	print "element", element
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

@app.route('/edittype', methods=['POST']) 
def edit_center_type():
	d = flask_session['daycare_center_id']
	center_typeid = request.form.get('id')
	center_obj = model.db_session.query(model.Center).filter_by(id = d).one()
	center_obj.type_of_center_id = center_typeid
	model.db_session.commit()
	return "OK"

@app.route('/sendendorse', methods=['POST'])
def send_to_endorse_form():
	p = g.parent_id
	daycare_id = request.form.get('daycare_id')
	exist_endorse = model.db_session.query(model.Endorsement).filter_by(
		daycare_id = daycare_id, parent_id =p).all()
	if len(exist_endorse) == 0: 
		new_endorse = model.Endorsement(parent_id = p, daycare_id = daycare_id)
		model.db_session.add(new_endorse)
		model.db_session.commit()
		endorse_obj_list = model.db_session.query(model.Endorsement).filter_by(
			parent_id = p).filter_by(daycare_id = daycare_id).all()
		return render_template('endorsement_form.html', endorse_obj_list = endorse_obj_list)
	else:
		flash("You've already endorsed this daycare")
		return redirect(url_for('parent_worksheet'))


@app.route('/process_endorse', methods=['POST'])
def process_endorsement(): 
	p = g.parent_id
	center_id= request.form.get('center_id')
	endo_text = request.form.get('endo_text')
	e_obj = model.db_session.query(model.Endorsement).filter_by(daycare_id = center_id
		).filter_by(parent_id=p).one()
	e_obj.endorsement = endo_text
	model.db_session.commit()
	return redirect(url_for('parent_worksheet'))


if __name__ == "__main__":
    app.run(debug = True)
