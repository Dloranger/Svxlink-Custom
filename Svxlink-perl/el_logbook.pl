#!/usr/bin/perl

use POSIX qw(strftime);

$svxlink_log = "/var/log/svxlink";
$svxlink_lb  = "/tmp/svxlink_lb";

#####################################################################################
$qso = 0;
$info = 0;

open(IN, "<$svxlink_log") || die "Can not open $svxlink_log";
 @lines = <IN>;
close(IN);

$date = strftime "%d%m%Y", localtime;

open(OUT, ">$svxlink_lb-$date") || die "Can not open $svxlink_lb-$date";

# print the lb-header
print OUT "Callsign\tbegin\tend\tEchoLink-ID\tremarks\n";

foreach $l (@lines) {
  if ($info == 1 && $l =~ m/(\d\d.\d\d.\d\d\d\d \d\d:\d\d:\d\d):(.*)/) {
    $info = 0;
    $inf_message = $2;
  }
  if ($l =~ m/(\d\d.\d\d.\d\d\d\d \d\d:\d\d:\d\d):\s([A-Z0-9-]{3,8}):\s(.*)ID\sis\s(\d{4,7})/) {
    $con_time = $1;
    $con_call = $2;
    $el_ID    = $4;
    $qso = 1;
  }
  if ($qso == 1 && $l =~ m/message received from/) {
    $info = 1;
  }
  if ($l =~ m/(\d\d.\d\d.\d\d\d\d \d\d:\d\d:\d\d):\s([A-Z0-9-]{3,8}):\s(.*)to\sDISCONNECTED/) {
    $disc_time = $1;
    $disc_call = $2;
    $qso = 0;
    print OUT "$disc_call\t$con_time\t$disc_time\t$el_ID\t$inf_message\n";
  }
}
close OUT;
