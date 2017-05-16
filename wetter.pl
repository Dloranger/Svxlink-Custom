#!/usr/bin/perl
#
# kleines Programm zum Auslesen von Wetterdaten von aprs.fi
#
# Adi Bier / DL1HRC
#
# V0.03 liest Temperatur von aprs.fi
#

use LWP::UserAgent;

$call = "CW0134";
$apikey = "hier den aprs.fi-Api key eintragen";
$owninfo = "SvxLink - no website";

#####################################################################
$ua = LWP::UserAgent->new();
$ua->timeout(10);
$ua->agent($owninfo);

$ret = $ua->get("https://api.aprs.fi/api/get?name=$call&what=wx&apikey=$apikey&format=xml");

if ($ret->is_success) {
  $r = $ret->decoded_content;
  $r =~ m/<temp>(-?\d{1,}\.\d)<\/temp>/;
  $temp = $1;
} else {
  print "Fehler bei Abfrage der Webseite\n";
}

# eine tcl-Datei für SvXLink-Ausgabe erstellen.
# Diese tcl-Datei wird dann z.B. bei der stündlichen Ansage 
# gesourced
#
# -> Eintrag in die Prozedur send_log_ident {hour minute} nach dem 
#    locale-Konzept einfügen:
#
# source "/tmp/wx.tcl";
#
open(WX,">/tmp/wx.tcl");
  print WX "playMsg \"MetarInfo\" \"temperature\";\n";
  print WX "playNumber $temp;\n";
  print WX "playMsg \"MetarInfo\" \"degrees\";\n";
close(WX);
