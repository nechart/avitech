cd C:\GIT\avitech\package
python setup.py sdist
pip uninstall avitech
pip install --upgrade --force avitech --no-index --find-links --no-cache-dir C:\GIT\avitech
pip install --upgrade --force avitech --no-index --find-links --no-cache-dir C:\GIT\avitech\package
# На сервере:
pip3 install --upgrade --force /home/artem/avitech/package

#pip3 install --upgrade --force git+https://github.com/nechart/avitech/tree/master
pip3 install -e git+https://github.com/nechart/avitech#egg=version_subpkg&subdirectory=package # install a python package from a repo subdirectory


# To server
# todo: https://stackoverflow.com/questions/13566200/how-can-i-install-from-a-git-subdirectory-with-pip
rm -rf avitech
git clone https://github.com/nechart/avitech
cd avitech
pip3 install --upgrade --force ./package

# Update:
cd avitech
git pull https://github.com/nechart/avitech

# Postgres
version: linux 9.2 win 9.6 (5432)
https://itproffi.ru/ustanovka-postgresql-na-centos-7/
https://khashtamov.com/ru/postgresql-python-psycopg2/
postgres
pass: nartPos_80
create user jupyter with password 'jupMaxim80';
jupyter
jupMaxim80
database:  labdb

