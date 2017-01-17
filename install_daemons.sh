#! /bin/bash
export PATH=$1/bin:$PATH

# install_daemons.sh

echo 'Installing Daemon for OSNAP'
echo '---------------------------'

echo 'Downloading PostgreSQL'
git clone -b REL9_5_STABLE https://github.com/postgres/postgres.git postgres
echo '...COMPLETE'

echo 'Installing PostgreSQL'
cd postgres
./configure --prefix=$1
make
make install
echo '...COMPLETE'

cd ..

echo 'Installing Apache'
curl http://mirrors.koehn.com/apache//httpd/httpd-2.4.25.tar.gz -o httpd-2.4.25.tar.gz
tar -xvfz httpd-2.4.25.tar.gz
rm httpd-2.4.25.tar httpd-2.4.25.tar.gz
cd $1/httpd-2.4.25
./configure --prefix=$1
make
make install
sed -i '/Listen 80/c\Listen 8080' $1/conf/httpd.conf
echo '...COMPLETE AND LIVE'

cd ..

