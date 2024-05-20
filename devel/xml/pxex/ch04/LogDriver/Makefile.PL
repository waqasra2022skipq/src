use ExtUtils::MakeMaker;
WriteMakefile(
    'NAME'		=> 'LogDriver',         # module name
    'VERSION_FROM'	=> 'LogDriver.pm',      # finds version
    'PREREQ_PM'         => { 'XML::SAX' => 0 }  # require XML::SAX
 );


sub MY::install {
    package MY;
    my $script = shift->SUPER::install(@_);
    $script =~ s/install :: (.*)$/install :: $1 install_sax_driver/m;
    $script .= <<"INSTALL";

    install_sax_driver :
	\t\@\$(PERL) -MXML::SAX -e "XML::SAX->add_parser(q(\$(NAME)))->save_parsers()"

INSTALL

    return $script;
}

