<html>
	<head>
		<?php session_start(); if($_SESSION['lin']!=1){header("Location: http://localhost/OSIVS/index.php");}elseif($_SESSION['dba']!="1"){header("Location: http://localhost/OSIVS/home.php");}?>
		<title>Social-Scrape:Graph</title>
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link typr="text/css" rel="stylesheet" href="graph.css">
		<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
	</head>
	<body>
		<div class="home-bar">
			<h4 id="logo">Social-Scrape</h4>
			<ul id="menu">
				<li><a href="home.php">Home</a></li>
				<li><a href="data.php">Data</a></li>
				<li><a href="targets.php">Targets</a></li>
				<li><a href="graph.php">Graph Database</a></li>
				<li id="lgout"><a href="logout.php">Logout</a></li>
			</ul>
		</div>
		<div class="content">
			<h3>Query the database</h3>
			<div class="query-form">
				<form method="POST" action="#">
					<input type="text" name="query" id="qry"/>
					<input type="submit" name="submit" id="submit" value="Submit Query"/>
				</form>
			</div>
			<br/>
			<h4>Result:</h4>
			<div class="query-result">
				<p>-----resut of the query is printed here-----</p>		
			</div>
		</div>
	</body>
<html>
