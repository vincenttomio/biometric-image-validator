from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from .image_validator import validate_image

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

@bp.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'danger')  # Translated
            return redirect(url_for('main.upload_image'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'danger')  # Translated
            return redirect(url_for('main.upload_image'))
        
        if file and allowed_file(file.filename):
            try:
                filepath = save_file(file)
                validation_result = validate_image(filepath)
                
                # Convert absolute paths to relative
                if validation_result.get('processed_image'):
                    validation_result['processed_image'] = os.path.relpath(
                        validation_result['processed_image'], 
                        current_app.config['UPLOAD_FOLDER']
                    )
                
                validation_result['original_image'] = os.path.relpath(
                    filepath, 
                    current_app.config['UPLOAD_FOLDER']
                )
                
                return render_template('result.html', result=validation_result)
            
            except Exception as e:
                current_app.logger.error(f"Error processing image: {str(e)}")  # Translated
                flash('Error processing image', 'danger')  # Translated
                return redirect(url_for('main.upload_image'))
    
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')