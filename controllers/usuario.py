from flask import Blueprint, Response, request
from models.usuario import db, Usuario
import json
import re

def validate_email(email):
  """Valida um endereço de email.

  Args:
    email: O endereço de email a ser validado.

  Returns:
    True se o endereço de email for válido, False se for inválido.
  """

  regex = re.compile(r'^[a-zA-Z0-9_\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$')
  return regex.match(email) is not None

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
def add(data={}):
    if not data:
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
def edit(useremail, data={}):
    # Localiza o usuário no banco pelo email
    usuario = Usuario.query.where(Usuario.email == useremail).first()

    if not data:
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

    if validate_email(useremail):
        usuarios = Usuario.query.where(Usuario.email == useremail)
        usuario = usuarios.first()

        if usuario:
            usuario = usuario.to_dict()
        else:
            usuario = {}

        return Response(response=json.dumps({"status": "success", "data": usuario}), status=200, content_type="application/json")
    else:
        return Response(response=json.dumps({"status": "bad request", "data": {"senha": ""}, "message": "The email address is invalid"}), status=400, content_type="application/json")


# @app.route("/logout")
# def logout():
#     # Remove the username from the session
#     session.pop("username", None)
#     return redirect(url_for("index"))