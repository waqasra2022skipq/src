#!/usr/bin/perl -w
 
use SOAP::Lite;

print SOAP::Lite                                             
  -> uri('http://www.soaplite.com/Demo')                                             
  -> proxy('http://services.soaplite.com/hibye.cgi')
  -> hi()                                                    
  -> result;
