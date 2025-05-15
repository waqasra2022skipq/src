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
include ('C:/xampp/htdocs/src/phimail/PhiMailConnector.php');

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
        // echo("<pre>\n");
        $aReplace = array('<','>');
        try {
            $phiMailServer = "sandbox.phimail-dev.com";
            $phiMailPort = 32541; // this is the default port #
            
            //$phiMailUser = "okmis-edge2015@directtest.interopengine.com";    // b1
            //$phiMailUser = "okmis@test.directproject.net";                   // h1
            $phiMailUser = $argv[1];
            echo("== phiMailUser = ".$phiMailUser."\n");
            $phiMailPass = "enn1sm6t";
            
//            echo("== argv = ".$argv[0]."\n".$argv[1]."\n".$argv[2]."\n");
            $tag = $argv[2];
            echo("== tag = ".$tag."\n");
            $attachmentSaveDirectory = "C:/xampp/htdocs/src/phimail/received/";
            echo("== attachmentSaveDirectory = ".$attachmentSaveDirectory."\n");

            PhiMailConnector::setServerCertificate("C:/xampp/htdocs/src/phimail/EMRDirectTestCA.pem");
            
            echo("== inititated connector\n");
            $c = new PhiMailConnector($phiMailServer, $phiMailPort);
	    $c->authenticateUser($phiMailUser, $phiMailPass);
            
            // Sample code to check for any incoming messages. Generally, this
            // code would run in a separate background process to poll the
            // phiMail server at regular intervals for new messages. In production
            // $phiMailUser above would be set to an address group to efficiently
            // retrieve messages for all addresses in the address group, rather
            // than iterating through individual addresses.  Please see the
            // API documentation for further information about address groups.
                while (true) {
                    echo("============\n");
                    echo("== Checking mailbox\n");

                    // check next message or status update
                    $cr = $c->check();
                    if ($cr == null) {
                        
                        echo("== Check returned null; no messages on queue.\n");
                        break;
                        
                    } else if($cr->isMail()) {
                        // If you are checking messages for an address group,
                        // $cr->recipient will contain the address in that
                        // group to which this message should be delivered.
                        echo("== A new message is available for " . $cr->recipient . "\n");
                        echo("== from " . $cr->sender . "; id " 
                                . $cr->messageId . "; #att=" . $cr->numAttachments
                                . "\n");
                        
                        $msgid = str_replace($aReplace,'',$cr->messageId);
                        $msginfo = "recipient: ".$cr->recipient."\nsender: ".$cr->sender."\n";
                        $msgfiles = '';
                        echo("== msgid: " . $msgid . "\n");
                        echo("== info: " . $msginfo . "\n");
                        for ($i = 0; $i <= $cr->numAttachments; $i++) {
                            // Get content for part i of the current message.
                            $showRes = $c->show($i);
                            echo("attachment # " . $i . "\n");
                            echo("MimeType = " . $showRes->mimeType . "; length=" . $showRes->length . "\n");

                            // List all the headers. Headers are set by the
                            // sender and may include Subject, Date, additional
                            // addresses to which the message was sent, etc.
                            // Do NOT use the To: header to determine the address
                            // to which this message should be delivered
                            // internally; use $cr->recipient instead.
                            foreach ($showRes->headers as $header) {
                                echo("Header: " . $header . "\n");
                                $msginfo .= $header."\n";
                            }

                            // Process the content; for this example text data 
                            // is echoed to the console and non-text data is
                            // written to files.
                            if (!strncmp($showRes->mimeType, 'text/', 5)) {
                                // ... do something with text parts ...
                                // For this example we assume ascii or utf8 
                                echo("Content: <TEXT>  Writing attachment file " . $showRes->filename . "\n");
                                //$s = $showRes->data;
                                //echo("Content:\n" . $s . "\n");
                                if ($showRes->filename != null)
                                {
                                  self::writeDataFile($attachmentSaveDirectory.$tag.'_'.$showRes->filename, $showRes->data);
                                }
                            } else {
                                // ... do something with binary data ...
                                echo("Content: <BINARY>  Writing attachment file " . $showRes->filename . "\n");
                                self::writeDataFile($attachmentSaveDirectory.$tag.'_'.$showRes->filename, $showRes->data);
                            }
                            if ($showRes->filename != null) { $msgfiles .= $tag.'_'.$showRes->filename."\n"; }

                            // Display the list of attachments and associated info. This info is only
                            // included with message part 0.
                            for ($k = 0; $i == 0 && $k < $cr->numAttachments; $k++) {
                                echo("Attachment: " . ($k + 1) 
                                        . ": " . $showRes->attachmentInfo[$k]->mimeType 
                                        . " fn:" . $showRes->attachmentInfo[$k]->filename 
                                        . " Desc:" . $showRes->attachmentInfo[$k]->description
                                        . "\n");
                            }

                        }
                        $msginfo .= "Files:\n".$msgfiles;
                        echo("== info: " . $msginfo . "\n");
                        self::writeDataFile($attachmentSaveDirectory.'newmsg_'.$tag.'_'.$msgid, $msginfo);

                        // This signals the server that the message can be safely removed from the queue
                        // and should only be sent after all required parts of the message have been
                        // retrieved and processed.
                        $c->acknowledgeMessage();
                        
                    } else {
                        
                        // Process a status update for a previously sent message.
                        echo("== Status message for ID = " . $cr->messageId . "\n");
                        echo("==   StatusCode = " . $cr->statusCode . "\n");
                        if ($cr->info != null) echo("==   Info = " . $cr->info . "\n");
                        if ($cr->statusCode == "failed") {
                            // ...do something about a failed message...
                            // $cr->messageId will match the messageId returned
                            // when you originally sent the corresponding message
                            // See the API documentation for information about
                            // status notification types and their meanings.
                        }
                        
                        // This signals the server that the status update can be 
                        // safely removed from the queue,
                        // i.e. it has been successfully received and processed.
                        // Note: this is NOT the same method used to acknowledge
                        // regular messages.
                        $c->acknowledgeStatus();
                    }
                }
            
        } catch (Exception $e) {
            echo($e->getMessage() . "\n");
        }
        
        try {
            $c->close();
        } catch (Exception $ignore) { }
        
        // echo("</pre>\n");

    }
}

// Run the example code
PhiMailExample::main($argv);

?>
