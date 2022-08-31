# rasa chatbot project

ongoing rasa chatbot using docker, rasa, nginx, django and postgres.

for the development version, run the following command:

```
docker-compose up --build
```

for the production version (which includes nginx), run the following command:

```
docker-compose -f docker-compose.prod.yml up --build
```

you can access the bot by going to the following address:

<a href="http://localhost:9000/bot/index">http://localhost:9000/bot/index</a>