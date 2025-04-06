from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_class)

    # Criar diretório de uploads se não existir
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Importar e registrar rotas usando blueprint
    from .routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Inicializar extensões (importante para sessions)
    with app.app_context():
        from flask import session  # Mantém a sessão ativa
        app.secret_key = app.config['SECRET_KEY']  # Confirmação explícita
    
    return app