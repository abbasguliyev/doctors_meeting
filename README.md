# doctors_meeting_backend
Doctors Meeting in Turkey

## Install
https://github.com/Vesnat-Teknoloji/doctors_meeting_backend.git
## Configuration
create .env file inside src folder, then copy and paste the contents from the .env.example file. \
run python manage.py add_default_data command for add default data to database \
run python manage.py cities_light command for add city and country data to database
## Run with Docker
docker-compose build \
docker-compose run --rm web python3 manage.py migrate \
docker-compose run --rm web python3 manage.py createsuperuser \
docker-compose up

