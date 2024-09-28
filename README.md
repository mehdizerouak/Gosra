# Gosra

**Gosra** is a real-time chat application built using **Django** and **Django Channels**, with **Redis** as a message broker. It supports both **private messaging** and **public chat rooms**. The project was created to explore and learn about real-time communication in Django.

### Prerequisites
1. **Python**
2. **Django**
3. **Django-channels**
4. **Redis** installed and running on your local machine on the port: 6379

### After cloning the repo

Cd to the folder and install the dependencies 
```
  cd Gosra
  pip install -r requirements.txt
```

### If you don't want to use redis you can use in-Memory Channel Layer in development
Update settings.py and change channel layers conf
```python

  # CHANNEL_LAYERS = {
  # "default": {
  #      "BACKEND": "channels_redis.core.RedisChannelLayer",
  #      "CONFIG": {
  #          "hosts": [("localhost", 6379)],
  #      },
  #  },
  #}
  # COMMENT THIS OUT IN settings.py and add the code below this 

  CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

```

Then run the server
```
  python manage.py runserver
```
it will run on http://http://127.0.0.1:8000/
