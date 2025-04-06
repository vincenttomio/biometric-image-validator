import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sup3r_s3cr3t_k3y!@#19794-5'  # Chave mais segura
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Limite de 16MB para uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}