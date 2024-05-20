#!/usr/bin/perl -w    

use strict; 

   sub main{    
   $~ = 'MYLINE_TOP'; write;
      my ($w1,$w2,$w3,$w4) = ('work1','work2','work3','work4');
   $~ = 'MYWORK'; write;
print qq|<SPAN CLASS="head1" >\n|;
      my ($l1,$l2,$l3,$l4,$l5,$l6,$l7,$l8) = ('header1','header2','header3','header4','header5','header6','header7','header8');
#foreach my $e ( @$row ) { print qq|e=$e\n|; }
   $~ = 'MYLINE'; write;
print qq|</SPAN>\n|;
      my @arr = (['something1','something2','something3','something4','something5','something6','something7','something8']
                ,['more1'     ,'more2'     ,'more3'     ,'more4'     ,'more5'     ,'more6'     ,'more7'     ,'more8'     ]
                ,['another1'  ,'another2'  ,'another3'  ,'another4'  ,'another5'  ,'another6'  ,'another7'  ,'another8'  ]
                );

      for my $row (@arr) {
      ($l1,$l2,$l3,$l4,$l5,$l6,$l7,$l8) = @$row;
   $~ = 'MYLINE'; write;
      }
         format MYLINE =
@<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  @<<<<<<<<<<<<  
         $l1, $l2, $l3, $l4, $l5, $l6, $l7, $l8
.
format MYLINE_TOP = 
Testing of font change right/left just           Page: @>>>>>>>>>>
                                                       $%
------------------------------------------------------------------
.
         format MYWORK =
@>>>>>>>>>>>>  @>>>>>>>>>>>>  @>>>>>>>>>>>>  @>>>>>>>>>>>>
         $w1, $w2, $w3, $w4
.

   }    

print qq|Content-type: text/html

<HTML>
<STYLE TYPE="text/css">
     .breakhere {page-break-before: always}
     .small1 {font-size: 31px}
     .head1 {font-weight: bold}
</STYLE>
<BODY BGCOLOR=WHITE TEXT=BLACK>
<DIV style="width:500px;height:500px;border:1px solid #000;">This is a rectangle!
<pre>
<span class="small1" >
Blah blah
Multiple lines and no br's!
Oh yeah!
</span>
</pre>
<P CLASS="breakhere">OK...NOW FOR PAGE 2
<PRE>
|;
   main();  
print qq|
</PRE>
</DIV>
</BODY>
</HTML>
|;
