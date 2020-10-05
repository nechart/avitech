cd C:\GIT\avitech\package
python setup.py sdist
pip install --upgrade --force avitech --no-index --find-links C:\GIT\avitech\package\dist
# На сервере:
pip3 install --upgrade --force /home/artem/avitech/package

#pip3 install --upgrade --force git+https://github.com/nechart/avitech/tree/master
pip3 install -e git+https://github.com/nechart/avitech#egg=version_subpkg&subdirectory=package # install a python package from a repo subdirectory


# To server
# todo: https://stackoverflow.com/questions/13566200/how-can-i-install-from-a-git-subdirectory-with-pip
git clone https://github.com/nechart/avitech
cd avitech
pip3 install --upgrade --force ./package

# Update:
cd avitech
git pull https://github.com/nechart/avitech