#---------------------------------------------------------------
#This piece of code was written by Dushyanth NP
#as a research project at Plymouth University
#under the guidance of Dr. Maria Papadaki
#---------------------------------------------------------------

#----------------------Import Statements------------------------
from py2neo import Graph,Node,Relationship
import plotly.plotly as py
import plotly.graph_objs as go


#-------------------Database connect----------------------------
graph = Graph("http://neo4j:Cross@localhost:7474/db/data/")

#---------------------Code Begins-------------------------------
userno = 0
#----------------Behavior Analytics-----------------------------

for rec in graph.cypher.execute("Match (p:Person)-[r:ACCOUNT]->(u:User) RETURN u.fb_user_id AS FB_User_Id,p.Id AS perid,u.t_user_id AS T_User_Id"):
	userno += 1
	target = graph.find_one("Person","Id",rec.perid)
	#----------------Facebook Posts---------------------------------
	fbp_total_no_posts = 0
	fbp_years = {}
	fbp_months = {}
	fbp_days = {}
	fbp_hrs12 = {}
	fbp_hrs6 = {}
	fbp_hrs = {}
	fbp_mins30 = {}
	fbp_mins15 = {}
	fbp_mins = {}
	if(rec.FB_User_Id != None):
		print rec.perid + "'s Facebook Posts : "
		for record in graph.cypher.execute("MATCH (u:User)-[r:POSTED]->(p:Post) Where u.fb_user_id = '"+rec.FB_User_Id+"' RETURN p.Post_Created AS Post_Created"):
			fbp_total_no_posts += 1	
			print record.Post_Created
			#---------No of Posts by Years--------------	
			if(record.Post_Created[0:4] in fbp_years):	
				fbp_years[record.Post_Created[0:4]] += 1
			else:
				fbp_years[record.Post_Created[0:4]] = 1
			#---------No of Posts by Months-------------
			if(record.Post_Created[0:7] in fbp_months):	
				fbp_months[record.Post_Created[0:7]] += 1
			else:
				fbp_months[record.Post_Created[0:7]] = 1
			#---------No of Posts by Dates--------------
			if(record.Post_Created[0:10] in fbp_days):	
				fbp_days[record.Post_Created[0:10]] += 1
			else:
				fbp_days[record.Post_Created[0:10]] = 1
			#---------No of Posts in 12 hrs-------------
			if(record.Post_Created[11:13] >= "00" and record.Post_Created[11:13] < "12"):
				try:
					fbp_hrs12[record.Post_Created[0:10]+":am"] += 1
				except KeyError:
					fbp_hrs12[record.Post_Created[0:10]+":am"] = 1
			elif(record.Post_Created[11:13] >= "12" and record.Post_Created[11:13] < "24"):
				try:
					fbp_hrs12[record.Post_Created[0:10]+":pm"] += 1
				except KeyError:
					fbp_hrs12[record.Post_Created[0:10]+":pm"] = 1
			#---------No of Posts in 6 hrs-------------
			if(record.Post_Created[11:13] >= "00" and record.Post_Created[11:13] < "06"):
				try:
					fbp_hrs6[record.Post_Created[0:10]+":0to6"] += 1
				except KeyError:
					fbp_hrs6[record.Post_Created[0:10]+":0to6"] = 1
			elif(record.Post_Created[11:13] >= "06" and record.Post_Created[11:13] < "12"):
				try:
					fbp_hrs6[record.Post_Created[0:10]+":6to12"] += 1
				except KeyError:
					fbp_hrs6[record.Post_Created[0:10]+":6to12"] = 1
			elif(record.Post_Created[11:13] >= "12" and record.Post_Created[11:13] < "18"):
				try:
					fbp_hrs6[record.Post_Created[0:10]+":12to18"] += 1
				except KeyError:
					fbp_hrs6[record.Post_Created[0:10]+":12to18"] = 1
			elif(record.Post_Created[11:13] >= "18" and record.Post_Created[11:13] < "24"):
				try:
					fbp_hrs6[record.Post_Created[0:10]+":18to24"] += 1
				except KeyError:
					fbp_hrs6[record.Post_Created[0:10]+":18to24"] = 1
			#---------No od posts every hour-----------
			if(record.Post_Created[0:13] in fbp_hrs):	
				fbp_hrs[record.Post_Created[0:13]] += 1
			else:
				fbp_hrs[record.Post_Created[0:13]] = 1
			#---------No of Posts in 30 mins------------
			if(record.Post_Created[14:16] >= "00" and record.Post_Created[14:16] < "30"):
				try:
					fbp_mins30[record.Post_Created[0:13]+":0to30"] += 1
				except KeyError:
					fbp_mins30[record.Post_Created[0:13]+":0to30"] = 1
			elif(record.Post_Created[14:16] >= "30" and record.Post_Created[11:13] < "60"):
				try:
					fbp_mins30[record.Post_Created[0:13]+":30to60"] += 1
				except KeyError:
					fbp_mins30[record.Post_Created[0:13]+":30to60"] = 1
			#---------No of Posts in 15 mins------------
			if(record.Post_Created[14:16] >= "00" and record.Post_Created[14:16] < "15"):
				try:
					fbp_mins15[record.Post_Created[0:13]+":0to15"] += 1
				except KeyError:
					fbp_mins15[record.Post_Created[0:13]+":0to15"] = 1
			elif(record.Post_Created[14:16] >= "15" and record.Post_Created[14:16] < "30"):
				try:
					fbp_mins15[record.Post_Created[0:13]+":15to30"] += 1
				except KeyError:
					fbp_mins15[record.Post_Created[0:13]+":15to30"] = 1
			elif(record.Post_Created[14:16] >= "30" and record.Post_Created[14:16] < "45"):
				try:
					fbp_mins15[record.Post_Created[0:13]+":30to45"] += 1
				except KeyError:
					fbp_mins15[record.Post_Created[0:13]+":30to45"] = 1
			elif(record.Post_Created[14:16] >= "45" and record.Post_Created[14:16] < "60"):
				try:
					fbp_mins15[record.Post_Created[0:13]+":45to60"] += 1
				except KeyError:
					fbp_mins15[record.Post_Created[0:13]+":45to60"] = 1
			#---------No of Posts every min--------------
			if(record.Post_Created[0:16] in fbp_mins):
				fbp_mins[record.Post_Created[0:16]] += 1
			else:
				fbp_mins[record.Post_Created[0:16]] = 1

		#------------------Print Statements-----------------------------
	
		print "total : "+str(fbp_total_no_posts)
		print "years : "
		print fbp_years
		print "months : "
		print fbp_months
		print "days : "
		print fbp_days
		print "12 hrs : "
		print fbp_hrs12
		print "6 hrs : "
		print fbp_hrs6
		print "hrs : "
		print fbp_hrs
		print "30 mins : "
		print fbp_mins30
		print "15 mins : "
		print fbp_mins15
		print "mins : "
		print fbp_mins
		#--------------Calculating Avg Posts------------------------------
		#------Per Year----------
		if ((int(max(fbp_years)) - int(min(fbp_years)))> 0):
			no_of_years = (int(max(fbp_years)) - int(min(fbp_years)))
		else:
			no_of_years = 1
		yearavg = float(fbp_total_no_posts)/no_of_years
		print "average posts per year : " + str(float(yearavg))
		target.properties["yearavgpost"] = float(yearavg)
		#------Per Month---------
		monthavg = float(fbp_total_no_posts)/(12 * no_of_years)
		print "average posts per month : " + str(float(monthavg))
		target.properties["monthavgpost"] = float(monthavg)
		#------Per Day---------
		dayavg = float(fbp_total_no_posts)/(30*(12 * no_of_years))
		print "average posts per day : " + str(float(dayavg))
		target.properties["dayavgpost"] = float(dayavg)
		#------Every 12 Hours---------
		hrs12avg = float(fbp_total_no_posts)/(2*(30*(12 * no_of_years)))
		print "average posts every 12 hours : " + str(float(hrs12avg))
		target.properties["hrs12avgpost"] = float(hrs12avg)
		#------Every 6 Hours----------
		hrs6avg = float(fbp_total_no_posts)/(4*(30*(12 * no_of_years)))
		print "average posts every 6 hours : " + str(float(hrs6avg))
		target.properties["hrs6avgpost"] = float(hrs6avg)
		#------Every Hour-------------
		hravg = float(fbp_total_no_posts)/(24*(30*(12 * no_of_years)))
		print "average posts every hour : " + str(float(hravg))
		target.properties["hrsavgpost"] = float(hravg)
		#------Every 30 Mins---------
		min30avg = float(fbp_total_no_posts)/(2*(24*(30*(12 * no_of_years))))
		print "average posts every 30 mins : " + str(float(min30avg))
		target.properties["min30avgpost"] = float(min30avg)
		#------Every 15 Mins----------
		min15avg = float(fbp_total_no_posts)/(4*(24*(30*(12 * no_of_years))))
		print "average posts every 15 mins : " + str(float(min15avg))
		target.properties["min15avgpost"] = float(min15avg)
		#------Every Mins-------------
		minavg = float(fbp_total_no_posts)/(60*(24*(30*(12 * no_of_years))))
		print "average posts every min : " + str(float(minavg))
		target.properties["minavgpost"] = float(minavg)
		target.push()

		#----------------Facebook Comments---------------------------------
		print rec.perid + "'s Facebook Comments : "
		fbc_total_no_comments = 0
		fbc_years = {}
		fbc_months = {}
		fbc_days = {}
		fbc_hrs12 = {}
		fbc_hrs6 = {}
		fbc_hrs = {}
		fbc_mins30 = {}
		fbc_mins15 = {}
		fbc_mins = {}

		for record in graph.cypher.execute("MATCH (u:User)-[r:COMMENTED]->(c:Comment) Where u.fb_user_id = '"+rec.FB_User_Id+"' RETURN c.Comment_Created AS Comment_Created"):
			fbc_total_no_comments += 1	
			print record.Comment_Created
			#---------No of Comments by Years--------------	
			if(record.Comment_Created[0:4] in fbc_years):	
				fbc_years[record.Comment_Created[0:4]] += 1
			else:
				fbc_years[record.Comment_Created[0:4]] = 1
			#---------No of Comments by Months-------------
			if(record.Comment_Created[0:7] in fbc_months):	
				fbc_months[record.Comment_Created[0:7]] += 1
			else:
				fbc_months[record.Comment_Created[0:7]] = 1
			#---------No of Comments by Dates--------------
			if(record.Comment_Created[0:10] in fbc_days):	
				fbc_days[record.Comment_Created[0:10]] += 1
			else:
				fbc_days[record.Comment_Created[0:10]] = 1
			#---------No of Comments in 12 hrs-------------
			if(record.Comment_Created[11:13] >= "00" and record.Comment_Created[11:13] < "12"):
				try:
					fbc_hrs12[record.Comment_Created[0:10]+":am"] += 1
				except KeyError:
					fbc_hrs12[record.Comment_Created[0:10]+":am"] = 1
			elif(record.Comment_Created[11:13] >= "12" and record.Comment_Created[11:13] < "24"):
				try:
					fbc_hrs12[record.Comment_Created[0:10]+":pm"] += 1
				except KeyError:
					fbc_hrs12[record.Comment_Created[0:10]+":pm"] = 1
			#---------No of Comments in 6 hrs-------------
			if(record.Comment_Created[11:13] >= "00" and record.Comment_Created[11:13] < "06"):
				try:
					fbc_hrs6[record.Comment_Created[0:10]+":0to6"] += 1
				except KeyError:
					fbc_hrs6[record.Comment_Created[0:10]+":0to6"] = 1
			elif(record.Comment_Created[11:13] >= "06" and record.Comment_Created[11:13] < "12"):
				try:
					fbc_hrs6[record.Comment_Created[0:10]+":6to12"] += 1
				except KeyError:
					fbc_hrs6[record.Comment_Created[0:10]+":6to12"] = 1
			elif(record.Comment_Created[11:13] >= "12" and record.Comment_Created[11:13] < "18"):
				try:
					fbc_hrs6[record.Comment_Created[0:10]+":12to18"] += 1
				except KeyError:
					fbc_hrs6[record.Comment_Created[0:10]+":12to18"] = 1
			elif(record.Comment_Created[11:13] >= "18" and record.Comment_Created[11:13] < "24"):
				try:
					fbc_hrs6[record.Comment_Created[0:10]+":18to24"] += 1
				except KeyError:
					fbc_hrs6[record.Comment_Created[0:10]+":18to24"] = 1
			#---------No of Comments every hour-----------
			if(record.Comment_Created[0:13] in fbc_hrs):	
				fbc_hrs[record.Comment_Created[0:13]] += 1
			else:
				fbc_hrs[record.Comment_Created[0:13]] = 1
			#---------No of Comments in 30 mins------------
			if(record.Comment_Created[14:16] >= "00" and record.Comment_Created[14:16] < "30"):
				try:
					fbc_mins30[record.Comment_Created[0:13]+":0to30"] += 1
				except KeyError:
					fbc_mins30[record.Comment_Created[0:13]+":0to30"] = 1
			elif(record.Comment_Created[14:16] >= "30" and record.Comment_Created[11:13] < "60"):
				try:
					fbc_mins30[record.Comment_Created[0:13]+":30to60"] += 1
				except KeyError:
					fbc_mins30[record.Comment_Created[0:13]+":30to60"] = 1
			#---------No of Comments in 15 mins------------
			if(record.Comment_Created[14:16] >= "00" and record.Comment_Created[14:16] < "15"):
				try:
					fbc_mins15[record.Comment_Created[0:13]+":0to15"] += 1
				except KeyError:
					fbc_mins15[record.Comment_Created[0:13]+":0to15"] = 1
			elif(record.Comment_Created[14:16] >= "15" and record.Comment_Created[14:16] < "30"):
				try:
					fbc_mins15[record.Comment_Created[0:13]+":15to30"] += 1
				except KeyError:
					fbc_mins15[record.Comment_Created[0:13]+":15to30"] = 1
			elif(record.Comment_Created[14:16] >= "30" and record.Comment_Created[14:16] < "45"):
				try:
					fbc_mins15[record.Comment_Created[0:13]+":30to45"] += 1
				except KeyError:
					fbc_mins15[record.Comment_Created[0:13]+":30to45"] = 1
			elif(record.Comment_Created[14:16] >= "45" and record.Comment_Created[14:16] < "60"):
				try:
					fbc_mins15[record.Comment_Created[0:13]+":45to60"] += 1
				except KeyError:
					fbc_mins15[record.Comment_Created[0:13]+":45to60"] = 1
			#---------No of Comments every min--------------
			if(record.Comment_Created[0:16] in fbc_mins):	
				fbc_mins[record.Comment_Created[0:16]] += 1
			else:
				fbc_mins[record.Comment_Created[0:16]] = 1

		#------------------Print Statements-----------------------------
		print "total : "+str(fbc_total_no_comments)
		print "years : "
		print fbc_years
		print "months : "
		print fbc_months
		print "days : "
		print fbc_days
		print "12 hrs : "
		print fbc_hrs12
		print "6 hrs : "
		print fbc_hrs6
		print "hrs : "
		print fbc_hrs
		print "30 mins : "
		print fbc_mins30
		print "15 mins : "
		print fbc_mins15
		print "mins : "
		print fbc_mins
		#--------------Calculating Avg Posts------------------------------
		if(fbc_total_no_comments != 0):
			#------Per Year----------
			if ((int(max(fbc_years)) - int(min(fbc_years)))> 0):
				no_of_years = (int(max(fbc_years)) - int(min(fbc_years)))
			else:
				no_of_years = 1
			yearavg = float(fbc_total_no_comments)/no_of_years
			print "average Comments per year : " + str(float(yearavg))
			target.properties["yearavgcom"] = float(yearavg)
			#------Per Month---------
			monthavg = float(fbc_total_no_comments)/(12 * no_of_years)
			print "average Comments per month : " + str(float(monthavg))
			target.properties["monthavgcom"] = float(monthavg)
			#------Per Day---------
			dayavg = float(fbc_total_no_comments)/(30*(12 * no_of_years))
			print "average Comments per day : " + str(float(dayavg))
			target.properties["dayavgcom"] = float(dayavg)
			#------Every 12 Hours---------
			hrs12avg = float(fbc_total_no_comments)/(2*(30*(12 * no_of_years)))
			print "average Comments every 12 hours : " + str(float(hrs12avg))
			target.properties["hrs12avgcom"] = float(hrs12avg)
			#------Every 6 Hours----------
			hrs6avg = float(fbc_total_no_comments)/(4*(30*(12 * no_of_years)))
			print "average Comments every 6 hours : " + str(float(hrs6avg))
			target.properties["hrs6avgcom"] = float(hrs6avg)
			#------Every Hour-------------
			hravg = float(fbc_total_no_comments)/(24*(30*(12 * no_of_years)))
			print "average Comments every hour : " + str(float(hravg))
			target.properties["hrsavgcom"] = float(hravg)
			#------Every 30 Mins---------
			min30avg = float(fbc_total_no_comments)/(2*(24*(30*(12 * no_of_years))))
			print "average Comments every 30 mins : " + str(float(min30avg))
			target.properties["min30avgcom"] = float(min30avg)
			#------Every 15 Mins----------
			min15avg = float(fbc_total_no_comments)/(4*(24*(30*(12 * no_of_years))))
			print "average Comments every 15 mins : " + str(float(min15avg))
			target.properties["min15avgcom"] = float(min15avg)
			#------Every Mins-------------
			minavg = float(fbc_total_no_comments)/(60*(24*(30*(12 * no_of_years))))
			print "average Comments every min : " + str(float(minavg))
			target.properties["minavgcom"] = float(minavg)
		target.push()


	#----------------Twitter tweets---------------------------------
	tt_total_no_posts = 0
	tt_years = {}
	tt_months = {}
	tt_days = {}
	tt_hrs12 = {}
	tt_hrs6 = {}
	tt_hrs = {}
	tt_mins30 = {}
	tt_mins15 = {}
	tt_mins = {}
	if(rec.T_User_Id != None):
		print rec.perid + "'s Twitter Tweets : "
		for record in graph.cypher.execute("MATCH (u:User)-[r:TWEETED]->(t:Tweet) Where u.t_user_id = '"+rec.T_User_Id+"' RETURN t.Tweet_Created AS Tweet_Created"):
			tt_total_no_posts += 1	
			print record.Tweet_Created
			#---------No of Tweets by Years--------------	
			if(record.Tweet_Created[0:4] in tt_years):	
				tt_years[record.Tweet_Created[0:4]] += 1
			else:
				tt_years[record.Tweet_Created[0:4]] = 1
			#---------No of Tweets by Months-------------
			if(record.Tweet_Created[0:7] in tt_months):	
				tt_months[record.Tweet_Created[0:7]] += 1
			else:
				tt_months[record.Tweet_Created[0:7]] = 1
			#---------No of Tweets by Dates--------------
			if(record.Tweet_Created[0:10] in tt_days):	
				tt_days[record.Tweet_Created[0:10]] += 1
			else:
				tt_days[record.Tweet_Created[0:10]] = 1
			#---------No of Tweetts in 12 hrs-------------
			if(record.Tweet_Created[11:13] >= "00" and record.Tweet_Created[11:13] < "12"):
				try:
					tt_hrs12[record.Tweet_Created[0:10]+":am"] += 1
				except KeyError:
					tt_hrs12[record.Tweet_Created[0:10]+":am"] = 1
			elif(record.Tweet_Created[11:13] >= "12" and record.Tweet_Created[11:13] < "24"):
				try:
					tt_hrs12[record.Tweet_Created[0:10]+":pm"] += 1
				except KeyError:
					tt_hrs12[record.Tweet_Created[0:10]+":pm"] = 1
			#---------No of Tweets in 6 hrs-------------
			if(record.Tweet_Created[11:13] >= "00" and record.Tweet_Created[11:13] < "06"):
				try:
					tt_hrs6[record.Tweet_Created[0:10]+":0to6"] += 1
				except KeyError:
					tt_hrs6[record.Tweet_Created[0:10]+":0to6"] = 1
			elif(record.Tweet_Created[11:13] >= "06" and record.Tweet_Created[11:13] < "12"):
				try:
					tt_hrs6[record.Tweet_Created[0:10]+":6to12"] += 1
				except KeyError:
					tt_hrs6[record.Tweet_Created[0:10]+":6to12"] = 1
			elif(record.Tweet_Created[11:13] >= "12" and record.Tweet_Created[11:13] < "18"):
				try:
					tt_hrs6[record.Tweet_Created[0:10]+":12to18"] += 1
				except KeyError:
					tt_hrs6[record.Tweet_Created[0:10]+":12to18"] = 1
			elif(record.Tweet_Created[11:13] >= "18" and record.Tweet_Created[11:13] < "24"):
				try:
					tt_hrs6[record.Tweet_Created[0:10]+":18to24"] += 1
				except KeyError:
					tt_hrs6[record.Tweet_Created[0:10]+":18to24"] = 1
			#---------No od Tweets every hour-----------
			if(record.Tweet_Created[0:13] in fbp_hrs):	
				tt_hrs[record.Tweet_Created[0:13]] += 1
			else:
				tt_hrs[record.Tweet_Created[0:13]] = 1
			#---------No of Tweets in 30 mins------------
			if(record.Tweet_Created[14:16] >= "00" and record.Tweet_Created[14:16] < "30"):
				try:
					tt_mins30[record.Tweet_Created[0:13]+":0to30"] += 1
				except KeyError:
					tt_mins30[record.Tweet_Created[0:13]+":0to30"] = 1
			elif(record.Tweet_Created[14:16] >= "30" and record.Tweet_Created[11:13] < "60"):
				try:
					tt_mins30[record.Tweet_Created[0:13]+":30to60"] += 1
				except KeyError:
					tt_mins30[record.Tweet_Created[0:13]+":30to60"] = 1
			#---------No of Tweets in 15 mins------------
			if(record.Tweet_Created[14:16] >= "00" and record.Tweet_Created[14:16] < "15"):
				try:
					tt_mins15[record.Tweet_Created[0:13]+":0to15"] += 1
				except KeyError:
					tt_mins15[record.Tweet_Created[0:13]+":0to15"] = 1
			elif(record.Tweet_Created[14:16] >= "15" and record.Tweet_Created[14:16] < "30"):
				try:
					tt_mins15[record.Tweet_Created[0:13]+":15to30"] += 1
				except KeyError:
					tt_mins15[record.Tweet_Created[0:13]+":15to30"] = 1
			elif(record.Tweet_Created[14:16] >= "30" and record.Tweet_Created[14:16] < "45"):
				try:
					tt_mins15[record.Tweet_Created[0:13]+":30to45"] += 1
				except KeyError:
					tt_mins15[record.Tweet_Created[0:13]+":30to45"] = 1
			elif(record.Tweet_Created[14:16] >= "45" and record.Tweet_Created[14:16] < "60"):
				try:
					tt_mins15[record.Tweet_Created[0:13]+":45to60"] += 1
				except KeyError:
					tt_mins15[record.Tweet_Created[0:13]+":45to60"] = 1
			#---------No of Tweets every min--------------
			if(record.Tweet_Created[0:16] in tt_mins):
				tt_mins[record.Tweet_Created[0:16]] += 1
			else:
				tt_mins[record.Tweet_Created[0:16]] = 1

		#------------------Print Statements-----------------------------
	
		print "total : "+str(tt_total_no_posts)
		print "years : "
		print tt_years
		print "months : "
		print tt_months
		print "days : "
		print tt_days
		print "12 hrs : "
		print tt_hrs12
		print "6 hrs : "
		print tt_hrs6
		print "hrs : "
		print tt_hrs
		print "30 mins : "
		print tt_mins30
		print "15 mins : "
		print tt_mins15
		print "mins : "
		print tt_mins
		#--------------Calculating Avg Posts------------------------------
		#------Per Year----------
		if ((int(max(tt_years)) - int(min(tt_years)))> 0):
			no_of_years = (int(max(tt_years)) - int(min(tt_years)))
		else:
			no_of_years = 1
		yearavg = float(tt_total_no_posts)/no_of_years
		print "average tweets per year : " + str(float(yearavg))
		target.properties["yearavgtweet"] = float(yearavg)
		#------Per Month---------
		monthavg = float(tt_total_no_posts)/(12 * no_of_years)
		print "average tweets per month : " + str(float(monthavg))
		target.properties["monthavgtweet"] = float(monthavg)
		#------Per Day---------
		dayavg = float(tt_total_no_posts)/(30*(12 * no_of_years))
		print "average tweets per day : " + str(float(dayavg))
		target.properties["dayavgtweet"] = float(dayavg)
		#------Every 12 Hours---------
		hrs12avg = float(tt_total_no_posts)/(2*(30*(12 * no_of_years)))
		print "average tweets every 12 hours : " + str(float(hrs12avg))
		target.properties["hrs12avgtweet"] = float(hrs12avg)
		#------Every 6 Hours----------
		hrs6avg = float(tt_total_no_posts)/(4*(30*(12 * no_of_years)))
		print "average tweets every 6 hours : " + str(float(hrs6avg))
		target.properties["hrs6avgtweet"] = float(hrs6avg)
		#------Every Hour-------------
		hravg = float(tt_total_no_posts)/(24*(30*(12 * no_of_years)))
		print "average tweets every hour : " + str(float(hravg))
		target.properties["hrsavgtweet"] = float(hravg)
		#------Every 30 Mins---------
		min30avg = float(tt_total_no_posts)/(2*(24*(30*(12 * no_of_years))))
		print "average tweets every 30 mins : " + str(float(min30avg))
		target.properties["min30avgtweet"] = float(min30avg)
		#------Every 15 Mins----------
		min15avg = float(tt_total_no_posts)/(4*(24*(30*(12 * no_of_years))))
		print "average tweets every 15 mins : " + str(float(min15avg))
		target.properties["min15avgtweet"] = float(min15avg)
		#------Every Mins-------------
		minavg = float(tt_total_no_posts)/(60*(24*(30*(12 * no_of_years))))
		print "average tweets every min : " + str(float(minavg))
		target.properties["minavgtweet"] = float(minavg)
		target.push()


	#--------Ploty API to Plot Graphs----------------------
	#--------Graph for Posts Every Year---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	
	for key, value in dict.iteritems(fbp_years):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_years):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_years):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2,trace3]
	layout = go.Layout(title="Posts And Tweets Per Year", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='yeargraph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["yeargraphlink"] = first_plot_url
	target.push()
'''	#--------Graph for Posts Every Month---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]

	for key, value in dict.iteritems(fbp_months):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_months):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_months):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Per Month", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='monthgraph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["monthgraphlink"] = first_plot_url
	#--------Graph for Posts Every Day---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_days):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_days):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_days):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Per Day", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='daygraph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["daygraphlink"] = first_plot_url
	#--------Graph for Posts Every 12 Hours---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_hrs12):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_hrs12):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_hrs12):
		tt_axis.append(key)
		tt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every 12 hours", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='hrs12graph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["hrs12graphlink"] = first_plot_url
	#--------Graph for Posts Every 6 Hours---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_hrs6):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_hrs6):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_hrs6):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every 6 hours", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='hrs6graph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["hrs6graphlink"] = first_plot_url
	#--------Graph for Posts Every Hour---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_hrs):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_hrs):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')	
	for key, value in dict.iteritems(tt_hrs):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xc_axis, y = yc_axis,name='Tweets')	
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every hour", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='hrsgraph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["hrsgraphlink"] = first_plot_url
	#--------Graph for Posts Every 30 Minutes---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_mins30):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_mins30):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_mins30):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every 30 Minutes", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='mins30graph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["min30graphlink"] = first_plot_url
	#--------Graph for Posts Every 15 Minutes---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_mins15):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_mins15):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_mins15):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2,trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every 15 Minutes", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='mins15graph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["min15graphlink"] = first_plot_url
	#--------Graph for Posts Every Minute---------------	
	xp_axis=[]
	yp_axis=[]
	xc_axis=[]
	yc_axis=[]
	xt_axis=[]
	yt_axis=[]
	for key, value in dict.iteritems(fbp_mins):
		xp_axis.append(key)
		yp_axis.append(value)
	trace1 = go.Bar(x = xp_axis, y = yp_axis,name='Posts')
	for key, value in dict.iteritems(fbc_mins):
		xc_axis.append(key)
		yc_axis.append(value)
	trace2 = go.Bar(x = xc_axis, y = yc_axis,name='Comments')
	for key, value in dict.iteritems(tt_mins):
		xt_axis.append(key)
		yt_axis.append(value)
	trace3 = go.Bar(x = xt_axis, y = yt_axis,name='Tweets')	
	data = [trace1,trace2,Trace3]
	layout = go.Layout(title=rec.FB_User_Id+"'s Posts And Tweets Every Minute", barmode= 'group',width=800, height=640)
	
	first_plot_url = py.plot(data, filename='minsgraph'+str(userno), layout=layout, auto_open=False,)
	print first_plot_url
	target.properties["mingraphlink"] = first_plot_url
'''
