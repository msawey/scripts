docker cp ~/scripts/populate_data.py optic:/home/ubuntu/scripts/populate_data.py && docker cp ~/scripts/actor.json optic:/home/ubuntu/scripts/actor.json && docker exec -it optic /bin/bash -c 'cd /home/ubuntu; source venv/bin/activate; source /environment.sh; ts/manage.py shell < scripts/populate_data.py'
