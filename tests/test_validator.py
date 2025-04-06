import unittest
import os
import sys

# Adicionar o diretório raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.image_validator import validate_image
import tempfile
import numpy as np
import cv2

class TestImageValidator(unittest.TestCase):
    def setUp(self):
        # Criar um diretório temporário para imagens de teste
        self.test_dir = tempfile.mkdtemp()

    def create_test_image(self, width, height, brightness=127):
        # Criar uma imagem de teste com brightness específico
        image = np.full((height, width, 3), brightness, dtype=np.uint8)
        
        # Adicionar um rosto simples (simulado)
        cv2.rectangle(image, (width//4, height//4), (3*width//4, 3*height//4), (0, 0, 0), 2)
        
        filepath = os.path.join(self.test_dir, 'test_image.jpg')
        cv2.imwrite(filepath, image)
        return filepath

    def test_image_resolution_too_small(self):
        # Testar imagem com resolução menor que o mínimo
        filepath = self.create_test_image(300, 200)
        result = validate_image(filepath)
        self.assertFalse(result['is_valid'])
        self.assertIn('Resolução inadequada', result['messages'][0])

    def test_image_resolution_acceptable(self):
        # Testar imagem com resolução aceitável
        filepath = self.create_test_image(800, 600)
        result = validate_image(filepath)
        self.assertTrue(result['is_valid'])

    def test_image_brightness(self):
        # Testar imagem com brilho muito baixo
        filepath = self.create_test_image(800, 600, brightness=20)
        result = validate_image(filepath)
        self.assertFalse(result['is_valid'])
        self.assertIn('Brilho inadequado', result['messages'][0])

    def tearDown(self):
        # Limpar arquivos temporários
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Erro ao deletar {file_path}. Razão: {e}")
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()