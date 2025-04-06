# Biometric Image Validator 🖼️👤

#### Video Demo: 
#### Description:



[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-brightgreen)](https://opencv.org/)

A web application for validating facial images against [ISO/IEC 19794-5 biometric standards](https://www.iso.org/standard/51522.html), developed as the final project for Harvard's CS50X course.

---

## ✨ Features

- 🎯 ISO Standard Compliance Checks
- 🔍 Advanced Face Detection
- 📊 Image Quality Analysis
- 📈 Detailed Validation Reports
- 🛡️ Secure File Handling

---

## 📂 Project Structure

```
biometric-image-validator/
│
├── app/                     # Core application logic
│   ├── __init__.py          # Initializes the Flask app
│   ├── routes.py            # Defines application routes
│   ├── image_validator.py   # Contains image validation logic
│   └── templates/           # HTML templates for the web interface
|       ├── about.html       # About page template
│       ├── index.html       # Home page template
│       └── result.html      # Results page template
│
├── tests/                   # Unit tests for the application
│   ├── __init__.py          # Initializes the test package
│   └── test_validator.py    # Tests for image validation functions
│
├── static/                  # Static files (CSS, images, etc.)
│   ├── css/
│   │   └── styles.css       # Stylesheet for the application
│   └── uploads/             # Directory for uploaded images
│
├── requirements.txt         # Python dependencies
├── config.py                # Configuration settings
└── run.py                   # Entry point to run the application
```

## 📋 Key Requirements

### 🧪 Technical Specifications

- **Image Resolution**: 640x480px (min) – 4000x4000px (max)
- **Color Depth**: 24-bit True Color
- **File Formats**: JPEG, PNG
- **Facial Requirements**: Frontal view, neutral expression, no occlusions

### 🧰 Core Dependencies

- Flask (Web Framework) - v2.0.3
- OpenCV (Image Processing) - v4.5.5
- Pillow (Image Handling) - v9.0.1
- NumPy (Numerical Analysis) - v1.22.0
- scikit-image (Quality Metrics) - v0.19.2

---

## 🛠️ Installation

1. **Clone the repository:**

```
git clone https://github.com/vincenttomio/biometric-image-validator.git
cd biometric-image-validator
```

2. **Install dependencies:**
```
pip install -r requirements.txt
```

3. **Configure environment (optional - `config.py`):**

   If the `config.py` file does not exist, create it in the project root directory and add the following content:
   ```
   UPLOAD_FOLDER = 'static/uploads'
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
   MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB
   ```
   You can modify these settings as needed for your environment.
```
# config.py
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB
```

## 🚀 Usage

To run the application, use the following command:

```
flask run
```

### Application Flow:

1. **Upload Image**: Use the web interface to upload an image.
2. **Automatic Validation**: The application processes the image for validation.
3. **View Report**: Access a detailed compliance report.
4. **Technical Metrics**: Review in-depth analysis and metrics.

---

### 🔬 Validation Criteria

| **Category**         | **Checks Performed**                          |
|-----------------------|-----------------------------------------------|
| **Image Quality**     | Brightness, Contrast, Sharpness, Noise        |
| **Facial Features**   | Position, Rotation, Expression               |
| **Technical Compliance** | Resolution, File Format, Color Depth       |
| **ISO Standards**     | ISO/IEC 19794-5 Requirements Implementation  |

---

### 💻 Key Functions

```python
def validate_image(image_path):
    """Main validation workflow"""
    # 1. Check resolution and format
    # 2. Analyze image quality metrics
    # 3. Detect and measure facial features
    # 4. Generate compliance report

def calculate_face_metrics(image):
    """Calculate facial characteristics"""
    # - Face positioning
    # - Symmetry analysis
    # - Expression evaluation
```

---

### 🔒 Security Considerations

- **Secure File Upload Validation**: The application ensures secure file uploads by:
  - Restricting allowed file extensions to `.png`, `.jpg`, and `.jpeg` using the `ALLOWED_EXTENSIONS` set in `config.py`.
  - Limiting file size to 8MB through the `MAX_CONTENT_LENGTH` setting.
  - Validating uploaded files in the `allowed_file` function within `routes.py`, which checks the file extension before processing.
- Temporary file cleanup.
- Exception handling for errors.
- File size restrictions (8MB max).
- Whitelist for allowed extensions (`.png`, `.jpg`, `.jpeg`).
### 🗺️ Future Roadmap

| **Feature**                     | **Priority** |
|----------------------------------|--------------|
| AI-powered validation models     | High         |
| Multi-image batch processing     | Medium       |
| PDF report generation            | Medium       |
| API endpoint integration         | Low          |
| Enhanced visualization tools     | Low          |
- PDF report generation.
- API endpoint integration.
- Enhanced visualization tools.

---

### 🙏 Acknowledgments

Special thanks to:
- **[CS50 Staff](https://cs50.harvard.edu/)** for the incredible curriculum.
- **[OpenCV community](https://docs.opencv.org/)** for excellent documentation.
- **[ISO organization](https://www.iso.org/iso-iec-19794-5.html)** for biometric standards.
---

### ✅ Compliance

This project adheres to all academic honesty requirements of the CS50x course.

---

### ℹ️ Notes

- README written in English to comply with CS50x standards.
- Designed for technical clarity and presentation quality.
- Project reflects progression from concept to full implementation.

---

