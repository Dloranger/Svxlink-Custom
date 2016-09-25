#!/bin/bash
txt=this is my text

echo "Capture Image "
sudo raspistill -w 800 -h 600 -o /home/pi/SSTV/sstv.jpg
echo "Add custom text to img "
sudo convert /home/pi/SSTV/sstv.jpg -gravity south -stroke "#000C" -strokewidth 2 -annotate 0 "$txt" -stroke none -fill white -annotate 0 "$txt" /home/pi/SSTV/sstv.jpg
echo " compilation sstv "
sudo python /home/pi/PySSTV-0.2.7/pysstv --vox /home/pi/SSTV/sstv.jpg /home/pi/SSTV/sstv.wav
echo " play the img "
play /home/pi/SSTV/sstv.wav




