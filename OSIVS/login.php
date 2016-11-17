<?php

session_start();

require('vendor/autoload.php'); 

use GraphAware\Neo4j\Client\ClientBuilder;

$client = ClientBuilder::create()
	->addConnection('default', 'http://neo4j:Cross@localhost:7474')
	->build();

$user = $_POST["uname"];

$pass = $_POST["pass"];

$result = $client->run("match (l:Login)-[c:CRED]->(a:Account) return a.uname as user_name");
foreach ($result->records() as $record) {
	if ($user == $record->value("user_name")) {
		$result1 = $client->run("match (l:Login)-[c:CRED]->(a:Account) where a.uname = '{$user}' return a.pass as password");
		foreach ($result1->records() as $record1) {
			if (md5($pass) == $record1->value("password")) {
				$_SESSION["lin"] = 1;
				
				$res = $client->run("match (l:Login)-[c:CRED]->(a:Account) return a.settargets as setar,a.seeresults as seeres,a.dbaccess as dba");
				foreach ($res->records() as $rec) {
					$_SESSION["setar"] = $rec->value('setar');
					$_SESSION["seeres"] = $rec->value('seeres');
					$_SESSION["dba"] = $rec->value('dba');
					
				}
				header("Location: http://localhost/OSIVS/home.php");
				exit();
			}
		}
	}
}

header("Location: http://localhost/OSIVS/index.php");
exit();
?>


