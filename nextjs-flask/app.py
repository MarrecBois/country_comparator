import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from countriesDict import *
from datetime import datetime
import random as rn

#for key in countryDict:
    #print(key, countryDict[key])

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) 

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        session['GameModeIndex'] = request.form.get('gameModeIndex')
        return redirect('/gameon')
    else:
        return render_template('index.html')

@app.route('/gameon', methods=['POST', 'GET'])
def gameon():
    if request.method == 'POST':    
        if request.form.get("Guess") == "Lower":
            country1Data = countryDict[session['country1']][int(session['GameModeIndex'])]
            country2Data = countryDict[session['country2']][int(session['GameModeIndex'])]
            if country1Data < country2Data:
                return redirect('/gameover')
            else:

                if session['hardMode']:
                   session['GameModeIndex'] = randomIndex = rn.randint(1, 14)

                country1 = session['country2']
                rand2 = rn.randint(0, len(countryList)-1)
                country2 = countryList[rand2]
                while (country2 == country1) or (countryDict[country2][int(session['GameModeIndex'])]) == 'NO':
                    rand2 = rn.randint(0, len(countryList)-1)
                    country2 = countryList[rand2]
                
                while (countryDict[country1][int(session['GameModeIndex'])]) == 'NO': # This code will only be applicable for hard mode
                    rand1 = rn.randint(0, len(countryList)-1)
                    country1 = countryList[rand1]

                session['country1'] = country1
                session['country2'] = country2
                session['score'] += 1
                gameMode = gameModeList[int(session['GameModeIndex'])]
                country1Info = countryDict[country1][int(session['GameModeIndex'])]
                country2Info = countryDict[country2][int(session['GameModeIndex'])]

                if session['Anthem']:
                    country1Info = str(country1Info)[0] + ':' + str(country1Info)[1:]
                    country2Info = str(country2Info)[0] + ':' + str(country2Info)[1:]
                
                elif session['Debt']:
                    country1Info = round(country1Info)
                    country2Info = round(country2Info)
                    newc1Info = str(country1Info)[-3:]
                    newc2Info = str(country2Info)[-3:]

                    for pos in range(1, len(str(country1Info))//3):
                        newc1Info = str(country1Info)[len(country1Info - 3*pos):len(country1Info - 3*pos) + 3] + ',' + newc1Info
                    
                    for pos in range(1, len(str(country2Info))//3):
                        newc2Info = str(country2Info)[len(country2Info - 3*pos):len(country2Info - 3*pos) + 3] + ',' + newc2Info
                    
                    country1Info = newc1Info
                    country2Info = newc2Info


                return render_template('gameon.html', score = session['score'], country1 = country1, country2 = country2, gameMode = gameMode, country1Info=country1Info,country2Info=country2Info)
        else:
            country1Data = countryDict[session['country1']][int(session['GameModeIndex'])]
            country2Data = countryDict[session['country2']][int(session['GameModeIndex'])]
            if country1Data > country2Data:
                return redirect('/gameover')
            else:

                if session['hardMode']:
                   session['GameModeIndex'] = randomIndex = rn.randint(1, 14)

                country1 = session['country2']
                rand2 = rn.randint(0, len(countryList)-1)
                country2 = countryList[rand2]
                while (country2 == country1) or (countryDict[country2][int(session['GameModeIndex'])]) == 'NO':
                    rand2 = rn.randint(0, len(countryList)-1)
                    country2 = countryList[rand2]

                while (countryDict[country1][int(session['GameModeIndex'])]) == 'NO': # This code will only be applicable for hard mode
                    rand1 = rn.randint(0, len(countryList)-1)
                    country1 = countryList[rand1]

                session['country1'] = country1
                session['country2'] = country2
                session['score'] += 1
                gameMode = gameModeList[int(session['GameModeIndex'])]
                country1Info = countryDict[country1][int(session['GameModeIndex'])]
                country2Info = countryDict[country2][int(session['GameModeIndex'])]

                if session['Anthem']:
                    country1Info = str(country1Info)[0] + ':' + str(country1Info)[1:]
                    country2Info = str(country2Info)[0] + ':' + str(country2Info)[1:]
                
                elif session['Debt']:
                    country1Info = round(country1Info)
                    country2Info = round(country2Info)
                    newc1Info = str(country1Info)[-3:]
                    newc2Info = str(country2Info)[-3:]

                    for pos in range(1, len(str(country1Info))//3):
                        newc1Info = str(country1Info)[len(country1Info - 3*pos):len(country1Info - 3*pos) + 3] + ',' + newc1Info
                    
                    for pos in range(1, len(str(country2Info))//3):
                        newc2Info = str(country2Info)[len(country2Info - 3*pos):len(country2Info - 3*pos) + 3] + ',' + newc2Info
                    
                    country1Info = newc1Info
                    country2Info = newc2Info

                return render_template('gameon.html', score = session['score'], country1 = country1, country2 = country2, gameMode = gameMode, country1Info=country1Info,country2Info=country2Info)
    else: 

        session['hardMode'] = False
        session['Anthem'] = False
        session['Debt'] = False
        gameMode = gameModeList[int(session['GameModeIndex'])]
        
        if gameMode == 'Hard Mode':
            session['hardMode'] = True
            randomIndex = rn.randint(1, 14)
            session['GameModeIndex'] = randomIndex = rn.randint(1, 14)
            gameMode = gameModeList[int(session['GameModeIndex'])]
        
        elif gameMode == 'National Anthem Length (Minutes:Seconds)':
            session['Anthem'] = True

        elif gameMode == 'Debt (USD)':
            session['Debt'] = True

        session['score'] = 0
        rand1 = rn.randint(0, len(countryList)-1)
        rand2 = rn.randint(0, len(countryList)-1)
        while rand1 == rand2:
            rand2 = rn.randint(0, len(countryDict))
        country1 = countryList[rand1]
        country2 = countryList[rand2] 
        session['country1'] = country1
        session['country2'] = country2
        country1Info = countryDict[country1][int(session['GameModeIndex'])]
        country2Info = countryDict[country2][int(session['GameModeIndex'])]
        
        while (country1Info == 'NO' or country2Info == 'NO'):
            
            rand1 = rn.randint(0, len(countryList)-1)
            rand2 = rn.randint(0, len(countryList)-1)
            while rand1 == rand2:
                rand2 = rn.randint(0, len(countryDict))
            country1 = countryList[rand1]
            country2 = countryList[rand2] 
            session['country1'] = country1
            session['country2'] = country2
            country1Info = countryDict[country1][int(session['GameModeIndex'])]
            country2Info = countryDict[country2][int(session['GameModeIndex'])]

        if session['Anthem']:
            country1Info = str(country1Info)[0] + ':' + str(country1Info)[1:]
            country2Info = str(country2Info)[0] + ':' + str(country2Info)[1:]

        elif session['Debt']:
            country1Info = round(country1Info)
            country2Info = round(country2Info)
            newc1Info = str(country1Info)[-3:]
            newc2Info = str(country2Info)[-3:]

            for pos in range(1, len(str(country1Info))//3):
                newc1Info = str(country1Info)[len(country1Info - 3*pos):len(country1Info - 3*pos) + 3] + ',' + newc1Info
            
            for pos in range(1, len(str(country2Info))//3):
                newc2Info = str(country2Info)[len(country2Info - 3*pos):len(country2Info - 3*pos) + 3] + ',' + newc2Info
            
            country1Info = newc1Info
            country2Info = newc2Info

        return render_template('gameon.html', score = 0, country1 = country1, country2 = country2, gameMode = gameMode, country1Info=country1Info, country2Info=country2Info) 

@app.route('/gameover', methods=['POST', 'GET'])
def gameover():
    if request.method == 'POST':
        return redirect('/gameon')
    return render_template('gameover.html', score = session['score'])

@app.route('/tutorial', methods=['GET'])
def tutorial():
    return render_template('tutorial.html', score = session['score'])

if __name__ == "__main__":
    app.run(port=8000, debug=True)