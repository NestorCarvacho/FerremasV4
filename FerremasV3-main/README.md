# 🛒 Django Ecommerce API

Este proyecto es una API REST para gestionar productos de un sistema de ecommerce, desarrollada con Django, Django REST Framework, y MySQL. Usa procedimientos almacenados en la base de datos y autenticación JWT.

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.8 o superior
- MySQL Server
- MySQL Workbench (opcional, para ejecutar scripts SQL gráficamente)
- Git (opcional)
- Postman (opcional, para pruebas)

---

## ⚙️ Instalación del Proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/NestorCarvacho/FerremasV3.git
cd ~/FerremasV3
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Configura las variables de entorno (opcional pero recomendado)

Puedes usar un archivo `.env` (con `python-decouple`, `django-environ`, etc.) o configurar directamente en `settings.py`.

Variables mínimas recomendadas:

```
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=tu_clave_secreta_django
DEBUG=True
```

> Si usas `.env`, asegúrate de cargar esas variables con la librería correspondiente en `settings.py`.

---

## 🗄️ Configuración de la Base de Datos

1. Crea una base de datos en MySQL (ej: `ecommerce_db`).

2. Ejecuta en MySQL Workbench o consola los archivos:

   - `createTables.sql` – para crear tablas necesarias.
   - `createProcedures.sql` – para cargar procedimientos almacenados.

3. En `settings.py`, configura la conexión MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

---

## 🔧 Migraciones y Usuarios

1. Aplica las migraciones de Django:

```bash
python manage.py migrate
```

2. Crea un superusuario o usuario para autenticación JWT:

```bash
python manage.py createsuperuser
```

---

## 🔐 Autenticación JWT

### 1. Obtener un token:

```
POST /api/token/
```

Body (JSON):

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

### 2. Usar el token en Postman:

- En la pestaña Authorization, selecciona **Bearer Token**.
- Pega el valor del campo `"access"` recibido al autenticarte.

---

## 📚 Documentación Swagger

Para explorar los endpoints:

```
http://localhost:8000/swagger/
```

---

## ▶️ Ejecutar el Servidor

```bash
python manage.py runserver
```

---

## 🚀 Despliegue en Producción

1. Usa `DEBUG=False` en producción.
2. Define un `SECRET_KEY` seguro.
3. Configura un servidor web como **Nginx + Gunicorn** o **Apache + mod_wsgi**.
4. Usa HTTPS y configura CORS si será consumida desde frontend externo.
5. Asegúrate de limitar acceso a `/swagger/` en entornos públicos.

---

## 📝 Notas Adicionales

- Los endpoints usan procedimientos almacenados para acceder a la base de datos.
- Se requiere autenticación JWT para acceder a la mayoría de recursos.
- Se recomienda usar entornos virtuales para instalar dependencias.

---

## 📧 Soporte

Para dudas o reportes, contáctame en: ne.carvacho@duocuc.cl
