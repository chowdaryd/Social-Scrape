#---------------------------------------------------------------
#This piece of code was written by Dushyanth NP
#as a research project at Plymouth University
#under the guidance of Dr. Maria Papadaki
#---------------------------------------------------------------

#----------------------Import Statements------------------------
import tweepy
from py2neo import Graph,Node,Relationship

#---------------------Authentication---------------------------------
consumer_key = "mhXKnV6222SS6pXZTJwiiwNxP"
consumer_secret = "EF5Br7gBdZKO1NGOH5tVhynWszHHI1Tz33JZNEDAvzGKjdRajt"
access_token = "4898833480-Q35ZwRvq0bLYJfZmi9FYaMWH9bxJnY3tW0vjtzS"
access_token_secret = "HtzsKqtvrHRF6jI6YtEzOiJzrzLzXW6bRHNyzSA0bKTnQ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#-------------------Database connect----------------------------------
graph = Graph("http://neo4j:Cross@localhost:7474/db/data/")
#---------------------API Code Begins---------------------------------

api = tweepy.API(auth)

home_tweets = api.home_timeline()

#--------------------List all Statuses------------------------------

print "--- Statuses ---"
for tweet in home_tweets:
	print "---------------------------------------" + "\n"
	print "Name:", tweet.author.name.encode('utf8')
    	print "Screen-name:", tweet.author.screen_name.encode('utf8')
	print "User's Unique Id : ", tweet.user.id_str
    	print "Tweet created:", tweet.created_at
	print "Tweet Id : " + tweet.id_str
    	print "Tweet:", tweet.text.encode('utf8')
	print "Hashtags : "	
	for hasht in tweet.entities['hashtags']:
		print hasht['text']
	print "User Mentions : "
	for user_men in tweet.entities['user_mentions']:
		print user_men['id_str']
		print user_men['screen_name']
		print user_men['name']
	print "Urls : "
	for url in tweet.entities['urls']:
		print url['expanded_url']
	print "Retweeted Count:", tweet.retweet_count
	print "Favourited Count:", tweet.favorite_count
    	print "Location:", tweet.user.location.encode('utf8')
    	print "Time-zone:", tweet.user.time_zone
	print "Geo : ", tweet.geo
	print "---------------------------------------" + "\n"

	#--------------------Code for Database Input----------------
	# Tweet Node Create
	create_new_tweet = 1
	for record in graph.cypher.execute("MATCH (t:Tweet) RETURN t.Tweet_Id AS Tweet_Id"):
		if(record.Tweet_Id == tweet.id_str):
			create_new_tweet = 0
	if(create_new_tweet == 1):
		db_tweet = Node("Tweet", Tweet_Id = tweet.id_str, Tweet_Created = tweet.created_at, Tweet_Text = tweet.text.encode('utf8'), Retweeted_Count = tweet.retweet_count, Favorited_Count = tweet.favorite_count)
		if(tweet.user.location.encode('utf8')!= None):
			db_tweet.properties["Location"] = tweet.user.location.encode('utf8')
		if(tweet.user.time_zone != None):	
			db_tweet.properties["Time_Zone"] = tweet.user.time_zone
	
		# User Nodes Create
		create_new_user = 1
		for record in graph.cypher.execute("MATCH (u:User) RETURN u.t_user_id AS user_id,u.t_Name as t_Name"):
			if(tweet.user.id_str == record.user_id):
				if(record.t_Name == None):
					graph.cypher.execute("MATCH (u:User) WHERE u.t_user_id = '"+record.user_id+"' SET u.t_Name = '"+ tweet.author.name.encode('utf8')+"',u.t_Screen_Name = '"+tweet.author.screen_name.encode('utf8')+"'")
				create_new_user = 0
		if(create_new_user == 1):
			db_user = Node ("User", t_user_id = tweet.user.id_str, t_Name = tweet.author.name.encode('utf8'), t_Screen_Name = tweet.author.screen_name.encode('utf8'))
			db_tweeted = Relationship(db_user, "TWEETED", db_tweet)
		else:
			db_tweeted = Relationship(graph.find_one('User','t_user_id',tweet.user.id_str), "TWEETED", db_tweet)
		graph.create(db_tweeted)
	
		# HashTag Node Create
		for hasht in tweet.entities['hashtags']:
			create_new_hashtag = 1
			for record in graph.cypher.execute("MATCH (h:Hashtag) RETURN h.HashTag_Text AS HashTag_Text"):
				if(hasht['text'] == record.HashTag_Text):
					db_hashtaged = Relationship(db_tweet, "HASHTAGED", graph.find_one('Hashtag','HashTag_Text',hasht['text']))
					graph.create(db_hashtaged)
					create_new_hashtag = 0	
			if(create_new_hashtag == 1):	
				db_hash = Node ("Hashtag", HashTag_Text = hasht['text'])
				db_hashtaged = Relationship(db_tweet, "HASHTAGED", db_hash)
				graph.create(db_hashtaged)
	
		# Url Node Create
		for url in tweet.entities['urls']:
			create_new_url = 1
			for record in graph.cypher.execute("MATCH (U:Url) RETURN U.Url AS Url"):	
				if(url['expanded_url'] == record.Url):
					db_url_linked = Relationship(db_tweet, "URL MENTIONED", graph.find_one('Url','Url',url['expanded_url']))
					graph.create(db_url_linked)
					create_new_url = 0			
			if(create_new_url == 1):
				db_url = Node ("Url", Url = url['expanded_url'])
				db_url_linked = Relationship(db_tweet, "URL MENTIONED", db_url)
				graph.create(db_url_linked)				
		
		# User Mention Node Create
		for user_men in tweet.entities['user_mentions']:
			create_new_user = 1
			for record in graph.cypher.execute("MATCH (u:User) RETURN u.t_user_id AS user_id,u.t_Name as t_Name"):
				if(user_men['id_str'] == record.user_id):
					if(record.t_Name == None):
						graph.cypher.execute("MATCH (u:User) WHERE u.t_user_id = '"+record.user_id+"' SET u.t_Name = '"+ user_men['name']+"',u.t_Screen_Name = '"+user_men['screen_name']+"'")	
					db_user_men_tweet = Relationship(db_tweet, "USERS MENTIONED", graph.find_one("User","t_user_id",user_men['id_str']))
					graph.create(db_user_men_tweet)
					create_new_user = 0
			if(create_new_user == 1):			
				db_user_men = Node ("User", t_user_id = user_men['id_str'], t_Name = user_men['name'], t_Screen_Name = user_men['screen_name'])
				db_user_men_tweet = Relationship(db_tweet, "USERS MENTIONED", db_user_men)
				graph.create(db_user_men_tweet)

