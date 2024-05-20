use IO;
my $output = new IO::File(">output.xml");

use XML::Writer;
my $writer = new XML::Writer( OUTPUT => $output );

$writer->xmlDecl( 'UTF-8' );
$writer->doctype( 'html' );
$writer->comment( 'My happy little HTML page' );
$writer->pi( 'foo', 'bar' );
$writer->startTag( 'html' );
$writer->startTag( 'body' );
$writer->startTag( 'h1' );
$writer->startTag( 'font', 'color' => 'green' );
$writer->characters( "<Hello World!>" );
$writer->endTag();
$writer->endTag();
$writer->dataElement( "p", "Nice to see you." );
$writer->endTag();
$writer->endTag();
$writer->end();
