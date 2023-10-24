from flask import render_template, request, redirect, url_for
from app import app

@app.route("/")
def mainPage():
    return render_template("index.html")

@app.route("/receive_message",methods=['POST'])
def receive_message():
    data=request.get_json()
    return "Mensaje Recibido con exito" 