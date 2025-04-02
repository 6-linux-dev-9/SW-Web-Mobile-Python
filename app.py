
# importa desde el app/__init__ de una manera magica
# es decir se dispara cuando hacemos esto
from app import create_app


app = create_app()

PORT = 8080
host = '127.0.0.1'

#ni idea
if __name__ == "__main__":
    app.run(host = host, port=PORT,debug=True)
