import cv2
import numpy as np
from PIL import Image, ImageOps
import math
import os

def validate_image(image_path):
    """
    Complete biometric image validation with detailed metrics
    """
    result = {
        'is_valid': True,
        'messages': [],
        'metrics': {},
        'face_analysis': {},
        'processed_image': None
    }

    try:
        # Load image with Pillow for metadata
        pil_img = Image.open(image_path)
        
        # =====================================================================
        # 1. Metadata and basic properties
        # =====================================================================
        width, height = pil_img.size
        dpi = pil_img.info.get('dpi', (72, 72))  # Default to 72 DPI if not present
        
        result['metrics'] = {
            'resolution': {'width': width, 'height': height},
            'dpi': {'horizontal': dpi[0], 'vertical': dpi[1]},
            'color_space': pil_img.mode,
            'file_size': os.path.getsize(image_path)
        }

        # =====================================================================
        # 2. Image quality analysis
        # =====================================================================
        # Convert to OpenCV (BGR) and grayscale
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Quality metrics calculation
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        # Sharpness calculation (Laplacian Variance)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()

        # Illumination uniformity (divide image into 9 regions)
        regions = [
            gray[0:height//3, 0:width//3],       # Top-left
            gray[0:height//3, width//3:2*width//3], # Top-center
            gray[0:height//3, 2*width//3:width], # Top-right
            gray[height//3:2*height//3, 0:width//3], # Middle-left
            gray[height//3:2*height//3, width//3:2*width//3], # Center
            gray[height//3:2*height//3, 2*width//3:width], # Middle-right
            gray[2*height//3:height, 0:width//3], # Bottom-left
            gray[2*height//3:height, width//3:2*width//3], # Bottom-center
            gray[2*height//3:height, 2*width//3:width]  # Bottom-right
        ]
        region_brightness = [np.mean(r) for r in regions]
        brightness_uniformity = np.std(region_brightness)

        result['metrics'].update({
            'brightness': brightness,
            'contrast': contrast,
            'sharpness': sharpness,
            'illumination_uniformity': brightness_uniformity
        })

        # =====================================================================
        # 3. Face detection and analysis
        # =====================================================================
        # Use a more robust classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Adjustable parameters for face detection
        scale_factor = 1.1
        min_neighbors = 5
        min_face_size = (int(width * 0.15), int(height * 0.15))  # At least 15% of image size
        
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=scale_factor, 
            minNeighbors=min_neighbors, 
            minSize=min_face_size
        )
        
        # Store analysis of all faces
        all_faces_analysis = []
        
        # Add reference lines at image center
        cv2.line(img, (0, height//2), (width, height//2), (255, 0, 0), 1)  # Horizontal line
        cv2.line(img, (width//2, 0), (width//2, height), (255, 0, 0), 1)   # Vertical line
        
        # Process all detected faces
        for i, (x, y, w, h) in enumerate(faces):
            # Relative position
            face_position = {
                'center_x': (x + w/2) / width,
                'center_y': (y + h/2) / height,
                'width_ratio': w / width,
                'height_ratio': h / height
            }
            
            # Face ROI
            face_roi = gray[y:y+h, x:x+w]
            
            # Facial symmetry (simplified example)
            if w > 10 and h > 10:
                left = face_roi[:, 0:w//2]
                right = face_roi[:, w//2:w]
                right_flipped = cv2.flip(right, 1)
                if left.shape == right_flipped.shape:
                    symmetry = cv2.matchTemplate(left, right_flipped, cv2.TM_CCOEFF_NORMED)[0][0]
                else:
                    symmetry = 0.0
            else:
                symmetry = 0.0

            # Individual face analysis
            face_analysis = {
                'index': i,
                'position': face_position,
                'size': {'width': w, 'height': h},
                'symmetry': symmetry,
                'face_brightness': np.mean(face_roi),
                'face_contrast': np.std(face_roi)
            }
            
            all_faces_analysis.append(face_analysis)
            
            # Draw colored rectangle (different color for each face)
            color_hue = (i * 30) % 180
            color = cv2.cvtColor(np.uint8([[[color_hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            color = (int(color[0]), int(color[1]), int(color[2]))
            
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            
            # Add face number
            cv2.putText(img, f"Face #{i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Add face center marker
            center_face_x = int(x + w/2)
            center_face_y = int(y + h/2)
            cv2.drawMarker(img, (center_face_x, center_face_y), color, markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
            
            # Add positioning info
            position_text = f"X: {face_position['center_x']:.2f}, Y: {face_position['center_y']:.2f}"
            cv2.putText(img, position_text, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        result['face_analysis'] = {
            'count': len(faces),
            'faces': all_faces_analysis
        }
        
        if len(faces) > 0:
            result['primary_face'] = all_faces_analysis[0]
            
        # Save processed image
        processed_path = os.path.join(os.path.dirname(image_path), 'processed_' + os.path.basename(image_path))
        cv2.imwrite(processed_path, img)
        result['processed_image'] = processed_path

        # =====================================================================
        # 4. ISO standard validations (adjusted criteria)
        # =====================================================================
        # Minimum resolution (ISO 19794-5:2011)
        if width < 640 or height < 480:
            result['is_valid'] = False
            result['messages'].append(f"Resolution below minimum requirement (640x480): {width}x{height}")

        # Minimum DPI (300 recommended)
        if dpi[0] < 150 or dpi[1] < 150:
            result['warnings'] = result.get('warnings', [])
            result['warnings'].append(f"DPI below recommended (300): {dpi[0]}x{dpi[1]}")

        # Brightness (ISO/IEC 29794-1)
        if not (40 <= brightness <= 220):
            result['is_valid'] = False
            result['messages'].append(f"Brightness out of ideal range (40-220): {brightness:.1f}")

        # Contrast (ISO/IEC 29794-1)
        if contrast < 30:
            result['is_valid'] = False
            result['messages'].append(f"Insufficient contrast (<30): {contrast:.1f}")

        # Illumination uniformity
        if brightness_uniformity > 35:
            result['is_valid'] = False
            result['messages'].append(f"Non-uniform illumination (variation >35): {brightness_uniformity:.1f}")

        # Face detection
        if len(faces) == 0:
            result['is_valid'] = False
            result['messages'].append("No face detected")
        elif len(faces) > 1:
            result['is_valid'] = False
            result['messages'].append(f"Multiple faces detected ({len(faces)} faces)")
        else:
            face_position = all_faces_analysis[0]['position']
            
            if not (0.3 <= face_position['center_x'] <= 0.7):
                result['is_valid'] = False
                result['messages'].append(f"Face not horizontally centered (value={face_position['center_x']:.2f}, acceptable: 0.3-0.7)")
            
            if not (0.3 <= face_position['center_y'] <= 0.7):
                result['is_valid'] = False
                result['messages'].append(f"Face not vertically centered (value={face_position['center_y']:.2f}, acceptable: 0.3-0.7)")
            
            # Minimum face size
            if face_position['width_ratio'] < 0.15 or face_position['height_ratio'] < 0.15:
                result['is_valid'] = False
                result['messages'].append(f"Face too small in image (width={face_position['width_ratio']:.2f}, height={face_position['height_ratio']:.2f}, minimum: 0.15)")

        # Sharpness (Laplacian Variance)
        if sharpness < 80:
            result['is_valid'] = False
            result['messages'].append(f"Insufficient sharpness (<80): {sharpness:.1f}")

    except Exception as e:
        result['is_valid'] = False
        result['messages'].append(f"Processing error: {str(e)}")
        return result

    return result