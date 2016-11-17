<html>
	<head>
		<?php session_start(); if($_SESSION['lin']!=1){header("Location: http://localhost/OSIVS/index.php");}?>
		<title>Social-Scrape:Home</title>
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link typr="text/css" rel="stylesheet" href="home.css">
		<link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
	</head>
	<body>
		<div class="home-bar">
			<h4 id="logo">Social Scrape</h4>
			<ul id="menu">
				<li><a href="home.php">Home</a></li>
				<li><a href="data.php">Data</a></li>
				<li><a href="targets.php">Targets</a></li>
				<li><a href="graph.php">Graph Database</a></li>
				<li id="lgout"><a href="logout.php">Logout</a></li>
			</ul>
		</div>
		<div class="content">
			<h5>*Disclaimer* : This tool was only developed for educational purposes.</h5>
			<pre>
______________________________________________________________________________________________________________
			 _____            _       _   _____                           
			/  ___|          (_)     | | /  ___|                          
			\ `--.  ___   ___ _  __ _| | \ `--.  ___ _ __ __ _ _ __   ___ 
			 `--. \/ _ \ / __| |/ _` | |  `--. \/ __| '__/ _` | '_ \ / _ \
			/\__/ / (_) | (__| | (_| | | /\__/ / (__| | | (_| | |_) |  __/
			\____/ \___/ \___|_|\__,_|_| \____/ \___|_|  \__,_| .__/ \___|
						                          | |         
						                          |_|         
_______________________________________________________________________________________________________________
			</pre>			
			<p>Social Scrape is a tool which uses API to interact with multiple social platforms to identify and grab information on select targets, it then verifies if the targets were suseptible to social engineering.</p>
			<br/><h3>How to use the tool:</h3>
			<h4>List of the required depandancies for this tool are:</h4>
			<ul id="dep">
				<li><a href ="https://www.python.org/download/releases/2.0/">python 2.0.7</a></li>
				<li><a href="https://httpd.apache.org/download.cgi">apache 2 web server</a></li>
				<li><a href="http://neo4j.com/download/">neo4j graph database<a/></li>
				<li><a href="https://github.com/tweepy/tweepy">Tweepy library for python<a/></li>
				<li><a href="https://docs.python.org/2/library/urllib2.html">urllib2 library for python<a/></li>
				<li><a href="https://docs.python.org/2/library/json.html">json library for python<a/></li>
				<li><a href="https://pypi.python.org/pypi/py2neo">py2neo library for python<a/></li>
				<li><a href="https://github.com/jadell/neo4jphp">neo4jphp library for python<a/></li>
			</ul>
			
			<h4>Steps to run this tool are:</h4>
			<ol>
				<li>Start the apache2 server</li>
				<li>Start the neo4j database</li>
				<li>Open the user interface from the web browser</li>
				<li>Enter login credentials and login into the tool</li>
				<li>Go to the targets tab and add targets</li>
				<li>Execute the python script to grab Twitter data</li>
				<li>Execute the python script to grab Facebook data</li>
				<li>Execute the python script to perform behavior analytics on collected data</li>
				<li>Go to data tab on user interface to see the results.</li>
			</ol>

		</div>

	</body>
<html>
