# vkprofi

Proforintation bot for Vk, working on machine learning algorithms.

#### Bot.

The bot runs on the vk_api library for Python 3.7. Interaction with the user takes place 
by means of Calback Api. Information about all new messages is sent to htpps application
on heroku's server and then forwarded via http to my Amazon server. This is handled by a
web-fraemwork Flask. The database is this sqllight, it stores information about the user, his current question
and the response data. Below is the user class in the database (peewee library). The main file is app.py


```angular2
db = SqliteDatabase('db.sqlite3')

class Subs(Model):
    vk_id=IntegerField()
    name = TextField()
    qnow = IntegerField()
    bals = TextField(null=True)
    result = BooleanField(null=True)

    class Meta:
        database = db
        db_table='Subs'
``` 

#### Ml часть.
The answers of more than 400 IT professionals were used to train machine learning models. In addition to taking the test, they also indicate their occupation; the bot is based on the theory that when people choose a narrow direction in IT, they are guided by their preferences, based on their character traits. I use multiclass linear regression and normalize the output. Thanks to this, professions are given out in roughly equal numbers. The profession is now defined in 2 steps - industry selection and specialization (it's already in the CatBoostClassifier decision trees). Also, I dissolved the information and profession and links to courses that are sent after the test. To solve problem with slow speed I uploaded everything to fast Amazon server and made asynchronous unloading of photos (response ~1s).
Now the bot is connected to the group https://vk.com/vkproorintation , the bot has 15 professions. 

Below is the code that sends the data to the training.

```
from sklearn.multioutput import MultiOutputRegressor
from sklearn.datasets import make_regression
from sklearn.linear_model import *

lasso = LinearRegression()
model = MultiOutputRegressor(lasso)
model.fit(x_train,y_train)
```
