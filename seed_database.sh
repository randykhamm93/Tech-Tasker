rm db.sqlite3
rm -rf ./techtaskerapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations techtaskerapi
python3 manage.py migrate techtaskerapi
python3 manage.py loaddata users
python3 manage.py loaddata categories
python3 manage.py loaddata work_orders  
python3 manage.py loaddata employees
python3 manage.py loaddata departments  
python3 manage.py loaddata employee_work_orders 
