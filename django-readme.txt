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
CREATE DATABASE $dbname;
CREATE USER $dbuser WITH PASSWORD '$password'
ALTER ROLE $dbuser SET client_encoding TO 'utf8';
ALTER ROLE $dbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE $dbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $dbname TO $dbuser;
ALTER USER $dbuser CREATEDB;


ERRORS:
P72
In render_to_response of CreateVote
    movie_id = self.kwargs['movie_id']
    # no context['object'] yet
P74
In render_to_response of UpdateVote
    movie_id = context['object'].movie.id
    # conext['object'] is a Vote object
    # not a Movie object
