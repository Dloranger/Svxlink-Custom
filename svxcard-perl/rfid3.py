# source code on https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100
import sys

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q$

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: '$

fp = open('/dev/hidraw1', 'rb')


ss = ""
shift = False

done = False
while true:
   while not done:

      ## Get the character from the HID
      buffer = fp.read(8)
      for c in buffer:
         if ord(c) > 0:

            ##  40 is carriage return which signifies
            ##  we are done looking for characters
            if int(ord(c)) == 40:
               done = True
               break;

            ##  If we are shifted then we have to 
            ##  use the hid2 characters.
            if shift:

               ## If it is a '2' then it is the shift key
               if int(ord(c)) == 2 :
                  shift = True

               ## if not a 2 then lookup the mapping
               else:
                  ss += hid2[ int(ord(c)) ]
                  shift = False

            ##  If we are not shifted then use
            ##  the hid characters

            else:

               ## If it is a '2' then it is the shift key
               if int(ord(c)) == 2 :
                  shift = True

               ## if not a 2 then lookup the mapping
               else:
                  ss += hid[ int(ord(c)) ]
   print ss

