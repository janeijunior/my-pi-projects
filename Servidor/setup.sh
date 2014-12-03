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

dbPass=$(grep "SenhaBanco" /home/pi/HousePi/bin/Config.ini);dbPass=${dbPass#SenhaBanco=}
dbPass=${dbPass//[[:space:]]/}

echo "Instalando MySQL..."
export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $dbPass"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $dbPass"
sudo apt-get -q -y install mysql-server python-mysqldb

echo "Instalando phpMyAdmin..."
export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
sudo debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password $dbPass"
sudo debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password $dbPass"
sudo debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password $dbPass"
sudo debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2"
sudo apt-get -q -y install phpmyadmin

echo "Instalando FTP.." 
sudo apt-get -y install vsftpd 
sudo cp /home/pi/HousePi/bin/vsftpd.conf /etc/
sudo /etc/init.d/vsftpd restart

echo "Instalando mjpg-streamer..."
sudo apt-get -y install libv41-0

echo "Instalando MPlayer..."
sudo apt-get -y install mplayer mplayer-gui alsa-base alsa-utils pulseaudio mpg123

echo "Configurando som..."
sed -i 's/#hdmi_drive=2/hdmi_drive=2/g' /boot/config.txt

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
sed -i 's/BLANK_TIME=30/BLANK_TIME=0/g' /etc/kbd/config
sed -i 's/POWERDOWN_TIME=15/POWERDOWN_TIME=0/g' /etc/kbd/config
sed -i 's/POWERDOWN_TIME=30/POWERDOWN_TIME=0/g' /etc/kbd/config
sudo /etc/init.d/kbd restart

echo "Configurando login automatico..."
sed -i "s@1:2345:respawn:/sbin/getty --noclear 38400 tty1@#1:2345:respawn:/sbin/getty --noclear 38400 tty1@g" /etc/inittab
sed -i '\@1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1@d' /etc/inittab
sed -i "/--noclear 38400 tty1/a1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1" /etc/inittab

echo "Configurando inicio automatico..."
sed -i '\@sudo python /home/pi/HousePi/bin/Servidor.pyc@d' /etc/init.d/rc.local
sed -i "/esac/a#sudo python /home/pi/HousePi/bin/Servidor.pyc\nnohup sudo python /home/pi/HousePi/bin/Servidor.pyc& </dev/null >/dev/null 2>&1 &" /etc/init.d/rc.local

echo "Criando banco de dados..."
mysql -u root -h localhost --password=$dbPass -Bse "DROP DATABASE IF EXISTS HousePi"
mysql -u root -h localhost --password=$dbPass -Bse "CREATE DATABASE HousePi"
mysql -u root -h localhost --password=$dbPass HousePi < /home/pi/HousePi/bin/ScriptBanco.sql
