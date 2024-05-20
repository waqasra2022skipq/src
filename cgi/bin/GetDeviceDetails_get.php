<!DOCTYPE html>

<html>

<head>
  <title></title>
</head>

<body>


<?php

function CallUDDIWeb($InputURL)
{
echo "\r\n";
echo "\r\n" . 'InputURL: ' . $InputURL;
echo "\r\n";
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $InputURL);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $output = curl_exec($ch);
        $err = curl_error($ch);

        echo '' . $err;
        curl_close($ch);

        return $output;
}

function ParseUddIResponse($uddiresonse)
{
    $jsonData = json_decode($uddiresonse);

    echo 'After Parsing response from FIRST URL';
    echo "<br />";
    echo "<br />";

    echo "\r\n" . 'udi: ' . $jsonData->{'udi'};
    echo "<br />";

    echo "\r\n" . 'issuing_agency: ' . $jsonData->{'issuing_agency'};
    echo "<br />";

    echo "\r\n" . 'di: ' . $jsonData->{'di'};
    echo "<br />";

    echo "\r\n" . 'serial_number: ' . $jsonData->{'serial_number'};
    echo "<br />";

    echo "\r\n" . 'expiration_date_original_format: ' . $jsonData->{'expiration_date_original_format'};
    echo "<br />";

    echo "\r\n" . 'expiration_date_original: ' . $jsonData->{'expiration_date_original'};
    echo "<br />";

    echo "\r\n" . 'expiration_date: ' . $jsonData->{'expiration_date'};
    echo "<br />";

    echo "\r\n" . 'manufacturing_date_original_format: ' . $jsonData->{'manufacturing_date_original_format'};
    echo "<br />";

    echo "\r\n" . 'manufacturing_date_original: ' . $jsonData->{'manufacturing_date_original'};
    echo "<br />";

    echo "\r\n" . 'manufacturing_date: ' . $jsonData->{'manufacturing_date'};
    echo "<br />";

    echo "\r\n" . 'lot_number: ' . $jsonData->{'lot_number'};
    echo "<br />";

    echo '--------------------------------------';
}

function GetDeviceIdentifier($uddiresonse)
{
    $jsonData = json_decode($uddiresonse);
    return $jsonData->{'di'};
}

function GetDeviceParameters($uddiresonse)
{
    $jsonData = json_decode($uddiresonse);

    echo "<br />";
    echo "<br />";
    echo 'After Parsing response from SECOND URL';
    echo "<br />";
    echo "<br />";
    
    echo "\r\n" . 'devicePublishDate: ' . $jsonData->{'gudid'}->{'device'}->{'devicePublishDate'};
    echo "<br />";    
    echo "\r\n" . 'catalogNumber: ' . $jsonData->{'gudid'}->{'device'}->{'catalogNumber'};
    echo "<br />";    
    echo '--------------------------------------';    
}

$deviceid = '';
$deviceid = $_GET["deviceid"];
#$y=$_POST['snum'];
echo "\r\n";
echo "\r\n" . 'deviceid: ' . $deviceid;
echo "\r\n";
$url = "https://accessgudid.nlm.nih.gov/api/v1/parse_udi.json?udi=" . $deviceid;

$uddiresonse = CallUDDIWeb($url);
ParseUddIResponse($uddiresonse);
$deviceIdentifier = GetDeviceIdentifier($uddiresonse);

$url = 'https://accessgudid.nlm.nih.gov/api/v1/devices/lookup.json?di=' . $deviceIdentifier;
$uddiresonse = CallUDDIWeb($url);
echo "<br />";
GetDeviceParameters($uddiresonse);
?>

</body>

</html>
