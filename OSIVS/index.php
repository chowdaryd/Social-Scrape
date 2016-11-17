<html>
	<head>
		<?php session_start(); $_SESSION['lin']=0;?>
		<title>Social-Scrape:Login</title>
		<link type="text/css" rel="stylesheet" href="login.css">
		<link type="text/css" rel="stylesheet" href="theme.css">
		<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
		
	</head>
	<body>
		<div class="form-box">		
			<div class="form-head">
				<h3>Social Scrape</h3>
			</div>
			<div class="form-in">
				<form action="login.php" method="POST">
					<input type="text" name="uname" id="uname" placeholder="Username"/><br/>
					<input type="password" name="pass" id="pass" placeholder="Password"/><br/>
					<input type="submit" id="submit" value="Login"/>			
				</form>
			</div>
		</div>
	</body>
</html>
