cd C:\GIT\avitech\package
python setup.py sdist
pip install --upgrade --force avitech --no-index --find-links C:\GIT\avitech\package\dist
# На сервере:
pip3 install --upgrade --force /home/artem/avitech/package

pip3 install --upgrade --force git+https://github.com/nechart/avitech/tree/master