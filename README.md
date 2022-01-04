# ComputerSecurity-backend

### Installation Guide


	MySQL environment
		1. Create new schema with the following name: 'communication_ltd'

	Python environment:
		1. run on terminal: pip install -r requirements.txt
		2. in the root project dir, create new file -> 'config.env', then insert the following parameters:
			SECRET_KEY = ''
			MYSQL_USER = *need to fill*
			MYSQL_PASS = *need to fill*
		3. run on terminal: python manage.py makemigrations
		4. run on terminal: python manage.py migrate
		5. run on terminal: python manage.py runserver