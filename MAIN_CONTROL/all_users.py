from firebase import firebase
from flask import Flask,render_template

#SETTING UP FIREBASE REALTIME DATABASE APPLICATION
firebase1 = firebase.FirebaseApplication('https://pro11255.firebaseio.com', None)
api_key = 'IF0tXyGaqNfQB9aR2PBDQrOVwZ3p3VT0BxZe_IuxqAU'



del_message = firebase1.delete('/message','')

#GEOFENCE COORDINATES IN IITH CAMPUSS
lat_boys = [17.596896,17.596941,17.598011, 17.598093]
long_boys = [78.127400,78.125364,78.125201,78.127497]


lat_girls=[17.596470,17.596486,17.595534,17.595637]
long_girls = [78.125499,78.126276,78.126341,78.125397]


lat_FTL= [17.585779, 17.585779,17.584225,17.584225]
long_FTL=[78.117980, 78.119922,78.119922,78.117980]


lat_FTR= [17.585207,17.585207,17.584153,17.584153]
long_FTR=[78.120695,78.122036,78.122036,78.120695]



app = Flask(__name__)

#ADDING ROUTE TO ALL THE USERS IN ONE MAP 
#AUTOMATICALLLY UPDATES THE LOCATION OF EACH USER USING THE APP
@app.route('/')
def map_func():
	#GETTING ALL THE INFORMATION OF THE USERS IN THE DATABASE
	results = firebase1.get('/','')
	latitude = list()
	longitude = list()
	roll = list()
	name = list()
	cell_no = list()
	time = list()
	#SAVING ALL VALUES OF THE USERS IN A SEPERATE LIST BASED ON THE CATEGORY OF LATITUDE,LONGITUDE,TIME,PHONE NUMBER,NAME
	#KEY IS PHONE NUMBER OF THE USER TO EXTACT DATA FROM THE DATABASE
	for keys in results.keys():
		latitude.append(results[keys]['latitude'])
		longitude.append(results[keys]['longitude'])
		roll.append(results[keys]['rollNumber'])
		name.append(results[keys]['name'])
		time.append(results[keys]['currentTime'])
		cell_no.append(keys)


	# GENERATING ALERTS FOR USERS REGARDING DIFFERENT GEOFENCES 

	alert = list()



	min_lat_boys = min(lat_boys)
	max_lat_boys = max(lat_boys)
	min_long_boys = min(long_boys)
	max_long_boys = max(long_boys)
	for (i,j) in zip(latitude,longitude):
		if (i>=min_lat_boys and i<= max_lat_boys and j>=min_long_boys and j<=max_long_boys):
			alert.append("  INTRUSION IN BOYS HOSTEL BY "+str(name[latitude.index(i)])+", "+str(cell_no[latitude.index(i)])+", "+str(time[latitude.index(i)])+", "+str(roll[latitude.index(i)]))

	min_lat_girls = min(lat_girls)
	max_lat_girls = max(lat_girls)
	min_long_girls = min(long_girls)
	max_long_girls = max(long_girls)
	for (i,j) in zip(latitude,longitude):
		if (i>=min_lat_girls and i<= max_lat_girls and j>=min_long_girls and j<=max_long_girls):
			alert.append("  INTRUSION IN GIRLS HOSTEL BY "+str(name[latitude.index(i)])+", "+str(cell_no[latitude.index(i)])+", "+str(time[latitude.index(i)])+", "+str(roll[latitude.index(i)]))

	min_lat_FTL = min(lat_FTL)
	max_lat_FTL = max(lat_FTL)
	min_long_FTL = min(long_FTL)
	max_long_FTL = max(long_FTL)
	for (i,j) in zip(latitude,longitude):
		if (i>=min_lat_FTL and i<= max_lat_FTL and j>=min_long_FTL and j<=max_long_FTL):
			alert.append("  INTRUSION IN FACULTY TOWER LEFT BUILDING BY "+str(name[latitude.index(i)])+", "+str(cell_no[latitude.index(i)])+", "+str(time[latitude.index(i)])+", "+str(roll[latitude.index(i)]))

	min_lat_FTR = min(lat_FTR)
	max_lat_FTR = max(lat_FTR)
	min_long_FTR = min(long_FTR)
	max_long_FTR = max(long_FTR)
	for (i,j) in zip(latitude,longitude):
		if (i>=min_lat_FTR and i<= max_lat_FTR and j>=min_long_FTR and j<=max_long_FTR):
			alert.append("  INTRUSION IN STAFF TOWER RIGHT BUILDING BY "+str(name[latitude.index(i)])+", "+str(cell_no[latitude.index(i)])+", "+str(time[latitude.index(i)])+", "+str(roll[latitude.index(i)]))

	if len(alert)==0:
		alert = "  NO INTRUSION IN ANY OF THE GEOFENCE"

	#RENDERING MAP WITH MARKERS AS SYMBOL FOR EACH USER
	alert = list(set(alert))
	return render_template('map2_updated.html',apikey=api_key,latitude=latitude,longitude=longitude,len=len(latitude),alert = alert, roll=roll,name=name,cell_no=cell_no)

#ADDING ROUTES TO LOCATE REAL-TIME LOCATION OF A SINGLE USER BASED THE PHONE NUMBER
@app.route('/<phone_number>')
def trace(phone_number):
	#RETRIEVING DETAILS OF USER USING PHONE NUMBER FROM DATABASE 
	phone_number = str(phone_number)
	results1 = firebase1.get('/'+phone_number,'')
	name = results1['name']
	lat_new = results1['latitude']
	long_new = results1['longitude']
	time = results1['currentTime']
	date = results1['currentDate']
	roll_number = results1['rollNumber']
	
	# GENERATING ALERTS
	alert1 = "  NO INTRUSION IN ANY OF THE GEOFENCE"

	min_lat_boys = min(lat_boys)
	max_lat_boys = max(lat_boys)
	min_long_boys = min(long_boys)
	max_long_boys = max(long_boys)


	if (lat_new >=min_lat_boys and lat_new <= max_lat_boys and long_new >=min_long_boys and long_new <=max_long_boys):
		alert1 = "  INTRUSION IN BOYS HOSTEL BY "+str(name)+" "+str(roll_number)+" at"+" " +" "+str(time)

	min_lat_girls = min(lat_girls)
	max_lat_girls = max(lat_girls)
	min_long_girls = min(long_girls)
	max_long_girls = max(long_girls)
	if (lat_new >=min_lat_girls and lat_new <= max_lat_girls and long_new >=min_long_girls and long_new <=max_long_girls):
		alert1 = "  INTRUSION IN GIRLS HOSTEL BY "+str(name)+" "+str(roll_number)+" at"+" " +" "+str(time)

	min_lat_FTL = min(lat_FTL)
	max_lat_FTL = max(lat_FTL)
	min_long_FTL = min(long_FTL)
	max_long_FTL = max(long_FTL)
	
	if (lat_new >=min_lat_FTL and lat_new <= max_lat_FTL and long_new >=min_long_FTL and long_new <=max_long_FTL):
		alert1 = "  INTRUSION IN FACULTY TOWER LEFT BUILDING BY "+str(name)+" "+str(roll_number)+" at"+" " +" "+str(time)

	min_lat_FTR = min(lat_FTR)
	max_lat_FTR = max(lat_FTR)
	min_long_FTR = min(long_FTR)
	max_long_FTR = max(long_FTR)
	if (lat_new >=min_lat_FTR and lat_new <= max_lat_FTR and long_new >=min_long_FTR and long_new <=max_long_FTR):
		alert1 = "  INTRUSION IN STAFF TOWER RIGHT BUILDING BY "+str(name)+" "+str(roll_number)+" at"+" " +" "+str(time)

	#PRODUCING MAP FOR A SINGLE USER AT A TIME WITH SYNTAX AS HTTP://127.0.0.1:5000/PHONE NUMBER OR LOCAL HOST/PHONE NUMBER
	return render_template('map_single.html',apikey=api_key,latitude1=lat_new,longitude1=long_new,alert1 = alert1,name = name)

@app.route('/D')
def defaulters():
	results = firebase1.get('/','')
	roll = list()
	name = list()
	cell_no = list()
	times = list()
	dates = list()
	#SAVING ALL VALUES OF THE USERS IN A SEPERATE LIST BASED ON THE CATEGORY OF LATITUDE,LONGITUDE,TIME,PHONE NUMBER,NAME
	#KEY IS PHONE NUMBER OF THE USER TO EXTACT DATA FROM THE DATABASE
	for keys in results.keys():
		roll.append(results[keys]['rollNumber'])
		name.append(results[keys]['name'])
		times.append(results[keys]['currentTime'])
		dates.append(results[keys]['currentDate'])
		cell_no.append(keys)

	from datetime import datetime
	from datetime import date

	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = date.today()
	current_date = today.strftime("%d-%m-%Y")

	defaulters =list()

	for i in range(len(times)):
		if current_date == dates[i]:
			temp1 = abs(int(current_time[:2])-int(times[i][:2]))
			if temp1>=2:
				defaulters.append("  Last updated location of {} {} was {} hours ago".format(name[i],roll[i],temp1))
			else:
				defaulters=[]
		else:
			temp1 = abs(int(current_date[:2])-int(dates[i][:2]))
			defaulters.append("  Last updated location of {} {} was {} days ago".format(name[i],roll[i],temp1))


	return render_template('defaulter.html',defaulters = defaulters)





if __name__ == '__main__':
    app.run(debug = False)


