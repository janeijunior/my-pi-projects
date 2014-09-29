#!/bin/bash

echo "Instalando atualizacoes..."
sudo apt-get -y update
sudo apt-get -y upgrade

echo "Configurando permissoes..."
sudo chmod 777 /home/pi/HousePi
cd /home/pi/HousePi
sudo chmod 777 Imagens
sudo chmod 777 Musicas
sudo chmod 777 Videos
sudo chmod 777 bin
cd bin 
sudo chmod 777 mjpg-streamer
sudo chmod 777 Adafruit_Python_DHT
sudo chmod 777 pexpect-2.3
cd /home/pi/HousePi

echo "Instalando bibliotecas GPIO..."
sudo apt-get -y install python-dev
sudo apt-get -y install python-rpi.gpio
sed -i '/i2c-bcm2708/d' /etc/modules
sed -i '/i2c-dev/d' /etc/modules
sed -i "/snd-bcm2835/ai2c-bcm2708\ni2c-dev" /etc/modules
sudo apt-get -y install python-smbus
sudo apt-get -y install i2c-tools
sed -i 's/blacklist spi-bcm2708/#blacklist spi-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf
sed -i 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf

echo "Instalando MySQL..."
sudo apt-get -y install mysql-server python-mysqldb

echo "Instalando phpMyAdmin..."
sudo apt-get -y install phpmyadmin

echo "Instalando FTP.." 
sudo cp /home/pi/HousePi/bin/vsftpd.conf /etc/
sudo apt-get -y install vsftpd 
sudo /etc/init.d/vsftpd restart

echo "Instalando mjpg-streamer..."
sudo apt-get -y install libv41-0

echo "Instalando MPlayer..."
sudo apt-get -y install mplayer

echo "Instalando OmxPlayer..."
sudo apt-get -y install omxplayer

echo "Instalando fswebcam..."
sudo apt-get -y install fswebcam

echo "Instalando pexpect-2.3..."
cd /home/pi/HousePi/bin/pexpect-2.3
sudo python ./setup.py install
cd /home/pi/HousePi

echo "Instalando DHT driver..."
sudo apt-get install build-essential python-dev
cd /home/pi/HousePi/bin/Adafruit_Python_DHT
sudo python ./setup.py install
cd /home/pi/HousePi

echo "Configurando tempo do monitor..."
sed -i 's/BLANK_TIME=30/BLANK_TIME=0/g' /etc/inittab
sed -i 's/POWERDOWN_TIME=15/POWERDOWN_TIME=0/g' /etc/inittab
sudo /etc/init.d/kbd restart

echo "Configurando login automatico..."
sed -i "s@1:2345:respawn:/sbin/getty --noclear 38400 tty1@#1:2345:respawn:/sbin/getty --noclear 38400 tty1@g" /etc/inittab
sed -i '\@1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1@d' /etc/inittab
sed -i "/--noclear 38400 tty1/a1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1" /etc/inittab

echo "Configurando inicio automatico..."
sed -i '\@/opt/vc/bin/tvservice -o@d' /etc/init.d/rc.local
sed -i '\@/opt/vc/bin/tvservice -p@d' /etc/init.d/rc.local
sed -i '\@sudo python /home/pi/HousePi/bin/Servidor.pyc@d' /etc/init.d/rc.local
sed -i "/esac/a/opt/vc/bin/tvservice -o\n/opt/vc/bin/tvservice -p\nsudo python /home/pi/HousePi/bin/Servidor.pyc\n#nohup sudo python /home/pi/HousePi/bin/Servidor.pyc& </dev/null >/dev/null 2>&1 &" /etc/init.d/rc.local
