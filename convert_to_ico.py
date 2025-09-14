from PIL import Image
import os

# Convertir PNG a ICO
png_path = "logo_ine.png"
ico_path = "logo_ine.ico"

if os.path.exists(png_path):
    img = Image.open(png_path)
    
    # Crear múltiples tamaños para el ICO (Windows estándar)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    print(f"[OK] Icono creado exitosamente: {ico_path}")
else:
    print(f"[ERROR] No se encontro el archivo: {png_path}")