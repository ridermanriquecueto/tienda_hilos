La Casa de Hilos y Repuestos
La Casa de Hilos y Repuestos es una aplicación web de comercio electrónico desarrollada con Django, un framework de Python. Está orientada a la gestión y venta de productos relacionados con hilos y repuestos. El sistema ofrece una plataforma completa para gestionar productos, controlar inventario y realizar promociones para atraer clientes.

Características Principales
Gestión de Productos: Los administradores pueden agregar, actualizar y eliminar productos del catálogo.
Base de Datos: Utiliza una base de datos SQLite para almacenar información de productos como nombre, precio, descripción y stock.
Interfaz de Usuario: Diseño responsive que proporciona una experiencia de usuario optimizada tanto en dispositivos móviles como de escritorio.
Promoción de Productos: Permite gestionar promociones y propaganda para facilitar la venta de productos especiales.
Gestión de Inventario: Control del stock de cada producto, evitando la venta de productos fuera de inventario.
Tecnologías Utilizadas
Django: Framework de desarrollo web basado en Python.
Python 3: Lenguaje de programación utilizado para el backend.
HTML/CSS/JavaScript: Tecnologías para el diseño y la interactividad de la aplicación.
SQLite: Base de datos ligera utilizada para almacenar información de los productos.
Instalación
1. Clonar el Repositorio
bash

Copiar
git clone https://github.com/tu_usuario/la_casa_de_hilos.git
cd la_casa_de_hilos
3. Crear un Entorno Virtual (opcional pero recomendado)
bash
Copiar
python3 -m venv env
source env/bin/activate  # Para sistemas Unix
env\Scripts\activate  # Para Windows
4. Instalar Dependencias
bash
Copiar
pip install -r requirements.txt
5. Realizar Migraciones de la Base de Datos
bash
Copiar
python manage.py migrate
6. Ejecutar el Servidor Local
bash
Copiar
python manage.py runserver
Accede a la aplicación a través de http://127.0.0.1:8000 en tu navegador.
