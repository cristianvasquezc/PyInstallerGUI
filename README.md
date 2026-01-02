# PyInstaller GUI Builder

<div align="center">

![PyInstaller GUI](icon.ico)

**Una interfaz gráfica moderna y completa para PyInstaller**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-6.17.0-green.svg)](https://pyinstaller.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Descripción

**PyInstaller GUI Builder** es una aplicación de escritorio con interfaz gráfica que simplifica el proceso de convertir scripts de Python en ejecutables independientes usando PyInstaller. Diseñada para desarrolladores que prefieren una interfaz visual intuitiva sobre la línea de comandos, esta herramienta ofrece acceso completo a todas las funcionalidades de PyInstaller de manera organizada y fácil de usar.

## ✨ Características Principales

### 🎯 Interfaz Intuitiva

- **Diseño limpio y organizado** con pestañas para diferentes configuraciones
- **Vista previa del icono** con selección visual mediante clic
- **Campos de entrada claros** para script principal, nombre de salida y carpeta de destino
- **Ventana de logs en tiempo real** que muestra el progreso de la compilación

### ⚙️ Configuración Completa

#### Opciones Básicas

- ✅ **Onefile**: Genera un único archivo ejecutable
- ✅ **Windowed**: Ejecutable sin ventana de consola (ideal para aplicaciones GUI)
- ✅ **Clean build**: Limpia archivos temporales antes de compilar
- ✅ **Strip**: Reduce el tamaño del ejecutable eliminando símbolos de depuración
- ✅ **No UPX**: Desactiva la compresión UPX

#### Gestión de Recursos (Pestaña "Datos")

- 📁 **Añadir archivos individuales**: Incluye archivos de datos específicos
- 📂 **Añadir carpetas completas**: Incluye directorios enteros con su contenido
- 🗑️ **Eliminar recursos**: Gestión fácil de los recursos añadidos

#### Binarios Externos (Pestaña "Binarios")

- 🔧 **Añadir bibliotecas compiladas**: Incluye archivos .dll, .so, .dylib
- 📦 **Gestión de dependencias nativas**: Asegura que todos los binarios necesarios estén incluidos

#### Imports Ocultos (Pestaña "Imports")

- 🔍 **Añadir módulos ocultos**: Especifica imports que PyInstaller no detecta automáticamente
- 📝 **Interfaz simple**: Diálogo de entrada para nombres de módulos

#### Configuración Avanzada (Pestaña "Avanzado")

- 🐛 **Debug**: Opciones de depuración (all, imports)
- 📊 **Log level**: Nivel de detalle de los logs (DEBUG, INFO, WARN)

### 🎨 Personalización

- 🖼️ **Icono personalizado**: Selecciona el icono para tu ejecutable
- 🏷️ **Nombre personalizado**: Define el nombre del archivo de salida
- 📍 **Carpeta de destino**: Elige dónde guardar el ejecutable generado

### 📺 Monitoreo en Tiempo Real

- 💻 **Ventana de logs**: Muestra el comando generado y la salida de PyInstaller
- ✅ **Notificaciones de estado**: Alertas de éxito o error al finalizar
- 🔄 **Proceso en segundo plano**: La interfaz permanece responsiva durante la compilación

## 🚀 Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**

```bash
git clone https://github.com/cristianvasquezc/PyInstallerGUI.git
cd PyInstallerGUI
```

2. **Crear un entorno virtual (recomendado)**

```bash
python -m venv .venv
```

3. **Activar el entorno virtual**

En Windows:

```bash
.venv\Scripts\activate
```

En Linux/macOS:

```bash
source .venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar la Aplicación

```bash
python main.py
```

### Flujo de Trabajo Básico

1. **Seleccionar el script principal**

   - Haz clic en "Seleccionar" junto a "Script Principal (.py)"
   - Navega hasta tu archivo Python principal

2. **Configurar el nombre de salida**

   - Ingresa el nombre deseado para tu ejecutable (por defecto: "setup")

3. **Seleccionar carpeta de destino**

   - Haz clic en "Seleccionar" junto a "Carpeta de salida"
   - Elige dónde se guardará el ejecutable

4. **Configurar opciones**

   - Marca/desmarca las opciones según tus necesidades
   - Por defecto: Onefile y Windowed están activados

5. **Añadir recursos (opcional)**

   - Ve a la pestaña "Datos" para incluir archivos o carpetas
   - Ve a la pestaña "Binarios" para incluir bibliotecas compiladas
   - Ve a la pestaña "Imports" para añadir módulos ocultos

6. **Seleccionar icono (opcional)**

   - Haz clic en el área del icono (esquina superior izquierda)
   - Selecciona un archivo .ico

7. **Procesar**
   - Haz clic en el botón "Procesar"
   - Se abrirá una ventana mostrando el progreso
   - Espera a que finalice el proceso

### Ejemplo de Uso

```
Script Principal: C:\MiProyecto\app.py
Nombre: MiAplicacion
Carpeta de salida: C:\MiProyecto\dist
Opciones: Onefile ✓, Windowed ✓
Icono: C:\MiProyecto\icon.ico
```

Esto generará: `C:\MiProyecto\dist\MiAplicacion.exe`

## 📁 Estructura del Proyecto

```
PyInstallerGUI/
│
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias del proyecto
├── icon.ico               # Icono de la aplicación
├── installer-icon.ico     # Icono por defecto para ejecutables
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Este archivo
```

## 🛠️ Dependencias

- **Pillow (12.0.0)**: Procesamiento de imágenes para la vista previa del icono
- **PyInstaller (6.17.0)**: Motor de conversión a ejecutable

## 🔧 Compilar la Aplicación

Para distribuir PyInstaller GUI Builder como un ejecutable independiente:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name=PyInstallerGUI --add-data "icon.ico;." --add-binary ".venv/Scripts/pyinstaller.exe;." main.py
```

O simplemente usa la propia aplicación para compilarse a sí misma:

1. Ejecuta `python main.py`
2. Selecciona `main.py` como script principal
3. Configura las opciones deseadas
4. Haz clic en "Procesar"

## 📝 Notas Técnicas

### Gestión de Recursos

La aplicación utiliza `sys._MEIPASS` para manejar rutas de recursos cuando se ejecuta como ejecutable empaquetado, asegurando que los iconos y otros archivos se carguen correctamente.

### Ventana de Logs

El proceso de compilación se ejecuta en un hilo separado para mantener la interfaz responsiva. Los logs se muestran en tiempo real con formato de terminal (fondo negro, texto verde).

### Comando Generado

La aplicación construye dinámicamente el comando de PyInstaller basándose en las opciones seleccionadas. El comando completo se muestra en la ventana de logs para referencia y depuración.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👤 Autor

Desarrollado con ❤️ por [Cristian Vásquez](https://mislinks.netlify.app/) para simplificar el proceso de empaquetado de aplicaciones Python.

## 🙏 Agradecimientos

- **PyInstaller Team**: Por la excelente herramienta de empaquetado
- **Tkinter**: Por proporcionar una interfaz GUI nativa multiplataforma
- **Pillow**: Por el procesamiento de imágenes

---

<div align="center">

**¿Te resultó útil esta herramienta? ¡Dale una ⭐ al repositorio!**

</div>
