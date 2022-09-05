<p align="center"><img src="./images/bot.png" width="10%"></p>
<h1 align="center">Financial Helper Bot 💬</h1>
<p align="center">Financial Helper Bot which can create bank accounts,
 deposit and withdraw money, check the accounts balance, answer FAQ questions and chitchat with users.</p>
<p align="center">
  <img src="https://img.shields.io/pypi/pyversions/rasa">
  <img src="https://img.shields.io/badge/rasa-3.2.2-yellowgreen">
</p>

<p align="center">
    <img src="https://img.shields.io/github/repo-size/achrafaourik/chatbot_rasa">
</p>

 ## 🛠 Features
- [x] Create bank accounts (**Savings** and **Credit**)
- [x] Check the bank accounts balance
- [x] Make a transaction (**Deposit** and **Withdrawal**)
- [x] Answer FAQ questions
- [x] Chitchat with users


ongoing rasa chatbot using docker, rasa, nginx, django and postgres.

for the development version, run the following command:

```
docker-compose up --build
```

for the production version (which includes nginx), run the following command:

```
docker-compose -f docker-compose.prod.yml up --build
```

you can access the bot by going to the following address: http://localhost:9000/bot/index
