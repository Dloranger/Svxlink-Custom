sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/smeter.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/svxstatus.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/screen.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/test-temperature.py' | awk '{print $2}')
sudo kill $(ps aux | grep 'python /usr/share/svxlink/events.d/local/SVXCard/door.py' | awk '{print $2}')

sleep 1

sudo pkill nc
sudo service svxlink stop
sudo python /usr/share/svxlink/events.d/local/SVXCard/smeter.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/svxstatus.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/screen.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/test-temperature.py > /dev/null &
sudo python /usr/share/svxlink/events.d/local/SVXCard/door.py > /dev/null &

sleep 1

sudo nc -lk 10000 | sudo service svxlink start

