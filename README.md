# estopa-partes


### Instalation


#### Install Connection Driver

As we are using MySQL database, our guide for client driver instalation is [here] (https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-installation.html).


Install Database Driver Manager
```bash
apt-get install odbcinst
```


Install odbc driver from bynary tarball. First we download the [ODBC driver](https://dev.mysql.com/downloads/connector/odbc/)


```bash
tar xvf mysql-connector-odbc-8.0.27-i686-pc-linux.tar
cp bin/* /usr/local/bin
cp -rf lib/* /usr/local/lib
```


Register the driver 

```bash
# Registers the Unicode driver:
myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so"

# Registers the ANSI driver 
myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so"
```


Or register manually editing `/etc/odbcinst.ini` 

```ini
[ODBC Driver MySQL]
Description=MySQL ODBC Driver
Driver=/usr/local/lib/libmyodbc8a.so
UsageCount=1

```


#### Install Python libraries

Create virtual enviorement & install dependencies
```bash
virtualenv -p python3 venv

. venv/bin/activate # Activate enviorement

pip install -r requirements.txt
```

Then run the main script

```bash
python main.py
```




