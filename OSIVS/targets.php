<html>
	<head>
		<?php session_start(); if($_SESSION['lin']!=1){header("Location: http://localhost/OSIVS/index.php");}elseif($_SESSION['setar']!="1"){header("Location: http://localhost/OSIVS/home.php");}?>
		<title>Social-Scrape:Targets</title>
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link typr="text/css" rel="stylesheet" href="targets.css">
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
			<h2>Targets</h2>
			<br/>
			<h4>Add Targets:</h4>
			<div id="target-form">
				<form method="POST" action="addtarget.php">
					<input type="text" name="name" id="fullname" placeholder="John Doe"/>
					<input type="text" name="facebook" id="fbid" placeholder="Facebook ID "/>
					<input type="text" name="twitter" id="tid" placeholder="Twitter ID "/>
					<input type="submit" id="add-btn" value="Add Target"/>					
				</form>		
			</div>
			<br/>
			<h4>List of Targets:</h4>
			<br/>
			<div id="target-list">

				<?php
					require('vendor/autoload.php'); 

					use GraphAware\Neo4j\Client\ClientBuilder;

					$client = ClientBuilder::create()
						->addConnection('default', 'http://neo4j:Cross@localhost:7474')
						->build();

					
					$query = "match (p:Person)-[r:ACCOUNT]->(u:User) return p.Name as Name,u.fb_user_id as fbid,u.t_user_id as tid";
					$result = $client->run($query);
					echo "<Table id='tbltar'><tr><th>Name</th><th>Facebook ID</th><th>Twitter ID</th><tr>";
					foreach ($result->records() as $record) {
						echo"<tr>";
						echo "<td>{$record->value("Name")}</td>";
						echo "<td>{$record->value("fbid")}</td>";
						echo "<td>{$record->value("tid")}</td>";
						echo"</tr>";
					}
					echo "</Table>";
				?>
			</div>
		</div>
	</body>
<html>
