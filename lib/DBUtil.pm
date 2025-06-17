package DBUtil;
use CGI::Carp qw(warningsToBrowser);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use Time::Local;
use DateTime;
use Cwd;
use myDBI;
############################################################################
# Date routine
#   InDate = date to reformat or dateofbirth or first diff date
#            (date must be in format YYYY-MM-DD or YYYY/MM/DD)
#   Type   =  'age' or 'fmt' or 'diff' 
#             or
#             a (+/-) integer for months to (add/subtract)
#   Str    =  fmt string, i.e. MM/DD/YY
#             or 
#             if age, date to calculate instead of using today
#             or
#             second diff date
#             or 
#             a (+/-) integer for days to (add/subtract)
#   Null Dates default to current date.
#
#   i.e. &Date();
#        returns today in format YYYY-MM-DD
#   i.e. &Date($mydate,'fmt','YYMMDD');
#        returns $mydate in format YYMMDD
#   i.e. &Date($mydate,1,-1);
#        returns $mydate plus 1 month minus 1 day.
#   these return 2 dates...
#   given date, type, str --- str increases/decreases by month always.
#   i.e. &Date('2000-12-16','monthly',0); returns '2000-12-01', '2000-12-31'
#   i.e. &Date('2000-12-16','monthly',-1); returns '2000-11-01', '2000-11-30'
#   i.e. &Date('2000-12-16','quarterly',0); returns '2000-11-01', '2001-01-31'
#   i.e. &Date('2000-12-16','quarterly',-1); returns '2000-10-01', '2000-12-31'
#   i.e. &Date('2000-12-16','annual',0); returns '2000-01-01', '2000-12-31'
#   i.e. &Date('2000-12-16','annual',-1); returns '1999-01-01', '1999-12-31'
############################################################################
sub Date($;$$)
{
  my ($self, $InDate, $Type, $Str) = @_;

#warn "Date: InDate=$InDate, Type=$Type, Str=$Str\n";
  my @DaysArray = (Sun,Mon,Tue,Wed,Thu,Fri,Sat);
  my @MonthsArray = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec);
  my @MonthsLongArray = (January,Febuary,March,April,May,June,July,August,September,October,November,December);
  my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime();
  my $dayname = @DaysArray[$wday];
  my $monthname = @MonthsArray[$month];
  $month++; $year +=1900;
  my ($Day, $Mon, $Year, $Julian);
  my ($byr, $bmon, $bday, $Age);
  my ($Date1, $Date2, $diff);

  if ( $Type =~ /dob/i || $Type =~ /age/i )
  { 
    return() if ( $InDate eq '' || $InDate eq '0000-00-00' );
    ($byr, $bmon, $bday) = $InDate =~ /(\d*)-(\d*)-(\d*)/;
    # calculate from date given in Str or today if not.
    ($year, $month, $day) = $Str =~ /(\d*)-(\d*)-(\d*)/ if $Str;
    $Age = $year - $byr;
    $month < $bmon && $Age--;
    $month == $bmon && $day < $bday && $Age--;
    return $Age;
  }
  elsif ( $Type =~ /stamp/i )
  {
    if ( $Str =~ /long/ )
    {
      my $tm = 'AM';
      if ( $hrs > 12 ) { $hrs-=12; $tm='PM'; }
      elsif ( $hrs == 12 ) { $tm='PM'; }
      $min = length($min) == 2 ? $min : '0'.$min;
      return("$dayname, $monthname $day, $year @ $hrs:$min $tm");
    }
    else
    {
      $month = length($month) == 2 ? $month : '0'.$month;
      $day = length($day) == 2 ? $day : '0'.$day;
      $hrs = length($hrs) == 2 ? $hrs : '0'.$hrs;
      $min = length($min) == 2 ? $min : '0'.$min;
      $sec = length($sec) == 2 ? $sec : '0'.$sec;
      return($year . $month . $day . $hrs . $min . $sec);
    }
  }
  elsif ( $Type =~ /diff/i )
  {
    $Date1 = $InDate;
    $Date1 = "$year-$month-$day" if ( !$InDate || $InDate =~ 'today' );
    $Date2 = $Str;
    $Date2 = "$year-$month-$day" if ( !$Str || $Str =~ 'today' );
    $diff = $self->getDays($Date1) - $self->getDays($Date2);
    return($diff);
  }
  elsif ( $Type =~ /dow/i )
  {
#   wday(Time[6]) makes it all rotate around today's dow.
    my $days = $self->getDays($InDate) - $self->getDays("$year-$month-$day");
    my $dow = (($wday + $days) % 7);
    return($dow);
  }
  elsif ( $Type =~ /fmt/i )
  {
    return() if ( $InDate eq '' || $InDate eq '0000-00-00' );
    if ( $InDate =~ /today/i )
    {
      $Year = $year;
      $julian++;
      $julian = length($julian) == 2 ? $julian : '0'.$julian;
      $Julian = length($julian) == 3 ? $julian : '0'.$julian;
    }  
    elsif ( $InDate =~ /-/i )
    { ($Year, $month, $day) = split(/-/, $InDate); }
    else
    { ($Year, $month, $day) = split(/\//, $InDate); }
   
    $year = substr($Year, -2);
    $month+=0; $day+=0;
    $Mon = length($month) == 2 ? $month : '0'.$month;
    $Day = length($day) == 2 ? $day : '0'.$day;
    my $MonthName = @MonthsArray[$month-1];
    my $MonthLongName = @MonthsLongArray[$month-1];
    my $suffix = $day == 1 || $day == 21 || $day == 31 ? 'st'
               : $day == 2 || $day == 22 ? 'nd'
               : $day == 3 || $day == 23 ? 'rd'
               : 'th';
    my $NewDateStr = $Str;
    $NewDateStr =~ s/MONTH/$MonthLongName/g;
    $NewDateStr =~ s/MON/$MonthName/g;
    $NewDateStr =~ s/YYYY/$Year/g;
    $NewDateStr =~ s/YY/$year/g;
    $NewDateStr =~ s/MM/$Mon/g;
    $NewDateStr =~ s/DD/$Day/g;
    $NewDateStr =~ s/M1/$month/g;
    $NewDateStr =~ s/D1/$day/g;
    $NewDateStr =~ s/SUF/$suffix/g;
    $NewDateStr =~ s/JJJ/$Julian/g;
    $NewDateStr =~ s/JJ/$julian/g;
    return($NewDateStr);
  }
  elsif ( $Type =~ /monthly/i )
  {
#warn "$inDate,$Str\n";
    if ( $Str ) 
    { 
      $bDate = $self->Date($InDate,$Str);
      ($year, $month, $day) = $bDate =~ /(\d*)-(\d*)-(\d*)/;
    }
    elsif ( $InDate && $InDate !~ /today/i )
    { ($year, $month, $day) = $InDate =~ /(\d*)-(\d*)-(\d*)/; }
#warn "$InDate,$year,$month,$day\n";
    my $maxDay = $self->daysInMonth($year,$month);
    $month = '0'. $month if ( length($month) < 2 );
#warn "return: $year,$month,$day,$maxDay\n";
    return("$year-$month-01", "$year-$month-$maxDay");
  }
  elsif ( $Type =~ /quarterly/i )
  {
    if ( $Str ) 
    { 
      $bDate = $self->Date($InDate,$Str*3);
      ($year, $month, $day) = $bDate =~ /(\d*)-(\d*)-(\d*)/;
    }
    elsif ( $InDate && $InDate !~ /today/i )
    { ($year, $month, $day) = $InDate =~ /(\d*)-(\d*)-(\d*)/; }
    my $maxDay = $self->daysInMonth($year,$month);
    $month = '0'. $month if ( length($month) < 2 );
    my $eDate = "$year-$month-$maxDay";
    my $bDate = "$year-$month-01";
    $bDate = $self->Date($bDate,-2,0);
    return($bDate, $eDate);
  }
  elsif ( $Type =~ /annual/i )
  {
    if ( $Str ) 
    { 
      $bDate = $self->Date($InDate,$Str*12);
      ($year, $month, $day) = $bDate =~ /(\d*)-(\d*)-(\d*)/;
    }
    elsif ( $InDate && $InDate !~ /today/i )
    { ($year, $month, $day) = $InDate =~ /(\d*)-(\d*)-(\d*)/; }
    return("$year-01-01", "$year-12-31");
  }
  elsif ( $Type == 0 && $Str == 0 )
  {
    if ( $InDate && $InDate !~ /today/i )
    { ($year, $month, $day) = $InDate =~ /(\d*)-(\d*)-(\d*)/; }
  }
  elsif ( $Type || $Str )
  {
    return() if ( $InDate eq '0000-00-00' );
    my $aMonth = $Type + 0;
    my $aDay = $Str + 0;
#warn qq|InDate=$InDate, aMonth=$aMonth, aDay=$aDay\n|;
    if ( $InDate && $InDate !~ /today/i )
    { ($year, $month, $day) = $InDate =~ /(\d*)-(\d*)-(\d*)/; }

#warn qq|year=$year, month=$month, day=$day\n|;
    $month += $aMonth;
    while ( $month > 12 ) { $month-=12; $year+=1; }
    while ( $month < 1 ) { $month+=12; $year-=1; }
#warn qq|year=$year, month=$month, day=$day\n|;
    my $maxDay = $self->daysInMonth($year,$month);
#warn qq|isleap=$isleap, maxDay=$maxDay\n|;
##   if we want month to stay within next month
##    while ( $day > $maxDay ) { $day -= 1; }
    $day += $aDay;
    $day = $maxDay if ( $aDay < 0 && $day > $maxDay );
#warn qq|before while: year=$year, month=$month, day=$day\n|;
    while ( $day > $maxDay ) 
    {
      $day -= $maxDay; 
      $month+=1;
      if ( $month > 12 ) { $month-=12; $year+=1; }
      $maxDay = $self->daysInMonth($year,$month);
#warn qq|in while: year=$year, month=$month, day=$day\n|;
    }
#warn qq|next while: year=$year, month=$month, day=$day\n|;
    while ( $day < 1 ) 
    {
      $month-=1;
      if ( $month < 1 ) { $month+=12; $year-=1; }
      $maxDay = $self->daysInMonth($year,$month);
      $day += $maxDay; 
#warn qq|in while: year=$year, month=$month, day=$day\n|;
    }
#warn qq|end while: year=$year, month=$month, day=$day\n|;
  }
  $month = length($month) == 2 ? $month : '0'.$month;
  $day = length($day) == 2 ? $day : '0'.$day;
#warn qq|return: $year-$month-$day\n|;
  return("$year-$month-$day");
}
############################################################################
sub daysInMonth($$)
{
  my ($self, $year, $month) = @_;
#warn "daysInMonth: year=$year, month=$month\n";
  my $isleap = ($year % 4 == 0 && ($year % 100 != 0 || $year % 400 == 0));
  if ( $month==4 || $month==6 || $month==9 || $month==11 ) { return(30); }
  elsif ( $month==2 ) 
  { if ( $isleap ) { return(29); } else { return(28); } }
  else { return(31); }
  return(30);
}
# returns number of days since 1/1/2000.
sub getDays($)
{
  my ($self, $InDate) = @_;

#warn "getDays: InDate=$InDate\n";
  ($year, $month, $day) = $InDate =~ /(\d+)-(\d+)-(\d+)/;
  my ($totDays, $yrDays) = (0,0);
  my $yr = $year;
  while ( $yr > 2000 )
  {
    $yr--;
    my $isleap = ($yr % 4 == 0 && ($yr % 100 != 0 || $yr % 400 == 0));
    if ( $isleap ) { $yrDays = 366; } else { $yrDays = 365; }
    $totDays += $yrDays;
  }
  $yr=$year+1;
  while ( $yr < 2000 )
  {
    my $isleap = ($yr % 4 == 0 && ($yr % 100 != 0 || $yr % 400 == 0));
    if ( $isleap ) { $yrDays = 366; } else { $yrDays = 365; }
    $totDays -= $yrDays;
    $yr++;
  }
  my $isleap = ($year % 4 == 0 && ($year % 100 != 0 || $year % 400 == 0));
  if ( $isleap ) { $yrDays = 366; } else { $yrDays = 365; }
  $julian = $day;
  $mon = $month - 1;
  while ( $mon > 0 )
  {
    if ( $mon==4 || $mon==6 || $mon==9 || $mon==11 ) { $maxDay = 30; }
    elsif ( $mon == 2 ) { if ( $isleap ) { $maxDay = 29; } else { $maxDay = 28; }; }
    else { $maxDay = 31; }
    $julian += $maxDay;
    $mon--;
  }
  if ( $year < 2000 ) { $julian = -($yrDays - $julian); }
  $diff = $totDays + $julian;
  return $diff;
}

sub SundayOfWeek
{
  my ($self,$year,$week) = @_;
  # Week 1 is defined as the one containing January 4:
  my $dt = DateTime
    ->new( year => $year, month => 1, day => 4 )
    ->add( weeks => ($week - 1) )
    ->truncate( to => 'week' )
    ->subtract( days => 1 );            # to get Sunday.
  my $mon = length($dt->month) == 1 ? '0'.$dt->month : $dt->month;  
  my $day = length($dt->day) == 1 ? '0'.$dt->day : $dt->day;  
  my $d = $year.'-'.$mon.'-'.$day;
  return($d);
}

sub vDate
{
  my ($self,$idate,$today,$min,$max) = @_;
  my @MonthsArray = ('',Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec);
#warn qq|idate=$idate\n|;
  $idate = $today if ( $idate eq 't' || $idate eq 'T' );
  ## YYYY/MM/DD   YYYY-MM-DD
  my ($yr,$d1,$mon,$d2,$day) = 
    $idate =~ /^(\d{4})(\/|-)(\d{1,2})(\/|-)(\d{1,2})$/;
#warn qq|yr=$yr,d1=$d1,mon=$mon,d2=$d2,day=$day\n|;
  if ($yr eq '')
  {
    ## MM/DD/YY   MM/DD/YYYY   MM-DD-YY   MM-DD-YYYY
    ($mon,$d1,$day,$d2,$yr) = 
      $idate =~ /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/;
#warn qq|yr=$yr,d1=$d1,mon=$mon,d2=$d2,day=$day\n|;
    if ($yr eq '')
    { return("Date is not in a valid format.\n(yyyy/mm/dd or mm/dd/yyyy)\nMake sure year is 4 digits.\nYou can use a 'T' for todays date.",$idate); }
  }
  if ($mon < 1 || $mon > 12)    # check month range
  { return("Month must be between 1 and 12.",$idate); }
  if ($day < 1 || $day > 31) 
  { return("Day must be between 1 and 31.",$idate); }
  if (($mon==4 || $mon==6 || $mon==9 || $mon==11) && $day==31) 
  { return("Month '@MonthsArray[$mon]' doesn't have 31 days!",$idate); }
  if ($mon == 2)                 # check for february 29th
  { 
    my $isleap = ($yr % 4 == 0 && ($yr % 100 != 0 || $yr % 400 == 0));
    if ($day>29 || ($day==29 && !$isleap)) 
    { return("February doesn't have ${day} days!",$idate); }
  }
  if ($yr < 2000 ) 
  { return("Year must be greater than 2000.",$idate); }

# idate is valid.
  if ( length($mon) < 2 ) { $mon = '0'.$mon; }
  if ( length($day) < 2 ) { $day = '0'.$day; }
  my $validDate = "${yr}-${mon}-${day}";
#warn qq|validDate=$validDate\n|;

  unless ( $min eq '' )
  {
#warn qq|min=$min\n|;
    if ( $validDate lt $min )
    { return("Date '${idate}' is before earliest date allowed (${min})!",$idate); }
  }
  unless ( $max eq '' )
  {
#warn qq|max=$max\n|;
    if ( $validDate gt $max )
    { return("Date '${idate}' is after lastest date allowed (${max})!",$idate); }
  }

#warn qq|vDate: =$validDate\n|;
  return('',$validDate);
}
sub vTime
{
  my ($self,$itime,$now) = @_;
  my $err = '';
  $itime = $now if ( $itime eq 'n' || $itime eq 'N' );
  my ($hrs,$d1,$min,$d2,$sec,$ampm) = 
    $itime =~ /^(\d{1,2})(\:|\.)?(\d{2})?(\:|\.)?(\d{2})?(\s?(A|a|AM|am|P|p|PM|pm|))?$/;
#warn qq|hrs=$hrs,d1=$d1,min=$min,d2=$d2,sec=$sec,ampm=$ampm\n|;
  if ($ampm eq "a" || $ampm eq "am" || $ampm eq "A" || $ampm eq "AM")
  { $ampm = "AM"; }
  elsif ($ampm eq "p" || $ampm eq "pm" || $ampm eq "P" || $ampm eq "PM")
  { $ampm = "PM"; }
  else { $ampm = ""; }
  $min = 0 unless ( $min );
  $sec = 0 unless ( $sec );
  if ($hrs eq '')
  { $err = "Incorrect Time format (minutes/seconds must be 2 digits)"; }
  elsif ($hrs < 0 || $hrs > 23)
  { $err = "Hour must be between 1 and 12.\n(or 0 and 23 for military time)"; }
  elsif ($hrs < 12 && $ampm eq '')
  { $err = "You must specify AM or PM."; }
  elsif  ($hrs > 12 && $ampm eq "AM" ) 
  { $err = "You can't specify AM in this case."; }
  elsif ($min<0 || $min > 59) 
  { $err = "Minute must be between 0 and 59."; }
  elsif ($sec && ($sec < 0 || $sec > 59)) 
  { $err = "Second must be between 0 and 59."; }
  if ( length($hrs) < 2 ) { $hrs = '0'.$hrs; }
  if ( length($min) < 2 ) { $min = '0'.$min; }
  if ( length($sec) < 2 ) { $sec = '0'.$sec; }
  if ( $ampm eq "AM" && $hrs == 12 ) { $hrs = '00'; }
  elsif ( $ampm eq "PM" && $hrs < 12 ) { $hrs += 12; }
  return($err,"${hrs}:${min}:${sec}");
}
sub AMPM($)
{
  my ($self, $Time) = @_;

  return $Time if ( $Time eq '' );

  $Time =~ /0?(\d*):(\d*)/;
  if ( $1 == 0 )     { $Time = "12:$2AM"; } 
  elsif ( $1 < 12 )  { $Time = "$1:$2AM"; }
  elsif ( $1 == 12 ) { $Time = "$1:$2PM"; }
  elsif ( $1 < 24 )  { $Time = $1 - 12 . ':' . $2 . 'PM'; }
  else  { $Time = $1 - 24 . ':' . $2 . 'AM'; }
  return $Time;
}
############################################################################
# use Times as from Notes: ie: 12:11:30
sub getDuration
{
  my ($self, $BegTime, $EndTime) =@_;

  my ($Bhrs, $Bmin, $Bsec) = split(/:/,$BegTime);
  $Btotal = ($Bhrs * 3600) + ($Bmin * 60) + $Bsec;
  my ($Ehrs, $Emin, $Esec) = split(/:/,$EndTime);
  $Etotal = ($Ehrs * 3600) + ($Emin * 60) + $Esec;
  $Diff = $Etotal - $Btotal;
#warn qq|Diff=$Diff, Btotal=$Btotal, Etotal=$Etotal, Bhrs=$Bhrs, Bmin=$Bmin, Ehrs=$Ehrs, Emin=$Emin, $Bsec, $Esec\n|;
  return($Diff);
}
##
# uses a timpstamp: ie: 20100415121130
sub getDurationTS
{
  my ($self, $BegStamp, $EndStamp) =@_;

#warn qq|getDuration: $BegStamp, $EndStamp\n|;
  my $Date1 = substr($BegStamp,0,4) . '-' . substr($BegStamp,4,2) . '-' . substr($BegStamp,6,2);
  my $Date2 = substr($EndStamp,0,4) . '-' . substr($EndStamp,4,2) . '-' . substr($EndStamp,6,2);
  my $Days = $self->getDays($Date2) - $self->getDays($Date1);
#warn qq|$Date1, $Date2, $Days\n|;
  my $Bhrs = substr($BegStamp,8,2);
  my $Bmin = substr($BegStamp,10,2);
  my $Bsec = substr($BegStamp,12,2);
#warn qq|$Bhrs, $Bmin, $Bsec, $Btotal\n|;
  $Btotal = ($Bhrs * 3600) + ($Bmin * 60) + $Bsec;
  my $Ehrs = substr($EndStamp,8,2);
  my $Emin = substr($EndStamp,10,2);
  my $Esec = substr($EndStamp,12,2);
  $Etotal = ($Ehrs * 3600) + ($Emin * 60) + $Esec + ($Days * 86400);
#warn qq|$Ehrs, $Emin, $Esec, $Etotal\n|;
  $Diff = $Etotal - $Btotal;
  return($Diff);
}
############################################################################
##
# check to get rid of form->{thisweek} and form->{lastpay} and other form not 'daterange'
sub setDates
{
  my ($self,$form) = @_;
  my $trash;
#foreach my $f ( sort keys %{$form} ) { warn "setDates: form-$f=$form->{$f}\n"; }
  if ( $form->{daterange} eq 'thisweek' || $form->{thisweek} )
  {
    my ($BILLDATE,$NEXTBILLDATE) = cBill->getBillDate();
    $form->{FromDate} = ${BILLDATE};
    $form->{ToDate} = DBUtil->Date($NEXTBILLDATE,0,-1);
  }
  elsif ( $form->{daterange} eq 'lastweek' )
  {
    my ($BILLDATE,$NEXTBILLDATE) = cBill->getBillDate();
    $form->{FromDate} = DBUtil->Date($BILLDATE,0,-7);
    $form->{ToDate} = DBUtil->Date($BILLDATE,0,-1);
  }
  elsif ( $form->{daterange} eq 'lastpay' || $form->{lastpay} )
  {
    my ($BEGINDATE,$ENDDATE) = cBill->getPayDates();
    $form->{FromDate} = ${BEGINDATE};
    $form->{ToDate} = ${ENDDATE};
  }
  elsif ( $form->{daterange} eq 'thismonth' || $form->{thismonth} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','monthly'); }
  elsif ( $form->{daterange} eq 'lastmonth' || $form->{lastmonth} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','monthly',-1); }
  elsif ( $form->{daterange} eq 'nextmonth' || $form->{nextmonth} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','monthly',1); }
  elsif ( $form->{daterange} eq 'last3m' )
  {
    ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','monthly',-1);
    ($form->{FromDate}, $trash) = DBUtil->Date('','monthly',-3);
  }
  elsif ( $form->{daterange} eq 'last6m' )
  {
    ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','monthly',-1);
    ($form->{FromDate}, $trash) = DBUtil->Date('','monthly',-6);
  }
  elsif ( $form->{daterange} eq 'back1m' )
  {
    $form->{FromDate} = DBUtil->Date('',-1);
    $form->{ToDate} = DBUtil->Date();
  }
  elsif ( $form->{daterange} eq 'back6m' )
  {
    $form->{FromDate} = DBUtil->Date('',-6);
    $form->{ToDate} = DBUtil->Date();
  }
  elsif ( $form->{daterange} eq 'back12m' )
  {
    $form->{FromDate} = DBUtil->Date('',-12);
    $form->{ToDate} = DBUtil->Date();
  }
  elsif ( $form->{daterange} eq 'lastquarter' || $form->{lastquarter} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','quarterly',-1); }
  elsif ( $form->{daterange} eq 'thisquarter' || $form->{thisquarter} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','quarterly'); }
  elsif ( $form->{daterange} eq 'thisyear' || $form->{thisyear} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','annual'); }
  elsif ( $form->{daterange} eq 'lastyear' || $form->{lastyear} )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','annual',-1); }
  elsif ( $form->{daterange} eq '2yago' )
  { ($form->{FromDate}, $form->{ToDate}) = DBUtil->Date('','annual',-2); }
  elsif ( $form->{daterange} eq 'all' )
  {
    $form->{FromDate} = '2000-01-01';
    $form->{ToDate} = $form->{TODAY};
  }
  elsif ( $form->{daterange} eq 'today' )
  {
    $form->{FromDate} = $form->{TODAY};
    $form->{ToDate} = $form->{TODAY};
  }
  $form->{FromDate} = '2000-01-01' if ( $form->{FromDate} eq '' );
  $form->{ToDate} = $form->{TODAY} if ( $form->{ToDate} eq '' );
  $form->{TheDate} = $form->{TODAY} if ( $form->{TheDate} eq '' );
  $form->{FromDateD} = $form->{FromDate} eq '2000-01-01' ? 'Start'
                     : DBUtil->Date($form->{FromDate},'fmt','MM/DD/YYYY');
  $form->{ToDateD} = DBUtil->Date($form->{ToDate},'fmt','MM/DD/YYYY');
  return($form);
}
############################################################################
# FmtStr: InStr, InLen, Just, InChr
#   Just: c=center, r=right, n=numbers right|text left, otherwise=left
sub FmtStr($$;$$)
{
  my ($self, $InStr, $InLen, $Just, $InChr) = @_;

#warn "FmtStr: $InStr, $InLen, $Just\n";
  my $StrLen = length($InStr);
  my $Chr = $InChr eq '' ? ' ' : $InChr;
  my ($Str, $Cnt) = ('', 0);
  if ( $StrLen == $InLen ) { $Str = $InStr; }
  elsif ( $StrLen > $InLen ) { $Str = substr($InStr,0,$InLen); }
  else
  { 
#warn "FmtStr: Just=$Just\n";
    if ( $Just =~ /c/i )
    { 
      $Cnt = int(($InLen - $StrLen) / 2);
      $Str = $Chr x $Cnt . $InStr . $Chr x $Cnt;
      $Str .= $Chr if (length($Str) < $InLen);
    }
    elsif ( $Just =~ /r/i )
    { $Str = $Chr x int($InLen - $StrLen) . $InStr; }
    elsif ( $Just =~ /n/i )
    {
      if ( $self->isnum($InStr) )
      { $Str = $Chr x int($InLen - $StrLen) . $InStr; }
      else
      { $Str = $InStr . $Chr x int($InLen - $StrLen); }
    }
    else
    { $Str = $InStr . $Chr x int($InLen - $StrLen); }
  }
#warn "FmtStr: return *$Str*\n";
  return($Str);
}
sub isnum
{
  my ($self, $num) = @_;
  if ( $num =~ /^-?(?:\d+(?:\.\d*)?|\.\d+)$/ ) { return(1); }
  return(0);
}
############################################################################
sub parse_lines
{
  my ($self,$text,$maxperline) = @_;
  my $in = $text . ' ';
  my @strs = ();
  my $str = '';
  while ($in =~ /\s+/) 
  {
    $m=$&;                          # what matched
    $w=$`;                          # before what matched
    if ( length($str) + length($w) < $maxperline )
    { $str .= $w . $m; } else { push(@strs,$str); $str = $w . $m; }
    $in = $';                       # now set to after what matched
  }
  push(@strs,$str) if ( length($str) > 0 );
  return(@strs);
}
sub parse_args
{
  my ($self, $str, $dbug) = @_;

  my ($chrs,$f,$set) = ('',0,0);
  my @new = ();
  foreach my $chr ( split(//,$str) )
  {
    if ( $chr eq '(' )
    {
print " IF(: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
      $f+=1;
      $chrs .= $chr;
print " IF(: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
    }
    elsif ( $chr eq ')' )
    {
print " IF): chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
      $f-=1;
      $chrs .= $chr;
print " IF): chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
    }
    elsif ( $chr eq ',' )
    {
print " IF,: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
      if ( $f>0 ) 
      {
        $chrs .= $chr;
      }
      else { $set = 1; }
print " IF,: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
    }
    else 
    { 
      $chrs .= $chr;
print " ELS: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug ); 
    }
    if ( $set && $chrs )
    {
print " SET: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
      push(@new,$chrs);
print " SET: chr=$chr, i=$i, set=$set, chrs=$chrs= f=$f\n" if ( $dbug );
      $chrs = ''; $set = 0; $f = 0;
    }
  }
  if ( !$set && $chrs ) { push(@new,$chrs); }
  return(@new);
}

############################################################################
# this one needs to work in a GET or POST
##
sub genToken
{
  my ($self,$Size) = @_;
  my $TokenLength = $Size ? $Size : '6';
  @Chars = ('A' .. 'N', 'P' .. 'Z', 
            'a' .. 'k', 'm' .. 'z', 
            '2' .. '9');
  $Cnt = scalar @Chars;
  my $Token = '';
  for ( my $i = 0; $i < $TokenLength; $i++ ) { $Token .= $Chars[int(rand($Cnt))]; }
  return($Token);
}

############################################################################
# test for null and not null.
sub isNULL { my ($self,$Test) = @_; if ( $Test eq '' ) { return(1); } else { return(0); } }
sub isNOTNULL { my ($self,$Test) = @_; if ( $Test ne '' ) { return(1); } else { return(0); } }
sub isTRUE($) { my ($self,$Test) = @_; if ( $Test ) { return(1); } else { return(0); } }
sub isFALSE($) { my ($self,$Test) = @_; if ( !$Test ) { return(1); } else { return(0); } }
sub isEQ($) { my ($self,$A,$B) = @_; if ( $A == $B ) { return(1); } else { return(0); } }
sub isGTE($) { my ($self,$A,$B) = @_; if ( $A >= $B ) { return(1); } else { return(0); } }
sub isLTE($) { my ($self,$A,$B) = @_; if ( $A <= $B ) { return(1); } else { return(0); } }
sub isEQSTR($) { my ($self,$A,$B) = @_; if ( $A eq $B ) { return(1); } else { return(0); } }
sub quoteSTR($) { my ($self,$form,$S) = @_; my $dbh=myDBI->dbconnect($form->{'DBNAME'}); return($dbh->quote($S)); }
sub divNUM($) { my ($self,$x,$y) = @_; if ( $y > 0 ) { return($x/$y); } else { return(0); } }

############################################################################
# Send an email to Provider
sub emailP
{
  my ($self, $form, $ProvID, $Subject, $field) = @_;
  my $result = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from Provider where ProvID=${ProvID}");
  $s->execute() || $form->dberror("EmailPP->select ProvID=${ProvID}");
  my $r = $s->fetchrow_hashref;
  if ( $r->{Email} ne '' )
  {
    (my $To = $r->{'Email'}) =~ s/\'/\\'/g;
    my $Text = $form->{$field};
    $self->email($form, $To, $Subject, $Text, '', 1);
  }
  $s->finish();
  return($result);
}
# Send an email.
sub email
{
  my ($self, $form, $Address, $Subject, $Text, $Afile, $AddrOnly) = @_;

if ( $form->{'DBNAME'} eq 'okmms_dev' )
{
warn qq|Address=${Address}\n|;
warn qq|Subject=${Subject}\n|;
warn qq|Text=${Text}\n|;
warn qq|Afile=${Afile}\n|;
warn qq|AddrOnly=${AddrOnly}\n|;
return(1);
}
  
  my $errs;
  (my $To = $Address) =~ s/\'/\\'/g;
# add support to all emails (except PA Expires)
  if ( $AddrOnly || $To =~ /support\@okmis.com/ || $To =~ /billing\@okmis.com/ )
  { null; } else { $To .= qq| support\@okmis.com| }
#warn qq| To=${To}\n|;
  my $Mutt = "| mutt ";
  $Mutt .= ${Subject} ? qq|-s "${Subject}" | : '';
  foreach my $fn ( split(' ',$Afile) )
  {
    if ( -f $fn ) { $Mutt .= qq|-a $fn |; }
    else { $errs .= "attach file not found: $fn\n"; }
  }
  $Mutt .= qq| -- ${To}|;
#warn qq|email: LOGINID=$form->{LOGINID}\n|;
  open( MUTT, $Mutt ) or die "Cannot connect to mutt ($!) ($Mutt) (Email)";
  if ( $form->{LOGINID} eq 'root' )
  { print MUTT qq|${errs}${Text}\n\nServer (okmis)|; }
  elsif ( $form->{LOGINID} )
  { print MUTT qq|${errs}${Text}\n\n$form->{LOGINUSERNAME} ($form->{LOGINID})|; }
  else 
  { print MUTT qq|${errs}${Text}\n\nServer (okmis)|; }
  close(MUTT);
#warn qq|email DONE\n|;
  return(1);
}
############################################################################
# Execute a system (shell/perl) Command
sub ExecCmd
{
  my ($self, $cmd, $sfx) = @_;
  my $outfile = $self->genToken() . '_' . $self->Date('','stamp') . '.uec';
  my $warnfile = $sfx ? "2>${outfile}${sfx}" : '2>&1';
#my $pwd=cwd();
#warn "ExecCmd: pwd=$pwd, cmd=$cmd\n";
#warn "ExecCmd: outfile=$outfile\n";
  $ENV{USERPROFILE} ||= "C:/Users/Lenovo"; # Set this to your actual user folder if not already set
  system("perl ${cmd} > ${outfile} ${warnfile}");
  return($outfile);
}
# Read a file
sub ReadFile
{
  my ($self,$file) = @_;
  my $pwd=cwd();
#warn "ReadFile: pwd=$pwd\n";
#warn "ReadFile: file=$file\n";
  my $text;
  open( FILE, ${file} ) or return "Could not open $file ($!) (ReadFile ${pwd})";
  while( $line = <FILE> ) { $text .= $line; }
  close(FILE);
  return($text);
}
sub readasarray
{
  my ($self,$file) = @_;
  my @lines = ();
  print qq|\nparse file: $file\n|;
  if ( open(FILE, $file) ) 
  {
    while ( my $in = <FILE> )
    { chomp($in); push(@lines,$in);  }
    close(FILE);
  }
  return(@lines);
}
sub CountFile
{
  my ($self,$file) = @_;
  open(IN,$file);
  my @str = <IN>;
  my $cnt = scalar(@str);
  close(IN);
  return($cnt);
}
sub sysfile
{
  my ($self, $pgm, $parms, $user) = @_;
  my $pathname = '/tmp/sysfile:' . $pgm . ':' . $parms;
  my ($sec, $min, $hrs, $day, $month, $year, $wday, $julian) = localtime();
  $month++; $year +=1900;
#warn qq|sysfile: $pathname\n|;
  if ( open(TEMPLATE, ">>$pathname") ) 
  { print TEMPLATE qq|${user}: ${year}-${month}-${day} ${hrs}:${min}\n|; }
  close(TEMPLATE);
#warn qq|sysfile: return\n|;
  return(1);
}
sub gTotal
{
  my ($self,$type) = @_;
  my ($Avg,$Tot,$Cnt) = (0,0,0);
  foreach $_ ( @_ )
  {
# check for number or null (null considered 0)
    if ( $_ =~ /^[0-9\.\-]+$/ || $_ eq '' )
    {
      $Tot += $_;
#     use 'all' in average or only non-zero values?
      if ( $type eq "all" ) { $Cnt++; }
      elsif ( $_ != 0 ) { $Cnt++; }

      if ( $Cnt == 0 ) { $Avg = 0; }
      else { $Avg = $Tot / $Cnt; }
    }
  }
  return($Avg,$Tot);
}
1;
