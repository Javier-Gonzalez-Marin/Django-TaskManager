# Instrucciones para ejecutar en local

## Descomprimir el proyecto:
   
Crear y activar entorno virtual:

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

Instalar dependencias:

pip install -r requirements.txt
Aplicar migraciones:

python manage.py migrate

Crear superusuario (para acceso admin):(deberia de estar creado correctamente de todos modos pero me ha dado muchos fallos)

python manage.py createsuperuser

Ejecutar servidor local:

python manage.py runserver
Abrir navegador en:

http://127.0.0.1:8000/



## Memoria del proceso de despliegue

El proyecto Django Task Manager fue desplegado en la plataforma Render.com. Se configuró el entorno para Python 3.11, gestionando dependencias con un `requirements.txt` actualizado.

## Pasos del despliegue

## Configuración del repositorio:
   Se subió el código al repositorio Git vinculado a Render.

## Configuración de entorno en Render:
   - Comando de inicio con Gunicorn:  
     
     gunicorn mysite.wsgi:application
     
   - Variables de entorno configuradas:  
     `DJANGO_SETTINGS_MODULE`, `SECRET_KEY`, entre otras.

## Base de datos:
   - Uso de SQLite para simplicidad.
   - Migraciones aplicadas con:  
     
     python manage.py migrate
     
   - Se solucionó el error `no such table: auth_user` asegurando la correcta ejecución de migraciones.

## Errores encontrados y solución: 
   - Error 404 en `/accounts/login/`: se agregaron rutas de autenticación en `urls.py`.
   - Problemas con variable `LOGIN_REDIRECT_URL`: se añadió en `settings.py`.
   - Error `ModuleNotFoundError` en el WSGI: corregido apuntando correctamente a `mysite.wsgi:application`.
   - Creación y acceso al usuario administrador configurado.

## Configuraciones adicionales:
   - Configuración de `ALLOWED_HOSTS` para el dominio Render.
   - Uso de Whitenoise para servir archivos estáticos.


## Enlace a la web desplegada


https://django-taskmanager-uznp.onrender.com/ (dashboard)
https://django-taskmanager-uznp.onrender.com/admin (para la vista de admin)
