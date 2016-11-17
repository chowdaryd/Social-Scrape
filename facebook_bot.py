#---------------------------------------------------------------
#This piece of code was written by Dushyanth NP
#as a research project at Plymouth University
#under the guidance of Dr. Maria Papadaki
#---------------------------------------------------------------

#----------------------Import Statements------------------------
import urllib2
import json
from py2neo import Graph,Node,Relationship

#---------------------Authentication & Request---------------------------------
url_body= 'https://graph.facebook.com/v2.5/'
user = 'me' 
request = '/feed?fields=from%2Cid%2Cname%2Cmessage%2Ccreated_time%2Cshares%2Clikes%7Bname%2Cid%7D%2Ccomments%7Bid%2Cmessage%2Cmessage_tags%2Ccreated_time%2Cfrom%7D%2Clink&'
access_token = 'EAAYuyF6gsNsBACium73cR7hZBaHq7cW9Mc0YQQxPq3IrNhZC3A8ASH1hI0XEMJFmIGq2VMbZBlj1ZAmalQwaManY25JgveK7ZBHOBEaZByeycMPVTbNOoTgoqHFEmlmLpYVuVGZArsTU205cZCaO5d1wP8xlx8IFgwg2Tnw3dZBSsEAZDZD'
url_final = url_body + user + request + 'access_token=' + access_token

#-------------------Database connect----------------------------------
graph = Graph("http://neo4j:Cross@localhost:7474/db/data/")
#---------------------API Code Begins---------------------------------

response = urllib2.urlopen(url_final)

html = response.read()

data = json.loads(html)

#--------------------List all Statuses------------------------------
#---------------Database input code is embedded---------------------
for post in data['data']:
	print '---------------------------------------'
	print '--POST BEGIN--'
	print 'Post id : ' + post['id']
	print 'Created time : ' + post['created_time']
	# post Node Create
	create_new_post = 1
	for record in graph.cypher.execute("MATCH (p:Post) RETURN p.Post_Id AS post_Id"):
		if(post['id'] == record.post_Id ):
			create_new_post = 0
	if(create_new_post == 1):	
		db_post = Node("Post", Post_Id = post['id'], Post_Created = post['created_time'])

		try:
			print 'Message : ' + post['message']
			db_post.properties["Message"] = post['message']
		except KeyError:
			print 'Message : -No message present-'
			pass
		try:
			print 'Story : ' + post['story']
			db_post.properties["Story"] = post['story']
		except KeyError:
			print '-No Story Present-'
			pass
		try:
			print 'Name : ' + post['name']
			db_post.properties["Name"] = post['name']
		except KeyError:
			print '-No Name Present-'
			pass
		print 'Posted By (name): ' + post['from']['name']
		print 'Posted By (Id) : ' + post['from']['id']
		# User Nodes Create
		create_new_user = 1
		for record in graph.cypher.execute("MATCH (u:User) RETURN u.fb_user_id AS user_id,u.fb_Name as fb_Name"):
			if(post['from']['id'] == record.user_id):
				if(record.fb_Name == None):
					graph.cypher.execute("MATCH (u:User) WHERE u.fb_user_id = '"+record.user_id+"' SET u.fb_Name = '"+ post['from']['name']+"'") 
				create_new_user = 0
		if(create_new_user == 1):
			db_user = Node ("User", fb_user_id = post['from']['id'], fb_Name = post['from']['name'])
			db_posted = Relationship(db_user, "POSTED", db_post)
		else:
			db_posted = Relationship(graph.find_one('User','fb_user_id',post['from']['id']), "POSTED", db_post)
		graph.create(db_posted)	
	
		print 'Likes : '
		# User Like Link Nodes Create
		try:
			for like in post['likes']['data']:
				print '--LIKE BEGIN--'
				print like['id']
				print like['name']
				print '--LIKE END--'
				create_new_user = 1
				for record in graph.cypher.execute("MATCH (u:User) RETURN u.fb_user_id AS user_id,u.fb_Name as fb_Name"):
					if(like['id']== record.user_id):
						if(record.fb_Name == None):
							graph.cypher.execute("MATCH (u:User) WHERE u.fb_user_id = '"+record.user_id+"' SET u.fb_Name = '"+ like['name']+"'") 
						create_new_user = 0
				if(create_new_user == 1):
					db_user = Node ("User", fb_user_id = like['id'], fb_Name = like['name'])
					db_liked = Relationship(db_user, "LIKED", db_post)
				else:
					db_liked = Relationship(graph.find_one('User','fb_user_id',like['id']), "LIKED", db_post)
				graph.create(db_liked)	
		except KeyError:
			print 'No Likes'
			pass
		print 'Comments : '
		#User Comment link Nodes
		try:	
			for comment in post['comments']['data']:
				print '--COMMENT BEGIN--'		
				print comment['id']
				print comment['created_time']
				print comment['message']
				create_new_comment = 1
				for record in graph.cypher.execute("MATCH (c:Comment) RETURN c.Comment_Id AS Comment_Id"):
					if(record.Comment_Id == comment['id']):
						create_new_comment = 0
						db_comment = graph.find_one('Comment','Comment_Id',comment['id'])
				if(create_new_comment == 1):	
					db_comment = Node("Comment", Comment_Id = comment['id'], Comment_Created = comment['created_time'], Comment_Message = comment['message'])
				db_commented = Relationship(db_comment, "COMMENTED ON", db_post)
				graph.create(db_commented)
				try:
					print '__User_mentions__ : '
					for usr_cmnt in comment['message_tags']:
						print usr_cmnt['type']		
						print usr_cmnt['id']
						print usr_cmnt['name']
						create_new_user = 1
						for record in graph.cypher.execute("MATCH (u:User) RETURN u.fb_user_id AS user_id,u.fb_Name as fb_Name"):
							if(usr_cmnt['id'] == record.user_id):
								if(record.fb_Name == None):
									graph.cypher.execute("MATCH (u:User) WHERE u.fb_user_id = '"+record.user_id+"' SET u.fb_Name = '"+ usr_cmnt['name']+"'") 
								db_user_men_cmnt = Relationship(db_comment, "USERS MENTIONED", graph.find_one("User","fb_user_id",usr_cmnt['id']))
								graph.create(db_user_men_cmnt)
								create_new_user = 0
						if(create_new_user == 1):			
							db_user_men = Node ("User", fb_user_id = usr_cmnt['id'], fb_Name = usr_cmnt['name'])
							db_user_men_cmnt = Relationship(db_comment, "USERS MENTIONED", db_user_men)
							graph.create(db_user_men_cmnt)
					
				except KeyError:
					print 'No __User_mentions__'
					pass
				try:
					print '__From__ : '					
					print comment['from']['name']
					print comment['from']['id']
					create_new_user = 1
					for record in graph.cypher.execute("MATCH (u:User) RETURN u.fb_user_id AS user_id,u.fb_Name as fb_Name"):
						if(comment['from']['id'] == record.user_id):
							if(record.fb_Name == None):
								graph.cypher.execute("MATCH (u:User) WHERE u.fb_user_id = '"+record.user_id+"' SET u.fb_Name = '"+ comment['from']['name']+"'") 
							create_new_user = 0
					if(create_new_user == 1):
						db_user = Node ("User", fb_user_id = comment['from']['id'], fb_Name = comment['from']['name'])
						db_commented_by = Relationship(db_user, "POSTED", db_comment)
					else:
						db_commented_by = Relationship(graph.find_one('User','fb_user_id',comment['from']['id']), "COMMENTED", db_comment)
					graph.create(db_commented_by)	
				except KeyError:
					print 'No __From__'
					pass
			print '--COMMENT END--'
		except KeyError:
			print 'No Comments'
			pass
		try:
			create_new_link = 1
			for record in graph.cypher.execute("MATCH (U:Url) RETURN U.Url AS Url"):	
				if(post['link'] == record.Url):
					db_url_linked = Relationship(db_post, "URL MENTIONED", graph.find_one('Url','Url',post['link']))
					graph.create(db_url_linked)
					create_new_url = 0			
			if(create_new_link == 1):
				db_url = Node ("Url", Url = post['link'])
				db_url_linked = Relationship(db_post, "URL MENTIONED", db_url)
				graph.create(db_url_linked)
		except KeyError:
			print 'No Link'
			pass
		
	print '--POST END--'
	print '---------------------------------------'
	

