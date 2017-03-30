# LOST Inventory Tracker

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This is an inventory tracking Flask web application utilizing a Postgres database without an ORM. You can create users with specific roles, create facilities, create assets, dispose of assets, move assets around, and get a report detailing each asset's location.


## Table of Contents

- [Resources Used](#resources-used)
- [Install](#install)
- [Contents](#contents)
- [Contribute](#contribute)
- [License](#license)


## Resources Used

https://www.cs.uoregon.edu/Classes/17W/cis322/

<i>Web Development with Flask</i> - Miguel Grinberg


## Install

This project uses [Flask](http://flask.pocoo.org/) and [Postgres](https://www.postgresql.org/).

To install, you must have [Virtual Environments](https://pypi.python.org/pypi/virtualenv) installed.

1. Clone repository.
2. Open terminal at top level of repository.
3. Create and activate your virtual environment.
4. `$ pip install -r requirements.txt`
5. Create a local postgres database instance.
6. `$ chmod u+x preflight.sh`
7. `$ ./preflight.sh <db_name>`
8. `$ python3 run.py`


## Contents
```
├── Procfile
├── README.md
├── app
│   ├── README.md
│   ├── __init__.py
│   ├── api.py
│   ├── helpers.py
│   ├── static
│   ├── templates
│   └── views
├── config.py
├── exports
│   ├── README.md
│   ├── assets.csv
│   ├── export_data.sh
│   ├── facilities.csv
│   ├── migrations.py
│   ├── transfers.csv
│   └── users.csv
├── imports
│   ├── data
│   └── import.py
├── preflight.sh
├── requirements.txt
├── run.py
├── runtime.txt
└── sql
    └── create_tables.sql
```  


## Contribute

I don't have any plans to continue this project as it was exploratory in nature.


## License

[MIT](LICENSE) © Kyle Holmberg