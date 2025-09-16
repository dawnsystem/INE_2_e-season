# Guía de Contribución

¡Gracias por tu interés en contribuir a INE Transformer 4 E-Season! 🎉

## 📋 Antes de empezar

Este proyecto fue creado específicamente para procesar datos de E-Season PMS para las encuestas del INE español. Las contribuciones son bienvenidas, especialmente si:
- Mejoran la compatibilidad con E-Season
- Añaden funcionalidades útiles para el procesamiento INE
- Corrigen bugs o mejoran el rendimiento
- Mejoran la documentación

## 🚀 Cómo contribuir

### 1. Fork y Clone
```bash
# Fork el proyecto en GitHub
# Luego clona tu fork
git clone https://github.com/tu-usuario/ine_transformer.git
cd ine_transformer
```

### 2. Crea una rama
```bash
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-del-bug
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Realiza tus cambios
- Mantén el estilo de código existente
- Comenta el código cuando sea necesario
- Actualiza la documentación si cambias funcionalidades

### 5. Prueba tus cambios
- Asegúrate de que la aplicación funciona correctamente
- Prueba con archivos de ejemplo de E-Season
- Verifica que las exportaciones son correctas

### 6. Commit
```bash
git add .
git commit -m "tipo: descripción breve

Descripción más detallada si es necesario"
```

Tipos de commit:
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (sin afectar funcionalidad)
- `refactor:` Refactorización de código
- `test:` Añadir tests
- `chore:` Tareas de mantenimiento

### 7. Push y Pull Request
```bash
git push origin feature/nombre-descriptivo
```
Luego abre un Pull Request en GitHub.

## 📝 Estándares de código

### Python
- Seguir PEP 8
- Nombres de variables y funciones en español (proyecto en español)
- Comentarios explicativos para lógica compleja
- Docstrings para funciones públicas

### Estructura
```python
def procesar_datos_ine(archivo_excel):
    """
    Procesa los datos exportados de E-Season para formato INE.

    Args:
        archivo_excel: Path al archivo Excel de E-Season

    Returns:
        DataFrame con los datos procesados
    """
    # Tu código aquí
```

## 🐛 Reportar bugs

Si encuentras un bug:
1. Verifica que no esté ya reportado en [Issues](../../issues)
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Versión de E-Season si es relevante
   - Mensajes de error (si los hay)
   - Screenshots si ayudan

## 💡 Sugerir mejoras

Para sugerir nuevas funcionalidades:
1. Verifica que no esté ya sugerida
2. Abre un issue con la etiqueta `enhancement`
3. Describe:
   - La funcionalidad deseada
   - Por qué sería útil
   - Posible implementación (opcional)

## 🌍 Traducciones

Actualmente el proyecto está en español. Si deseas traducirlo:
- Contacta primero para coordinar
- Mantén la terminología técnica del INE

## ❓ Preguntas

Si tienes dudas:
- Revisa la documentación existente
- Busca en issues cerrados
- Abre un issue con la etiqueta `question`

## 📜 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Respeta las decisiones del mantenedor

## ⚖️ Licencia

Al contribuir, aceptas que tus contribuciones estarán bajo la misma licencia MIT del proyecto.

---

**¿Necesitas ayuda?** Contacta a darenas@capfun.com

¡Gracias por hacer INE Transformer mejor! 🚀