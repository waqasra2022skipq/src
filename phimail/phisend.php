<?php
/*
 * Example illustrating use of the PhiMailConnector class.
 *
 * (c) 2014-2016 EMR Direct. All Rights Reserved.
 * Use of this code is subject to the terms of the phiMail Developer
 * License Agreement ("DLA"). This code may not be used, redistributed or 
 * modified without the express written consent of EMR Direct, except as 
 * permitted by the DLA.
 */
include ('/home/okmis/mis/src/phimail/PhiMailConnector.php');

/**
 *
 * @author EMR Direct
 */
class PhiMailExample {
            
    public static function loadFile($filename) {
        return file_get_contents($filename);
    }

    public static function writeDataFile($filename, $data) {
        return file_put_contents($filename, $data);
    }
    
    /**
     * @param args the command line arguments
     */
    public static function main($argv) {
        echo("<pre>\n");
        try {
            $phiMailServer = "sandbox.phimail-dev.com";
            $phiMailPort = 32541; // this is the default port #
            
            //$phiMailUser = "okmis@test.directproject.net";//mahesh-edge2015@directtest.interopengine.com
            $phiMailUser = "okmis-edge2015@directtest.interopengine.com";    // b1
            $phiMailPass = "enn1sm6t";
            
            $outboundFile = $argv[1];
	    echo('outboundFile = ' . $outboundFile . "\n");
            //$outboundRecipient = "wellformed1@ttpedge.sitenv.org";
            $outboundRecipient = $argv[2];
	    echo('argv2 = ' . $argv[2] . "\n");
	    echo('outboundRecipient = ' . $outboundRecipient . "\n");

            PhiMailConnector::setServerCertificate("/home/okmis/mis/src/phimail/EMRDirectTestCA.pem");
            
            $c = new PhiMailConnector($phiMailServer, $phiMailPort);
            echo("inititated connector\n");
			$c->authenticateUser($phiMailUser, $phiMailPass);
            
            // Sample code to send a Direct message.
                echo("Sending a CDA as an attachment\n");

                // After authentication, the server has a blank outgoing message
                // template. Begin building this message by adding a recipient.
                // Multiple recipients can be added by calling this command more
                // than once. A separate message will be sent for each recipient.
                $recip = $c->addRecipient($outboundRecipient);

                // The server returns information about the recipient if the
                // address entered is accepted, otherwise an exception is thrown.
                // How you use this recipient information is up to you...
                echo('Recipient Info = ' . $recip . "\n");

                // Optionally, set the Subject of the outgoing message.
                // This will override the default message Subject set by the server.
                $c->setSubject('Test Subject sent by PHP connector');

                // Add the main body of the message.
                $c->addText("This is the main message content. A CDA is attached.");

                // Add a CDA attachment and let phiMail server assign a filename.
	        echo('Argument Info = ' . $outboundFile . "\n");
                $c->addCDA(self::loadFile($outboundFile));

                // Optionally, add a binary attachment and specify the 
                // attachment filename yourself.
                //$c->addRaw(self::loadFile("/tmp/Test_pdf.pdf"), "test.pdf");

                // Optionally, request a final delivery notification message.
                // Note that not all HISPs can provide this notification when requested.
                // If the receiving HISP does not support this feature, the message will
                // result in a failure notification after the timeout period has elapsed.
                // This command will override the default setting set by the server.
                //
                $c->setDeliveryNotification(true);

                // Send the message. srList will contain one entry for each recipient.
                // If more than one recipient was specified, then each would have an entry.
                $srList = $c->send();
                foreach ($srList as $sr) {
                    echo("Send to " . $sr->recipient);
                    echo($sr->succeeded ? " succeeded id=" : "failed err=");
                    echo($sr->succeeded ? $sr->messageId : $sr->errorText);
                    echo("\n");
                }
            
        } catch (Exception $e) {
            echo($e->getMessage() . "\n");
        }
        
        try {
            $c->close();
        } catch (Exception $ignore) { }
        
        echo("</pre>\n");

    }
}

// Run the example code
PhiMailExample::main($argv);

?>
