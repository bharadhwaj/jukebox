# JUKEBOX

Jukebox is a voting based playlist creator, which 

  - Fetches the Youtube URLs from a predefined Slack Channel.
  - Allow users to vote against each album.
  - Plays the songs based on the vote each album received.

### Technology and Tools

**Jukebox** is developed using:

* [Django] - This app is developed by Python Web Framework Django.
* [MySQL] - Used for persistent storage.
* [Materialize] - An awesome UI boilerplate.

### Installation

**Jukebox** is written in Django2.0.

1. Clone the repository at required location.

```sh
$ cd required/path
$ git clone https://github.com/bharadhwaj/jukebox.git # For HTTPs
$ git clone git@github.com:bharadhwaj/jukebox.git # For SSH
```

2. Install the dependencies

```sh
$ cd jukebox/
$ pip install -r requirements.txt
```

3. Configure the Database
 Inside the file `entri/settings.py`, configure the below things,
```python
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<Database Name>',
        'HOST': '<Host>',
        'USER': '<User>',
        'PASSWORD': '<Password>'
    }
}
...
````

4. Configure the Slack Legacy Token
  Obtain **Slack Legacy Token** for a specific slack channel from [here](https://api.slack.com/custom-integrations/legacy-tokens)
After generating the Slack Legacy Token, add it as environment variable `SLACK_TOKEN`,
```sh
$ export SLACK_TOKEN='xoxp-....
```

5. Configure the Channel Name
 Inside `entri/settings.py`, edit the following line to your required channel name,
```py
...
SLACK_CHANNEL = "<Slack-Channel-Name>"
...
```

6. Create the Database Migration 
 From the root directory of the repo, enter,
```sh
$ python manage.py migrate
```
Now the database is setup if you have configured correctly.

7. Run the server.
 ```sh
$ python manage.py runserver 0:8080
```

### Routes Available

Jukebox app has the following views.

| Route | Description |
| ------ | ------ |
| / | Display the playlist of albums that have been added. |
| /vote/ | To vote for any album |
| /result/ | To see the result of the polls |

License
----

MIT


**Free Software, Hell Yeah!**

   [Django]: <https://www.djangoproject.com/>
   [Materialize]: <https://materializecss.com/>
   [MySQL]: <https://www.mysql.com/>
