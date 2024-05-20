package Apache::DocBook;

use warnings;
use strict;

use Apache::Constants qw(:common);

use XML::LibXML;
use XML::LibXSLT;

our $xml_path;			# Document source directory
our $base_path;			# HTML output directory
our $xslt_file;			# path to DocBook-to-HTML XSLT stylesheet
our $icon_dir;                  # path to icons used in index pages

sub handler {
  my $r = shift;                # Apache request object
  # Get config info from Apache config
  $xml_path = $r->dir_config('doc_dir') or die "doc_dir Apache variable not set.\n";
  $base_path = $r->dir_config('html_dir') or die "html_dir Apache variable not set.\n";
  $icon_dir = $r->dir_config('icon_dir') or die "icon_dir Apache variable not set.\n";
  unless (-d $xml_path) {
    $r->log_reason("Can't use an xml_path of $xml_path: $!", $r->filename);
    die;
  }
  my $filename = $r->filename;

  $filename =~ s/$base_path\/?//;
  # Add in path info (the file might not actually exist... YET)
  $filename .= $r->path_info;

  $xslt_file = $r->dir_config('xslt_file') or die "xslt_file Apache variable not set.\n";
  
  # The subroutines we'll call after this will take care of printing
  # stuff at the client.

  # Is this an index request?
  warn "Got a filename of $filename.";
  if ( (-d "$xml_path/$filename") or ($filename =~ /index.html?$/) ) {
    warn "Looks like an index request.";
    # Why yes! We whip up an index page from the floating aethers.
    my ($dir) = $filename =~ /^(.*)(\/index.html?)?$/;
    # Semi-hack: stick trailing slash on URI, maybe.
    if (not($2) and $r->uri !~ /\/$/) {
      $r->uri($r->uri . '/');
    }
    make_index_page($r, $dir);
    return $r->status;
  } else {
    # No, it's a request for some other page.
    warn "Not an index request.";
    make_doc_page($r, $filename);
    return $r->status;
  }
  return $r->status;

}

sub transform {
  my ($filename, $html_filename) = @_;

  # make sure there's a home for this file.
  maybe_mkdir($filename);

  my $parser = XML::LibXML->new;
  my $xslt = XML::LibXSLT->new;

  # Because libxslt seems a little broken, we have to chdir to the
  # XSLT file's directory, else its file includes won't work. ;b
  use Cwd;                      # so we can get the current working dir
  my $original_dir = cwd;
  my $xslt_dir = $xslt_file;
  $xslt_dir =~ s/^(.*)\/.*$/$1/;
  chdir($xslt_dir) or die "Can't chdir to $xslt_dir: $!";

  my $source = $parser->parse_file("$xml_path/$filename");
  my $style_doc = $parser->parse_file($xslt_file);
  
  my $stylesheet = $xslt->parse_stylesheet($style_doc);
  
  my $results = $stylesheet->transform($source);

  open (HTML_OUT, ">$base_path/$html_filename");
  print HTML_OUT $stylesheet->output_string($results);
  close (HTML_OUT);

  # Go back to original dir
  chdir($original_dir) or die "Can't chdir to $original_dir: $!";

}

sub make_index_page {
  my ($r, $dir) = @_;

  # If there's no corresponding dir in the XML source, the request
  # goes splat

  my $xml_dir = "$xml_path/$dir";
  unless (-r $xml_dir) {
    unless (-d $xml_dir) {
      # Whoops, this ain't a directory.
      $r->status( NOT_FOUND );
      return;
    }
    # It's a directory, but we can't read it. Whatever.
    $r->status( FORBIDDEN );
    return;
  }
    
  # Fetch mtimes of this dir and the index.html in the corresponding
  # html dir
  my $index_file = "$base_path/$dir/index.html";

  my $xml_mtime = (stat($xml_dir))[9];
  my $html_mtime = (stat($index_file))[9];

  # If the index page is older than the XML dir, or if it simply
  # doesn't exist, we generate a new one.
  warn "Shall we dance? $index_file is $html_mtime, xml is $xml_dir is $xml_mtime.";
  if ((not($html_mtime)) or ($html_mtime <= $xml_mtime)) {
    warn "Yes.";
    generate_index($xml_dir, "$base_path/$dir", $r->uri);
    $r->filename($index_file);
    send_page($r, $index_file);
    return;
  } else {
    warn "No.";
    # The cached index page is fine. Let Apache serve it.
    $r->filename($index_file);
    $r->path_info('');
    send_page($r, $index_file);
    return;
  }
  
}

sub generate_index {
  my ($xml_dir, $html_dir, $base_dir) = @_;

  # Snip possible trailing / from base_dir 
  $base_dir =~ s|/$||;

  warn "Generating, with @_.";

  my $index_file = "$html_dir/index.html";

  my $local_dir;
  if ($html_dir =~ /^$base_path\/*(.*)/) {
    $local_dir = $1;
  } else {
    $local_dir = "POOP";
  }


  # make directories, if necessary
  maybe_mkdir($local_dir);
  warn "Generating index file...";
  open (INDEX, ">$index_file") or die "Can't write to $index_file: $!";
  
  opendir(DIR, $xml_dir) or die "Couldn't open directory $xml_dir: $!";
  chdir($xml_dir) or die "Couldn't chdir to $xml_dir: $!";

  # Set icon files
  my $doc_icon = "$icon_dir/generic.gif";
  my $dir_icon = "$icon_dir/folder.gif";

  # Make the displayable name of $local_dir (probably the same)
  my $local_dir_label = $local_dir || 'document root';

  # Print start of page
  print INDEX <<END;
<html>
<head><title>Index of $local_dir_label</title></head>
<body>
<h1>Index of $local_dir_label</h1>
<table width="100%">
END
  
  # Now print one row per file in this dir

  while (my $file = readdir(DIR)) {
    # ignore dotfiles & directories & stuff
    if (-f $file && $file !~ /^\./) {
      # Create parser objects 
      warn "Indexing $file.";
      my $parser = XML::LibXML->new;
      
      # Check for well-formedness, skip if yukky:
      warn "Got parser: $parser";
      eval {$parser->parse_file($file);};
      if ($@) {
        warn "Blecch, not a well-formed XML file.";
        warn "Error was: $@";
        next;
      }
      
      my $doc = $parser->parse_file($file);
      
      my %info;                   # Will hold presentable info
      # Determine root type
      my $root = $doc->documentElement;
      my $root_type = $root->getName;
      warn "Root type is $root_type";
      # Now try to get an appropriate info node, which is named $FOOinfo
      my ($info) = $root->findnodes("${root_type}info");
      if ($info) {
        # Yay, an info element for us. Fill it %info with it.
        if (my ($abstract) = $info->findnodes('abstract')) {
          $info{abstract} = $abstract->string_value;
        } elsif ($root_type eq 'reference') {
          # We can usee first refpurpose as our arbstract instead.
          if ( ($abstract) = $root->findnodes('/reference/refentry/refnamediv/refpurpose')) {
            $info{abstract} = $abstract->string_value;
          }
        }
        if (my ($date) = $info->findnodes('date')) {
          $info{date} = $date->string_value;
        }
      }
      if (my ($title) = $root->findnodes('title')) {
        $info{title} = $title->string_value;
      }
      # Fill in %info stuff we don't need the XML for...
      unless ($info{date}) {
        my $mtime = (stat($file))[9];
        $info{date} = localtime($mtime);
      }
      $info{title} ||= $file;
      # That's enough info. Let's build an HTML table row with it.
      print INDEX "<tr>\n";
      # Figure out a filename to link to -- foo.html
      my $html_file = $file;
      $html_file =~ s/^(.*)\..*$/$1.html/;
      print INDEX "<td>";
      print INDEX "<img src=\"$doc_icon\">" if $doc_icon;
      print INDEX "<a href=\"$base_dir/$html_file\">$info{title}</a></td> ";
      foreach (qw(abstract date)) {
        print INDEX "<td>$info{$_}</td> " if $info{$_};
      }
      print INDEX "\n</tr>\n";
    } elsif (-d $file) {
      # Just make a directory link.
      # ...unless it's an ignorable directory.
      next if grep (/^$file$/, qw(RCS CVS .)) or ($file eq '..' and not $local_dir);
      print INDEX "<tr>\n<td>";
      print INDEX "<a href=\"$base_dir/$file\"><img src=\"$dir_icon\">" if $dir_icon;
      print INDEX "$file</a></td>\n</tr>\n";
    }
  }


  # Close the table and end the page
  print INDEX <<END;
</table>
</body>
</html>
END
  
  close(INDEX) or die "Can't close $index_file: $!";
  closedir(DIR) or die "Can't close $xml_dir: $!";
}

sub make_doc_page {
  my ($r, $html_filename) = @_;

  # Generate a source filename by replacing existing extension with .xml
  my $xml_filename = $html_filename;
  $xml_filename =~ s/^(.*)(?:\..*)$/$1.xml/;

  # If there's a problem reading the source XML file, so it goes with
  # the result HTML.
  unless (-r "$xml_path/$xml_filename") {
    unless (-e "$xml_path/$xml_filename") {
      $r->status( NOT_FOUND );
      return;
    } else {
      # Exists, but no read permissions, shrug.
      $r->status( FORBIDDEN );
      return;
    }
  }

  # Fetch mtimes of this file and corresponding html file
  my $xml_mtime = (stat("$xml_path/$xml_filename"))[9];
  my $html_mtime = (stat("$base_path/$html_filename"))[9];
  # If the html file is older than the xml XML file, or if it simply
  # doesn't exist, generate a new one
  
  if ((not($html_mtime)) or ($html_mtime <= $xml_mtime)) {
    transform($xml_filename, $html_filename);
    $r->filename("$base_path/$html_filename");
    $r->status( DECLINED );
    return;
  } else {
    # It's cached. Let Apache serve up the existing file.
    $r->status( DECLINED );
  }  
}

sub send_page {
  my ($r, $html_filename) = @_;
  # Problem here: if we're creating the file, we can't just write it
  # and say 'DECLINED', cuz the default server handle hits us with a
  # file-not-found. Until I find a better solution, I'll just spew
  # the file, and DECLINE only known cache-hits.
  $r->status( OK );
  $r->send_http_header('text/html');
  
  open(HTML, "$html_filename") or die "Couldn't read $base_path/$html_filename: $!";
  while (<HTML>) {
    $r->print($_);
  }
  close(HTML) or die "Couldn't close $html_filename: $!";
  return;
}

sub maybe_mkdir {
  # Given a path, make sure directories leading to it exist, mkdir-ing
  # any that dont.
  my ($filename) = @_;
  my @path_parts = split(/\//, $filename);
  # if the last one is a filename, toss it out.
  pop(@path_parts) if -f $filename;
  my $traversed_path = $base_path;
  foreach (@path_parts) {
    $traversed_path .= "/$_";
    unless (-d $traversed_path) {
      mkdir ($traversed_path) or die "Can't mkdir $traversed_path: $!";
    }
  }
  return 1;
}
