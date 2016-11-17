<html>
	<head>
		<?php session_start(); if($_SESSION['lin']!=1){header("Location: http://localhost/OSIVS/index.php");}elseif($_SESSION['seeres']!="1"){header("Location: http://localhost/OSIVS/home.php");}?>
		<title>Social-Scrape:Data</title>
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link typr="text/css" rel="stylesheet" href="data.css">
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
			<h3>Search the database</h3>
			<div class="query-form">
				<form method="POST" action="">
					<input type="text" name="query" id="qry" placeholder="Project X,John Doe,Jane Doe"/>
					<input type="submit" name="submit" id="submit" value="Submit Query"/>
				</form>
			</div>
			<br/>
			
			<div class="query-result">
				<?php 
					require('vendor/autoload.php'); 
					use GraphAware\Neo4j\Client\ClientBuilder;

					$client = ClientBuilder::create()
						->addConnection('default', 'http://neo4j:Cross@localhost:7474')
						->build();

				     if(isset($_POST['submit'])){
					echo "<h4>Result:</h4>";
					$tweetm = Array();
					$postm = Array();
					$cmntm = Array();
					$perm =Array();
					$search = $_POST['query'];
					$keywords = explode(",",$search);
					echo "<br/><p><b>You searched for : </b>";echo $search; echo "</p>";
					foreach($keywords as $key){
						$result = $client->run("Match (t:Tweet) Return t.Tweet_Text as Tweet,t.Tweet_Id as id");
						foreach ($result->records() as $record){
							if(preg_match("/{$key}/i", $record->value("Tweet"), $match)){
								if(!in_array($record->value("id"),$tweetm)){
									array_push($tweetm, $record->value("id"));
								}
							}
						}
						
						$result = $client->run("Match (p:Post) Return p.Message as msg,p.Post_Id as id");
						foreach ($result->records() as $record){

							if(preg_match("/{$key}/i", $record->value("msg"), $match)){
								if(!in_array($record->value("id"),$postm)){
									array_push($postm, $record->value("id"));
								}						
								
							}
						}
						
						$result = $client->run("Match (c:Comment) Return c.Comment_Message as msg,c.Comment_Id as id");
						foreach ($result->records() as $record){
							
							if(preg_match("/{$key}/i", $record->value("msg"), $match)){
								if(!in_array($record->value("id"),$cmntm)){
									array_push($cmntm, $record->value("id"));
								}
							}
						}
						
						$result = $client->run("Match (p:Person)-->(u:User) return p.Name as name,u.fb_Name as fbname,u.t_Name as tname,u.t_Screen_Name as scname,p.Id as id");
						foreach ($result->records() as $record){
							
							if(preg_match("/{$key}/i", $record->value("name"), $match)){
								if(!in_array($record->value("id"),$perm)){
									array_push($perm, $record->value("id"));
								}
							}
							if(preg_match("/{$key}/i", $record->value("fbname"), $match)){
								if(!in_array($record->value("id"),$perm)){
									array_push($perm, $record->value("id"));
								}
							}
							if(preg_match("/{$key}/i", $record->value("tname"), $match)){
								if(!in_array($record->value("id"),$perm)){
									array_push($perm, $record->value("id"));
								}
							}
							if(preg_match("/{$key}/i", $record->value("scname"), $match)){
								if(!in_array($record->value("id"),$perm)){
									array_push($perm, $record->value("id"));
								}
							}
						}
					}

					echo "<br/><h3>Targets</h3><br/>";

					echo "<Table id='tblser'><tr><th>Target Name</th><tr>";
					foreach ($perm as $p){
						$res = $client->run("Match (p:Person) where p.Id = '{$p}' Return p.Name as name");
						foreach($res->records() as $r){
							echo "<tr>";
							echo "<td><a href='profile.php?pid={$p}'>{$r->value("name")}</a></td>";
							echo "</tr>";
						}
					}
					echo "</Table>";


					echo "<br/><h3>Facebook Posts</h3><br/>";

					echo "<Table id='tblser'><tr><th>User</th><th>Message</th><tr>";
					foreach ($postm as $p){
						$res = $client->run("Match (u:User)-[r:POSTED]->(p:Post) where p.Post_Id = '{$p}' Return p.Message as msg,u.fb_Name as name,u.fb_user_id as id");
						foreach($res->records() as $r){
							echo "<tr>";
							echo "<td><a href='profile.php?fbid={$r->value("id")}'>{$r->value("name")}</a></td>";
							echo "<td>{$r->value("msg")}</td>";
							echo "</tr>";
						}
					}
					echo "</Table>";

					echo "<br/><h3>Facebook Comments</h3><br/>";

					echo "<Table id='tblser'><tr><th>User</th><th>Message</th><tr>";
					foreach ($cmntm as $c){
						$res = $client->run("Match (u:User)-[r:COMMENTED]->(c:Comment) where c.Comment_Id = '{$c}' Return c.Comment_Message as msg,u.fb_Name as name,u.fb_user_id as id");
						foreach($res->records() as $r){
							echo "<tr>";
							echo "<td><a href='profile.php?fbid={$r->value("id")}'>{$r->value("name")}</a></td>";
							echo "<td>{$r->value("msg")}</td>";
							echo "</tr>";
						}
					}
					echo "</Table>";
					
					echo "<br/><h3>Twitter Tweets</h3><br/>";

					echo "<Table id='tblser'><tr><th>User</th><th>Message</th><tr>";
					foreach ($tweetm as $t){
						$res = $client->run("Match (u:User)-[r:TWEETED]->(t:Tweet) where t.Tweet_Id = '{$t}' Return t.Tweet_Text as msg,u.t_Name as name,u.t_user_id as id");
						foreach($res->records() as $r){
							echo "<tr>";
							echo "<td><a href='profile.php?tid={$r->value("id")}'>{$r->value("name")}</a></td>";
							echo "<td>{$r->value("msg")}</td>";
							echo "</tr>";
						}
					}
					echo "</Table>";
				}?>
			</div>
		</div>
	</body>
<html>
