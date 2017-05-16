###############################################################################
#
# WeatherInformation module event handlers
#
###############################################################################

#
# This is the namespace in which all functions and variables below will exist.
# The name must match the configuration variable "NAME" in the
# [ModuleTcl] section in the configuration file. The name may be changed
# but it must be changed in both places.
#
namespace eval WeatherInfo {

#
# Check if this module is loaded in the current logic core
#
if {![info exists CFG_ID]} {
  return
}


#
# Extract the module name from the current namespace
#
set module_name [namespace tail [namespace current]]


#
# An "overloaded" playMsg that eliminates the need to write the module name
# as the first argument.
#
#   msg - The message to play
#
proc playMsg {msg} {
  variable module_name
  printInfo "Module name: $module_name $msg"
  ::playMsg $module_name $msg
}



#
# A convenience function for printing out information prefixed by the
# module name
#
proc printInfo {msg} {
  variable module_name
}


#
# Executed when this module is being activated
#
proc activating_module {} {
  variable module_name
  Module::activating_module $module_name
}


#
# Executed when this module is being deactivated.
#
proc deactivating_module {} {
  variable module_name;
  Module::deactivating_module $module_name;
}


#
# Executed when the inactivity timeout for this module has expired.
#
proc timeout {} {
  variable module_name;
  Module::timeout $module_name;
}


#
# Executed when playing of the help message for this module has been requested.
#
proc play_help {} {
  variable module_name;
  Module::play_help $module_name;
}


#
# Executed when the state of this module should be reported on the radio
# channel. The rules for when this function is called are:
#
# When a module is active:
# * At manual identification the status_report function for the active module is
#   called.
# * At periodic identification no status_report function is called.
#
# When no module is active:
# * At both manual and periodic (long variant) identification the status_report
#   function is called for all modules.
#
proc status_report {} {
  #printInfo "status_report called...";
}


#
# Called when an illegal command has been entered
#
#   cmd - The received command
#
proc unknown_command {cmd} {
  playNumber $cmd
  playMsg "unknown_command"
}


proc give_out {afile} {
  playMsg $afile
}

#
# Play an alert sound to get the users attention
#
proc playAlertSound {} {
  for {set i 0} {$i < 3} {set i [expr $i + 1]} {
    playTone 440 500 100
    playTone 880 500 100
    playTone 440 500 100
    playTone 880 500 100
    playSilence 600
  }
  playSilence 1000
}

#
# Ausgabe der Anzahl der aktuellen Wettermeldungen
#
proc getNumber {} {
  variable CFG_PLAY_DIR
  variable callsign
  variable msg_cnt
  variable files
  set callsign $Logic::CFG_CALLSIGN
  set files [glob -nocomplain -directory "$CFG_PLAY_DIR/archive/" old-$callsign.*.wav]
  set msg_cnt [llength $files]
  return $msg_cnt
}


# end of namespace
}


#
# This file has not been truncated
#