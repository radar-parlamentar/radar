<?php

//Retrieve form data
//GET - user submitted data using AJAX
//POST - in case user does not support javascript, we'll use POST instead

@$name = ($_GET['name']) ? $_GET['name'] : $_POST['name'];
@$email = ($_GET['email']) ? $_GET['email'] : $_POST['email'];
@$homepage = ($_GET['url']) ? $_GET['url'] : $_POST['url'];
@$subject = ($_GET['subject']) ? $_GET['subject'] : $_POST['subject'];
@$message = ($_GET['message']) ? $_GET['message'] : $_POST['message'];

$error_msgs = array(
					"name" => "Enter your full name.",
					"email" => "Enter a valid email address. e.g. john@example.com",
					"subject" => "Subject is required.",
					"message" => "Message is required."
					);

//Flag to indicate which method it uses. If POST set it to 1
if($_POST){$post = 1;}

$error_msg = "<h4>Please fill up the required fields.</h4>";

$errors = array();

if(!preg_match("/^[a-z0-9]+([_\\.-][a-z0-9]+)*" ."@"."([a-z0-9]+([\.-][a-z0-9]+)*)+"."\\.[a-z]{2,}"."$/", $email)){
	$errors[count($errors)] = 'email';
}

//Simple server side validation for POST data, of course,
//you should validate the email

if(empty($name)){
	$errors[count($errors)] = 'name';
}
if(empty($subject)){
	$errors[count($errors)] = 'subject';
}
if(empty($message)){
	$errors[count($errors)] = 'message';
}

//if the errors array is empty, send the mail
if(!$errors){
	//recipient - change this to your name and email
	$to = 'Nuruzzaman Sheikh <palpaldal@yahoo.com>';
	//sender
	$from = $name.' <'.$email.'>';
	//html message
	$cMsg = '
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head></head>
	<body>
	<table border=1>
		<tr><td>Name</td><td>' . $name . '</td></tr>
		<tr><td>Email</td><td>' . $email . '</td></tr>
		<tr><td>Homepage</td><td>' . $homepage . '</td></tr>
		<tr><td>Subject</td><td>' . $subject . '</td></tr>
		<tr><td>Message</td><td>' . nl2br($message) . '</td></tr>
	</table>
	</body>
	</html>';

	//send the mail
	$result = @sendmail($to, $subject, $cMsg, $from);

	//if POST was used, display the message straight away
	if($_POST){
		if($result) echo 'Thank you! We have received your message.';
		else echo 'Sorry, unexpected error. Please try again later.';
		echo '<br/><a href="index.html" title="">Back to Home Page</a>';
	}
	//else if GET was used, return the boolean value so that
	//ajax script can react accordingly
	//1 means success, 0 means failed
	else{
		echo $result;
	}
	//if the errors array has values
}
else{
	//display the error message(s)
	for($i = 0; $i < count($errors); $i++){
		$error_msg .= $error_msgs[$errors[$i]]. "<br />";
	}

	$error_msg .= '<a href="contact.html" title="">Retry Again</a>';
	echo $error_msg;
	exit;
}

//Simple mail function with HTML header
function sendmail($to, $subject, $cMsg, $from){
	$headers = "MIME-Version: 1.0" . "\r\n";
	$headers .= "Content-type:text/html; charset=iso-8859-1" . "\r\n";
	$headers .= "From: ".$from."\r\n";

	$result = mail($to, $subject, $cMsg, $headers);
	if($result) return 1;
	else return 0;
}

?>