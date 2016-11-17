<html>
	<head>
		<?php session_start(); if($_SESSION['lin']!=1){header("Location: http://localhost/OSIVS/index.php");}?>
		<title>Social-Scrape:Home</title>
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link typr="text/css" rel="stylesheet" href="profile.css">
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
			<?php
				require('vendor/autoload.php'); 
				use GraphAware\Neo4j\Client\ClientBuilder;

				$client = ClientBuilder::create()
					->addConnection('default', 'http://neo4j:Cross@localhost:7474')
					->build();

				if(isset($_GET['tid'])){
					$tid = $_GET['tid'];
					$result = $client->run("Match (p:Person)-[r:ACCOUNT{Type:'Twitter'}]->(u:User) where u.t_user_id='{$tid}' Return p.Name as name,p.Id as SSID,p.yearavgpost as yap,p.yearavgcom as yac,p.yearavgtweet as yat,p.yeargraphlink as ygl,p.monthavgpost as map,p.monthavgcom as mac,p.monthavgtweet as mat,p.monthgraphlink as mgl,p.dayavgpost as dap,p.dayavgcom as dac,p.dayavgtweet as dat,p.daygraphlink as dgl,p.hrs12avgpost as h12ap,p.hrs12avgcom as h12ac,p.hrs12avgtweet as h12at,p.hrs12graphlink as h12gl,p.hrs6avgpost as h6ap,p.hrs6avgcom as h6ac,p.hrs6avgtweet as h6at,p.hrs6graphlink as h6gl,p.hrsavgpost as hap,p.hrsavgcom as hac,p.hrsavgtweet as hat,p.hrsgraphlink as hgl,p.min30avgpost as m30ap,p.min30avgcom as m30ac,p.min30avgtweet as m30at,p.min30graphlink as m30gl,p.min15avgpost as m15ap,p.min15avgcom as m15ac,p.min15avgtweet as m15at,p.min15graphlink as m15gl,p.minavgpost as miap,p.minavgcom as miac,p.minavgtweet as miat,p.mingraphlink as migl");
				}
				elseif(isset($_GET['fbid'])){
					$fbid = $_GET['fbid'];
					$result = $client->run("Match (p:Person)-[r:ACCOUNT{Type:'Facebook'}]->(u:User) Where u.fb_user_id='{$fbid}' Return p.Name as name,p.Id as SSID,p.yearavgpost as yap,p.yearavgcom as yac,p.yearavgtweet as yat,p.yeargraphlink as ygl,p.monthavgpost as map,p.monthavgcom as mac,p.monthavgtweet as mat,p.monthgraphlink as mgl,p.dayavgpost as dap,p.dayavgcom as dac,p.dayavgtweet as dat,p.daygraphlink as dgl,p.hrs12avgpost as h12ap,p.hrs12avgcom as h12ac,p.hrs12avgtweet as h12at,p.hrs12graphlink as h12gl,p.hrs6avgpost as h6ap,p.hrs6avgcom as h6ac,p.hrs6avgtweet as h6at,p.hrs6graphlink as h6gl,p.hrsavgpost as hap,p.hrsavgcom as hac,p.hrsavgtweet as hat,p.hrsgraphlink as hgl,p.min30avgpost as m30ap,p.min30avgcom as m30ac,p.min30avgtweet as m30at,p.min30graphlink as m30gl,p.min15avgpost as m15ap,p.min15avgcom as m15ac,p.min15avgtweet as m15at,p.min15graphlink as m15gl,p.minavgpost as miap,p.minavgcom as miac,p.minavgtweet as miat,p.mingraphlink as migl");
					
				}
				elseif(isset($_GET['pid'])){
					$pid = $_GET['pid'];
					$result = $client->run("Match (p:Person) Where p.Id='{$pid}' Return p.Name as name,p.Id as SSID,p.yearavgpost as yap,p.yearavgcom as yac,p.yearavgtweet as yat,p.yeargraphlink as ygl,p.monthavgpost as map,p.monthavgcom as mac,p.monthavgtweet as mat,p.monthgraphlink as mgl,p.dayavgpost as dap,p.dayavgcom as dac,p.dayavgtweet as dat,p.daygraphlink as dgl,p.hrs12avgpost as h12ap,p.hrs12avgcom as h12ac,p.hrs12avgtweet as h12at,p.hrs12graphlink as h12gl,p.hrs6avgpost as h6ap,p.hrs6avgcom as h6ac,p.hrs6avgtweet as h6at,p.hrs6graphlink as h6gl,p.hrsavgpost as hap,p.hrsavgcom as hac,p.hrsavgtweet as hat,p.hrsgraphlink as hgl,p.min30avgpost as m30ap,p.min30avgcom as m30ac,p.min30avgtweet as m30at,p.min30graphlink as m30gl,p.min15avgpost as m15ap,p.min15avgcom as m15ac,p.min15avgtweet as m15at,p.min15graphlink as m15gl,p.minavgpost as miap,p.minavgcom as miac,p.minavgtweet as miat,p.mingraphlink as migl");
					
				}


				foreach($result->records() as $r){
					
					$result1 = $client->run("Match (p:Person)-[r1:ACCOUNT]->(u:User)-[r2:TWEETED]->(t:Tweet) where p.Id='{$r->value('SSID')}' Return count(r2) as totalt");
					foreach($result1->records() as $res){
						$tot = $res->value('totalt');
					}
					$result1 = $client->run("Match (p:Person)-[r1:ACCOUNT]->(u:User)-[r2:POSTED]->(p1:Post) where p.Id='{$r->value('SSID')}' Return count(r2) as totalp");
					foreach($result1->records() as $res){
						$top = $res->value('totalp');
					}
					$result1 = $client->run("Match (p:Person)-[r1:ACCOUNT]->(u:User)-[r2:COMMENTED]->(c:Comment) where p.Id='{$r->value('SSID')}' Return count(r2) as totalc");
					foreach($result1->records() as $res){
						$toc = $res->value('totalc');
					}

					echo "<h2>Target Profile</h2>";
					echo "<table id='tblpro'><tr><th>Name : </th><td>{$r->value('name')}</td>";
					echo "<th>SSID : </th><td>{$r->value('SSID')}</td></tr>";
					echo "<tr><th>Total No of Tweets</th><td colspan='1'>$tot</td></tr>";
					echo "<tr><th>Total No of Posts</th><td colspan='1'>$top</td></tr>";
					echo "<tr><th>Total No of Comments</th><td colspan='1'>$toc</td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Per Year</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('yap')}</td>";
					echo "<td>{$r->value('yac')}</td>";
					echo "<td>{$r->value('yat')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('ygl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Per Month</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('map')}</td>";
					echo "<td>{$r->value('mac')}</td>";
					echo "<td>{$r->value('mat')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('mgl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Per Day</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('dap')}</td>";
					echo "<td>{$r->value('dac')}</td>";
					echo "<td>{$r->value('dat')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('dgl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every 12 Hours</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('h12ap')}</td>";
					echo "<td>{$r->value('h12ac')}</td>";
					echo "<td>{$r->value('h12at')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('h12gl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every 6 Hours</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('h6ap')}</td>";
					echo "<td>{$r->value('h6ac')}</td>";
					echo "<td>{$r->value('h6at')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('h6gl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every Hour</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('hap')}</td>";
					echo "<td>{$r->value('hac')}</td>";
					echo "<td>{$r->value('hat')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('hgl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every 30 Minutes</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('m30ap')}</td>";
					echo "<td>{$r->value('m30ac')}</td>";
					echo "<td>{$r->value('m30at')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('m30gl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every 15 Minutes</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('m15ap')}</td>";
					echo "<td>{$r->value('m15ac')}</td>";
					echo "<td>{$r->value('m15at')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('m15gl')}'>Click here for graph</a></td></tr>";
					echo "</table>";

					echo "<br/><h4>Avg Stats Every Minute</h4><br/>";
					echo "<table id='tblpro'>";
					echo "<tr><th>Posts</th><th>Comments</th><th>Tweets</th><tr>";
					echo "<tr><td>{$r->value('miap')}</td>";
					echo "<td>{$r->value('miac')}</td>";
					echo "<td>{$r->value('miat')}</td></tr>";
					echo "<tr><th>Graph of per year data : </th><td colspan='3'><a href='{$r->value('mgl')}'>Click here for graph</a></td></tr>";
					echo "</table>";
				}

			?>
		</div>

	</body>
<html>
