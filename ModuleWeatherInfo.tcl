###############################################################################
#
# WeatherInfo module implementation
#
###############################################################################


#
# This is the namespace in which all functions and variables below will exist.
# The name must match the configuration variable "NAME" in the
# [ModulePropagationMonitor] section in the configuration file. The name may
# be changed but it must be changed in both places.
#
namespace eval WeatherInfo {

#
# Check if this module is loaded in the current logic core
#
if {![info exists CFG_ID]} {
  return;
}


#
# Extract the module name from the current namespace
#
set module_name [namespace tail [namespace current]];


#
# A convenience function for printing out information prefixed by the
# module name
#
proc printInfo {msg} {
  variable module_name;
  puts "$module_name: $msg";
}

#
# A convenience function for calling an event handler
#
proc processEvent {ev} {
  variable module_name
  ::processEvent "$module_name" "$ev"
}


#
# Executed when this module is being activated
#
proc activateInit {} {
  printInfo "Module activated"
}


#
# Executed when this module is being deactivated.
#
proc deactivateCleanup {} {
  printInfo "Module deactivated"
}


#
# Executed when a DTMF digit (0-9, A-F, *, #) is received
#
proc dtmfDigitReceived {char duration} {
  printInfo "DTMF digit $char received with duration $duration milliseconds";
}


#
# Executed when a DTMF command is received
#
proc dtmfCmdReceived {cmd} {
  #printInfo "DTMF command received: $cmd";

  if {$cmd == "0"} {
    processEvent "play_help"
  } elseif {$cmd == "1"} {
    getNumberOfRecords
  } elseif {$cmd == "2"} {
    playAllWeatherInfos
  } elseif {$cmd == ""} {
    deactivateModule
  } else {
    processEvent "unknown_command $cmd"
  }
}


#
# gibt die Anzahl der Meldungen im /archive-Verzeichnis aus
#
proc getNumberOfRecords {} {
  variable msg_cnt
  variable files
  variable CFG_PLAY_DIR
  variable callsign

  set callsign $Logic::CFG_CALLSIGN
  set files [glob -nocomplain -directory "$CFG_PLAY_DIR/archive/" old-$callsign.*.wav]
  set msg_cnt [llength $files]
  playMsg "we_have"

  if {$msg_cnt == 0} {
    playMsg "none"
    playMsg "new_weatherinfos"
  } elseif {$msg_cnt == 1} {
    playMsg "one"
    playMsg "new_weatherinfo"
  } else {
    playNumber $msg_cnt
    playMsg "new_weatherinfos"
  }
}


#
# give out all Weatherinfos
#
proc playAllWeatherInfos {} {
  variable files
  variable tfile
  variable sortlist
  variable outfile
  variable filearray
  variable CFG_PLAY_DIR
  variable minute
  variable hour
  variable callsign

  set callsign $Logic::CFG_CALLSIGN
  set files [glob -nocomplain -directory "$CFG_PLAY_DIR/archive/" old-$callsign.*.wav]

  if {[llength $files] > 0} {

    # Meldungen in Array packen
    foreach tfiles $files {
      set xtime [file mtime $tfiles]
      set filearray($xtime) $tfiles
    }

    # Array sortieren
    set sortlist [lsort -integer [array names filearray]]

    # und ausgeben
    foreach outfile $sortlist {
      set minute [clock format $outfile -format %M]
      set hour [clock format $outfile -format %H]
      set tfile [file tail $filearray($outfile)]
      set tfile [string map [list ".wav" ""] $tfile]

      playTime $hour $minute
      playSilence 200
      playMsg "/archive/$tfile"
      playSilence 500
    }
  }
}


#
# Executed when a DTMF command is received in idle mode. That is, a command is
# received when this module has not been activated first.
#
proc dtmfCmdReceivedWhenIdle {cmd} {
  printInfo "DTMF command received while idle: $cmd";
}


#
# Executed when the squelch open or close. If it's open is_open is set to 1,
# otherwise it's set to 0.
#
proc squelchOpen {is_open} {
  if {$is_open} {set str "OPEN"} else {set str "CLOSED"};
#  printInfo "The squelch is $str";
}


#
# Executed when all announcement messages has been played.
# Note that this function also may be called even if it wasn't this module
# that initiated the message playing.
#
proc allMsgsWritten {} {
  #printInfo "all_msgs_written called...";
}


#
# Verzeichnis prüfen auf neue Verkehrsmitteilungen
# und die vorhandenen Dateien entsprechen bearbeiten
#
proc check_dir {dir} {
  variable CFG_SPOOL_DIR
  variable CFG_PLAY_DIR
  variable CFG_DELETE_AFTER
  variable CFG_ALERT
  set alert $CFG_ALERT
  set diff [expr "60 * $CFG_DELETE_AFTER"]
  set callsign $Logic::CFG_CALLSIGN

  # bereits veroeffentlichte Dateien in das archive_Verzeichnis verschieben
  set old_file [glob -nocomplain -directory "$CFG_PLAY_DIR/" old-$callsign.*]

  foreach item $old_file {
    set target "$CFG_PLAY_DIR/archive/[file tail $item]"
    file rename -force "$item" "$target"
  }

  # dann checken, ob neue Daten vorhanden sind
  set msg_file [glob -nocomplain -directory "$CFG_SPOOL_DIR/" $callsign.*.wav]

  if {[llength $msg_file] > 0} {

    if {$alert == 1} { 
      playAlertSound;
      playSilence 1000;
    }

    foreach message $msg_file {
       printInfo "$callsign - $message"
       playSilence 500

       set mfile [file tail "$message"]
       set mfile [string map [list ".wav" ""] $mfile]
       file rename -force "$message" "$CFG_PLAY_DIR/old-$mfile.wav"
       file rename -force "$CFG_SPOOL_DIR/$mfile.info" "$CFG_PLAY_DIR/old-$mfile.info"
       playMsg "old-$mfile"
    }
  }

  # alte Files loeschen
  set old_file [glob -nocomplain -directory "$CFG_PLAY_DIR/archive/" old-$callsign.*]
  set now [clock seconds]
  foreach item $old_file {
    set itime [file mtime $item]
    set d [expr "$now - $itime"]
    if {$d > $diff} {
      printInfo "$itime, loesche $item"
      file delete "$item"
    }
  }
}


#
# executes the function weatherinfo
#
proc check_for_alerts {} {
  check_dir weatherinfo
}


if {![file exists $CFG_SPOOL_DIR/archive]} {
  file mkdir $CFG_SPOOL_DIR/archive
}

append func $module_name "::check_for_alerts";
Logic::addTimerTickSubscriber $func;


# end of namespace
}


#
# This file has not been truncated
#
