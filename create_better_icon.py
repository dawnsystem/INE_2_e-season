"""
Script mejorado para crear un icono ICO con múltiples resoluciones
manteniendo las proporciones del logo original
"""

from PIL import Image
import os

def create_multisize_ico(input_png, output_ico):
    """
    Crea un archivo ICO con múltiples resoluciones manteniendo las proporciones
    """
    # Abrir la imagen PNG original
    img = Image.open(input_png)
    
    # Convertir a RGBA si no lo es
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Tamaños estándar para iconos de Windows
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Lista para almacenar las imágenes redimensionadas
    images = []
    
    for size in sizes:
        # Crear una nueva imagen cuadrada con fondo transparente
        new_img = Image.new('RGBA', size, (255, 255, 255, 0))
        
        # Calcular el tamaño manteniendo la proporción
        img_ratio = img.width / img.height
        
        if img_ratio > 1:  # Imagen más ancha que alta
            new_width = size[0]
            new_height = int(size[0] / img_ratio)
        else:  # Imagen más alta que ancha o cuadrada
            new_height = size[1]
            new_width = int(size[1] * img_ratio)
        
        # Asegurar que no exceda el tamaño del canvas
        if new_width > size[0]:
            new_width = size[0]
            new_height = int(new_width / img_ratio)
        if new_height > size[1]:
            new_height = size[1]
            new_width = int(new_height * img_ratio)
        
        # Redimensionar la imagen original
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calcular la posición para centrar la imagen
        x = (size[0] - new_width) // 2
        y = (size[1] - new_height) // 2
        
        # Pegar la imagen redimensionada en el centro
        new_img.paste(resized, (x, y), resized)
        
        images.append(new_img)
        
        print(f"  Creada resolución {size[0]}x{size[1]}")
    
    # Guardar como ICO con todas las resoluciones
    images[0].save(output_ico, format='ICO', sizes=[(img.width, img.height) for img in images])
    
    print(f"\nIcono creado exitosamente: {output_ico}")
    print(f"Resoluciones incluidas: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")

def main():
    print("=" * 60)
    print("CREADOR DE ICONOS MEJORADO PARA INE_4_e-season")
    print("=" * 60)
    print()
    
    input_file = "logo_ine.png"
    output_file = "logo_ine.ico"
    
    if not os.path.exists(input_file):
        print(f"ERROR: No se encontró el archivo {input_file}")
        return
    
    print(f"Procesando: {input_file}")
    print()
    
    try:
        # Crear copia de seguridad del icono anterior si existe
        if os.path.exists(output_file):
            backup_file = "logo_ine_backup.ico"
            os.rename(output_file, backup_file)
            print(f"Copia de seguridad creada: {backup_file}")
        
        create_multisize_ico(input_file, output_file)
        
        print()
        print("PROCESO COMPLETADO")
        print("-" * 60)
        print("El nuevo icono mantiene las proporciones correctas")
        print("y no se verá deformado en Windows.")
        print()
        print("Próximos pasos:")
        print("1. Verificar el icono en el explorador de Windows")
        print("2. Ejecutar build_exe.bat para recompilar con el nuevo icono")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        # Restaurar el backup si algo falló
        if os.path.exists("logo_ine_backup.ico"):
            os.rename("logo_ine_backup.ico", output_file)
            print("Se restauró el icono anterior debido al error")

if __name__ == "__main__":
    main()