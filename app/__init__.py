from flask import Flask

def create_app():
    # Crear una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configurar la aplicación usando una clase de configuración
    # app.config.from_object(Config)

    # Importar las rutas de la aplicación
    # from app import routes

    # Puedes importar extensiones de Flask aquí, si las estás utilizando
    # Por ejemplo, para trabajar con una base de datos:
    # from flask_sqlalchemy import SQLAlchemy
    # db = SQLAlchemy(app)

    # Puedes realizar otras inicializaciones aquí, como configurar autenticación, correos electrónicos, etc.

    return app