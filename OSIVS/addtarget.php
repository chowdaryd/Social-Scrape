<?php
	require('vendor/autoload.php'); // or your custom autoloader

	use GraphAware\Neo4j\Client\ClientBuilder;

	$client = ClientBuilder::create()
		->addConnection('default', 'http://neo4j:Cross@localhost:7474')
		->build();
	
	$Name = $_POST["name"];
	$fbid = $_POST["facebook"];
	$tid = $_POST["twitter"];
	$fb_node = 0;
	$t_node = 0;

	$query = "MATCH (u:User) RETURN u.fb_user_id as fbid";		//search node with given fbid
	$result0 = $client->run($query);
	foreach ($result0->records() as $record) {
		if ($fbid == $record->value("fbid")){		
    			$fb_node = 1;

		}
	}
	$query = "MATCH (u:User) RETURN u.t_user_id as tid";		//search node with given tid
	$result = $client->run($query);
	foreach ($result->records() as $record) {		
		if ($tid == $record->value("tid")){
			$t_node = 1;

		}
	}

	$client->run("CREATE (p:Person) SET p += {infos}", ['infos' => ['Name' => $Name,'Id'=> uniqid()]]);

	if($fb_node== 1 && $t_node == 0){
		$client->run("CREATE (u:User) SET u += {infos}", ['infos' => ['t_user_id' => $tid]]);
	}
	elseif($fb_node== 0 && $t_node == 1){
		$client->run("CREATE (u:User) SET u += {infos}", ['infos' => ['fb_user_id' => $fbid]]);
	}
	elseif($fb_node== 0 && $t_node == 0){
		$client->run("CREATE (u:User) SET u += {infos}", ['infos' => ['t_user_id' => $tid]]);
		$client->run("CREATE (u:User) SET u += {infos}", ['infos' => ['fb_user_id' => $fbid]]);
	}
	
	$client->run("MATCH (p:Person),(u:User) WHERE p.Name = '{$Name}' AND u.t_user_id = '{$tid}' CREATE (p)-[r:ACCOUNT {Type: 'Twitter'}]->(u)");
	$client->run("MATCH (p:Person),(u:User) WHERE p.Name = '{$Name}' AND u.fb_user_id = '{$fbid}' CREATE (p)-[r:ACCOUNT {Type: 'Facebook'}]->(u)");

	header("Location: http://localhost/OSIVS/targets.php");
?>
