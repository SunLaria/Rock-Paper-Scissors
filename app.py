from flask import Flask,redirect,url_for,render_template,request,session
import random
from whitenoise import WhiteNoise


user_hands={
    "r":"/static/rock-right.png",
    "p":"/static/right-hand.png",
    "s":"/static/scissors-right.png"
}
pc_hands={
    "r":"/static/rock-left.png",
    "p":"/static/hand-left.png",
    "s":"/static/scissors-left.png"
}

app=Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/", prefix='static/')
app.secret_key="123456"

@app.route('/')
def home():
    session["score"]={"user":0,"pc":0}
    return render_template('home.html')

@app.route("/game", methods=["GET","POST"])
def game():
    if request.method=="GET":
        if request.args.get("user_image") and request.args.get("pc_image"):
            user_image = request.args["user_image"]
            pc_image = request.args["pc_image"]
        else:
            user_image = user_hands["r"]
            pc_image = pc_hands["r"]
        return render_template('game.html',user_image=user_image,pc_image=pc_image,score=session["score"])

    if request.method=="POST":
        user_choice = request.form["user_choose"]
        pc_choice = random.choice(list(pc_hands.keys()))
        score = session["score"]
        hands = user_choice+pc_choice
        even=["pp","rr","ss"]
        user_win = ["pr","rs","sp"]
        if hands in even:
            pass
        elif hands in user_win:
            score["user"]+=1
        else:
            score["pc"]+=1
        session["score"] = score
        
        return redirect(url_for("game", pc_image=pc_hands[pc_choice], user_image=user_hands[user_choice],score=session["score"]))
