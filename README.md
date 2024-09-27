# Bitpin
Assessment API service for <a href="https://bitpin.ir/">Bitpin</a>

## Development

### Prerequisites
- Pycharm (IDE)
- At least 6GB of RAM
- 2 Core CPU

### Getting started

- Copy & update environment variables from `.env.sample`
  ```shell
  cp .env.sample .env
   ```
- Apply migrations
  ```shell
  python manage.py migrate
  ```
- Happy coding!!!

### Advanced:
- Install dependencies for Python 3.12
  ```shell
  pip install -r requirements.txt
  ```
- Make new migrations
  ```shell
  python manage.py makemigrations
  ```
- Run tests with full detail for api
  ```shell
  python manage.py test -v2
  ```


## Spam detection scenario [description]
To find scores registered as spam. We divided the averages recorded for _(one hour into 6 parts: __*it's variable and you can change it easily__)_.

If the average scores change by more than 20% in this 10-minute period, we consider all the votes in that hour as spam. (not only bad score)

We do not consider the number of scores and the increase in the number of scores as spam because these votes may be real. We only consider sudden changes in the average as spam.
