mkdir ~/.virtualenv

vim ~/.bashrc
# Press shift+I to add the next two lines to your .bash_profile
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source ~/.bashrc

python3 -m venv ~/.virtualenv/mymdb
source ~/.virtualenv/mymdb/bin/activate
[ or workon mymdb]

pip install --upgrade pip

python3 -m pip install -r requirements.dev.txt

sudo -u postgres psql
create databse $dbname;
create user $dbuser with password '$password'
alter role $dbuser set client_encoding to 'utf8';
ALTER ROLE $dbuser SET default_transaction_isolation TO 'read committed';
alter role $dbuser set timezone to 'UTC';
grant all privileges on database $dbname to $dbuser;
