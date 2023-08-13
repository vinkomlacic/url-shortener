# URL Shortener
+ [![cov](https://vinkomlacic.github.io/url_shortener/badges/coverage.svg)](https://github.com/vinkomlacic/url_shortener/actions)
+ [![version](https://vinkomlacic.github.io/url_shortener/badges/version.svg)](https://github.com/vinkomlacic/url_shortener/actions)

A simple private URL shortener.

For authenticated users, allows creation and management of shortened URLs. The
shortened URLs are redirected to their original counterparts.

## Usage
To use the online version of the [URL shortener](https://urls.vinkomlacic.com),
you can use the demo account with the following credentials:
 - **username:** demo
 - **password:** Demo123#

The demo account has a limit on the creation of 1000 URLs. Later, you will have
to delete old ones to be able to shorten new URLs. Note that this account can
be used by anyone.

If you'd like a real account, please contact me at 
[vinkomlacic@outlook.com](mailto:vinkomlacic@outlook.com).


## Local development quickstart
For development purposes, there is the `docker-compose.yml` file which allows
easy setup of the PostgreSQL database which is used by the project.

1. Create the virtual environment, activate it and install all required 
packages from `requirements.txt`: `pip install -r config/requirements/local.txt`
2. Create `config/.env` file. See `config/.env.example` for guidance.
3. In the `docker` directory, run `docker-compose up`.
4. Create the `url_shortener` DB in your PostgreSQL server and add it to the 
`DATABASE_URL` environment variable.
5. Run the migrations: `python manage.py migrate`
6. Start the server
 