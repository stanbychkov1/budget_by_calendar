# budget_by_calendar

Hi! My name is Stan and it's my first full-stack app. It works with caldev Calendar.
If you'd like to control your finance, then welcome.

This app can be helpful for people, who works for themselves.
Caldev events must be created in one of the calendar, that must be used only for this purpose, you have in your Iphone,
Mac or another caldev apps. Caldev Events must include two required variables <client_name>/<amount> in summary.
Example:
Maria/500
Julia/350

Requirements:
1. Docker ([install](https://docs.docker.com/engine/install/))
2. Docker-compose ([install](https://docs.docker.com/compose/install/))

Launch app:
At first clone repo with an app:
```bash
git clone git@github.com:stanbychkov/budget_by_calendar.git
````
Secondly create .env file with variables and fill all rows with <>:
````
URL='https://caldav.icloud.com'
USER_NAME='<username>@icloud.com'
PASSWORD='<your_password>'
CAL_NAME='<calendar_name>'
DJANGO_SECRET_KEY='<secret_key>'
DJANGO_DEBUG=false
DOMAIN_NAME=<domain_name>
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=<postgres_username>
POSTGRES_PASSWORD=<postgres_password>
DJANGO_DATABASE_HOST=db
DJANGO_DATABASE_PORT=5432
````
Thirdly that you should use docker-compose command in repo fileroot:
```bash
docker-compose up
````
After that all you can sign up on your domain and log in, go to <domain_name>/calendar_date, upload your calendar events to database!
Then go to <domain_name>/payment and create payments for unpaid events, that had been paid.

Watch for updates!