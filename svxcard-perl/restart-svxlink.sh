sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/smeter.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/svxstatus.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/screen.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/test-temperature.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/door.py' | awk '{print $2}')

#ps -ef | grep 'svxlink --logfile=/var/log/svxlink' | awk '{print $2}' | sudo xargs kill -9

#Force PTT TX and LINK to down
sudo echo '0'>  /sys/class/gpio/gpio16/value
sudo echo '0'>  /sys/class/gpio/gpio17/value

#ps -ef | grep 'smeter.py' | awk '{print $2}' | sudo xargs kill -9
#ps -ef | grep 'test-temperature.py' | awk '{print $2}' | sudo xargs kill -9
#ps -ef | grep 'screen.py' | awk '{print $2}' | sudo xargs kill -9
#ps -ef | grep 'svxstatus.py' | awk '{print $2}' | sudo xargs kill -9

sleep 1
#sudo kill -9 $(pidof nc) &
#sudo kill -9 $(pidof svxlink) &
sudo pkill nc
sudo pkill svxlink
sudo python /usr/share/svxlink/events.d/local/SVXCard/smeter.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/svxstatus.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/screen.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/test-temperature.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/door.py > /dev/null &

sleep 1

#sudo nc -lk 10000 | sudo svxlink  &> ./svx.log
#sudo nc -lk 10000 | sudo bash /usr/share/svxlink/events.d/local/SVXCard/svxlaunch.sh >> ./svx.log
sudo nc -lk 10000 | sudo svxlink >> /var/log/svxlink
#sudo nc -l 10000 | sudo svxlink |  logger -f /var/log/svxlink
#nc -lk 10000 | sudo svxlink 2>&1 | sed "s|^|$('date') :: |"  &> ./svx.log
#nc -lk 10000 | sudo svxlink 2>&1 | sed "s|^|$('date') :: |"  > ./svx.log
#sudo nc -lk 10000 2>&1 | sudo svxlink 2>&1 | sed "s|^|$('date') :: |" > ./svx.log
