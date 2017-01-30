from setuptools import setup

setup(
	name = 'application_name',
	packages = ['application_name'],
	include_package_data = True,
	install_requires = [flask, psycopg2] # TODO: Find out what to do between venv and setuptools or if theyre different things.
)
