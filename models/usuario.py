from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(150))
    sobrenome = db.Column("sobrenome", db.String(150))
    email = db.Column("email", db.String(150))
    senha = db.Column("senha", db.String(150))
    dataDeAniversario = db.Column("data_de_aniversario", db.Date)
    genero = db.Column("genero", db.String(30))

    def __init__(self, nome, sobrenome, email, senha, dataDeAniversario, genero):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.dataDeAniversario = dataDeAniversario
        self.genero = genero
        

    def birthday_to_str(self):
        """ Cast user birthday from datetime to string
        """
        from datetime import datetime
        self.dataDeAniversario = datetime.strftime(self.dataDeAniversario, "%Y-%m-%d")

    def birthday_to_datetime(self):
        """ Cast user birthday from string to datetime
        """
        from datetime import datetime
        self.dataDeAniversario = datetime.strptime(self.dataDeAniversario, "%Y-%m-%d")
    
    def to_dict(self, columns=[]):
        # Verifica se foram informadas colunas para filtrar o retorno
        self.birthday_to_str()

        if not columns:
            return {
                "id": self.id,
                "nome": self.nome,
                "sobrenome": self.sobrenome,
                "email": self.email,
                "senha": self.senha,
                "dataDeAniversario": self.dataDeAniversario,
                "genero": self.genero
            }
        else:
            return {col: getattr(self, col) for col in columns}


