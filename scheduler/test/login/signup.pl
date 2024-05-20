
my $ehr_user_type = 'user/admin'; # this will be single value. when you create a user, just pass user and when you create admin, just pass admin here.

my $ehr_email = 'ada@gmail.com';
my $ehr_username = 'ehr-username';
my $ehr_first_name => 'test first';
my $ehr_last_name => 'test last';
my $ehr_password => 'anypassword';
my $ehr_login_token => 'a random string'

# this is condition for user-type, On the basis of user-type, we will send different value.
if ($ehr_user_type == 'user') { # $ehr_panel and $ehr_action value when you create a user.
	my $ehr_panel => 'anon/register';
	my $ehr_action => 'register';
} else { ## $ehr_panel and $ehr_action value when you create a admin.
	my $ehr_panel => 'admin/company/staff/create';
	my $ehr_action => 'create';
}

# This is the URL of scheduler application where you send data to register a new user into schedular.
my $url = 'https://dev.okmms.com/scheduler/mms/index.php';
my $header = ['Content-Type' => 'application/json; charset=UTF-8'];

# This the data array which need to send to scheduler
my $data = [
	'nts-email' => $ehr_email,
	'nts-username' => $ehr_username,
	'nts-first_name' => $ehr_first_name,
	'nts-last_name' => $ehr_last_name,
	'nts-password' => $ehr_password,
	'nts-password2' => $ehr_password,
	'nts-panel' => $ehr_panel,
	'nts-action' => $ehr_action,
	'nts-source' => 'EHR',
	'nts-ehr_login_token' => $ehr_login_token, # this same token need to store into EHR database
];
# my $encoded_data = encode_utf8(encode_json($data));

# this is the POST request from perl to send data on URL...
my $r = HTTP::Request->new('POST', $url, $header, $data);



# When you create a user into ehr and scheduler you can call this login URL something like this.

# https://dev.okmms.com/scheduler/mms/index.php?nts-panel=anon%2Flogin&source=ehr&token=user-random-login-token


