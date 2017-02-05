#! /bin/bash
export PATH=$1/bin:$PATH

# install_daemons.sh

printf 'Installing Daemon for OSNAP\n'
printf '---------------------------\n'

printf 'Downloading PostgreSQL\n'
git clone -b REL9_5_STABLE https://github.com/postgres/postgres.git postgres
printf '...COMPLETE\n\n'

printf 'Installing PostgreSQL\n'
cd postgres
./configure --prefix=$1
make
make install
printf '...COMPLETE\n\n'

cd ..

printf 'Installing Apache\n'
curl http://download.nextag.com/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2 
cd httpd-2.4.25
./configure --prefix=$1
make
make install
sed -i '/Listen 80/c\Listen 8080' $1/conf/httpd.conf
printf '...COMPLETE AND LIVE\n\n'

cd ..
