from flask import Blueprint, Response, request
from models.usuario import db, Usuario
import json

app = Blueprint("usuario", __name__)


@app.route("/")
def index():
    # Is returned an iterator with
    #  all users
    usuarios = Usuario.query.all()
    # Cast every object into dict
    result = [u.to_dict() for u in usuarios]
    return Response(response=json.dumps({"status": "success", "data": result}), status=200, content_type="application/json")


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(force=True)
    usuario = Usuario(
        data["nome"], 
        data["sobrenome"],
        data["email"],
        data["senha"],
        data["dataDeAniversario"],
        data["genero"]
        )
    # Converte a data de aniversário do usuário para datetime
    usuario.birthday_to_datetime()
    db.session.add(usuario)
    db.session.commit()
    # Retorna a resposta em json
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")


@app.route("/edit/<useremail>", methods=["PUT", "POST"])
def edit(useremail):
    # Localiza o usuário no banco pelo email
    usuario = Usuario.query.where(Usuario.email == useremail).first()
    data = request.get_json(force=True)
    usuario.nome = data["nome"]
    usuario.sobrenome = data["sobrenome"]
    usuario.email = data["email"]
    usuario.senha = data["senha"]
    usuario.dataDeAniversario = data["dataDeAniversario"]
    usuario.genero = data["genero"]
    usuario.birthday_to_datetime()
    db.session.commit()
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")


@app.route("/delete/<useremail>", methods=["DELETE", "GET"])
def delete(useremail):
    usuario = Usuario.query.where(Usuario.email == useremail).first()
    db.session.delete(usuario)
    db.session.commit()
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")


@app.route("/getuser/<useremail>", methods=["GET"])
def getUser(useremail):

    usuarios = Usuario.query.where(Usuario.email == useremail)
    usuario = usuarios.first()

    if usuario:
        usuario = usuario.to_dict()
    else:
        usuario = {}

    return Response(response=json.dumps({"status": "success", "data": usuario}), status=200, content_type="application/json")



# @app.route("/logout")
# def logout():
#     # Remove the username from the session
#     session.pop("username", None)
#     return redirect(url_for("index"))