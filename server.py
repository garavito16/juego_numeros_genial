
from random import randint
from flask import Flask, redirect, render_template, request,session

app = Flask(__name__)
app.secret_key = 'para guardar numero random'

@app.route('/')
def iniciar():
    if not('number_random' in session):
        session["number_random"] = randint(1,100)
        session["contador"] = 0
        session["game_over"] = 0
        session["winner"] = 0
        session["register"] = 0
        
    if not('message' in session):
        session["color"] = "red"
    
    print("el numero es : "+str(session["number_random"]))
    print("el contador es "+str(session["contador"]))
    return render_template("index.html")

@app.route('/register',methods=["POST"])
def register():
    winner = {}
    input_name = request.form["input_name"]
    if not('list_winners' in session):
        session["list_winners"] = []
    winner["winner"] = input_name
    winner["intents"] = session["contador"]
    session["list_winners"].append(winner);
    session["register"] = 1
    print(session["list_winners"])
    return redirect('/')

@app.route('/view_list',methods=["GET"])
def view_list():
    return redirect('/view_page')

@app.route('/view_page')
def view_page():
    return render_template("list_winners.html")


@app.route('/return',methods=["GET"])
def function_return():
    return redirect('/')

@app.route('/guess',methods=["POST"])
def guess():
    if session["game_over"] == 0:
        if session["contador"] < 5:
            num = int(request.form["input_guess"])
            num_random = session["number_random"]
            color = "red"
            texto = ""
            if(num > num_random):
                texto ="Too High!"
            elif (num < num_random):
                texto="Too Low!"
            else:
                texto=str(num)+" was the number!"
                color = "green"
                session["game_over"] = 1
                session["winner"] = 1
                session["message_intent"] = "Usted realizó "+str(session['contador'])+" intentos"
            
            session["message"] = texto
            session["color"] = color
            session["contador"] += 1
        else:
            session["game_over"] = 1 # se utiliza para volver a iniciar el juego
            session["message_intent"] = "Usted alcanzo el máximo de intentos"
    else:
        session.pop("number_random")
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

