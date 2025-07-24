# moolah

Plataforma de educación financiera para jóvenes sin historial crediticio. Cuenta con un backend en FastAPI y una app Flutter para registrar gastos y ahorros mientras otorga recompensas por buenas decisiones.

![logo](logo.png)

## Guía rápida

1. Clona este repositorio y entra en la carpeta del proyecto.
   ```bash
   git clone https://github.com/tuusuario/moolah.git
   cd moolah
   ```
2. Instala las dependencias del backend (incluye la versión fijada `bcrypt==3.2.0`):
   ```bash
   pip install -r requirements.txt
   ```
3. Copia el archivo `.env.example` a `.env` y define `MOOLAH_SECRET_KEY` 
   (puedes ajustar `DATABASE_URL` si usas otra base de datos).
4. Inicia la API:
   ```bash
   uvicorn moolah_backend.app.main:app --reload
   ```
   ![backend](backend.png)
5. (Opcional) Ejecuta el script de datos de ejemplo:
   ```bash
   python seed_db.py
   ```
   Ejecuta este script únicamente si la base de datos está vacía. Si necesitas
   volver a poblarla, borra `moolah.db` o las tablas existentes antes de
   ejecutarlo de nuevo.
6. Desde `moolah_frontend` descarga dependencias y lanza la app:
   ```bash
   flutter pub get
   flutter run
   ```
7. La documentación completa de la API está disponible en `http://localhost:8000/docs`.

### Funcionalidades principales
- Transacciones y categorías
- Metas de ahorro
- Presupuestos mensuales
- Recompensas por puntos
- Analytics y resúmenes


## Requisitos

 - Python 3.11 ó superior (recomendado debido a las versiones fijadas de las dependencias).
 - FastAPI 0.115 ó superior.
 - Pydantic 2.11 ó superior.

## Instalación

1. Clona el repositorio y entra en la carpeta del proyecto.
2. Instala las dependencias del backend (entre ellas `httpx`, necesaria para ejecutar las pruebas) y la version fijada `bcrypt==3.2.0`:

```bash
pip install -r requirements.txt
```

3. Define la variable de entorno `MOOLAH_SECRET_KEY` con la clave utilizada para firmar los JWT. La aplicación no arrancará si no se establece.
4. Puedes indicar otra base de datos estableciendo `DATABASE_URL`. Si no se especifica se creará `moolah.db` con SQLite.

### Variables de entorno

- `MOOLAH_SECRET_KEY`: clave secreta para firmar y verificar los JWT. **Obligatoria**.
- `DATABASE_URL`: cadena de conexión a la base de datos (por ejemplo `postgresql://usuario:pass@localhost/db`). Si se omite se utilizará SQLite en `moolah.db`.

Puedes copiar el archivo `.env.example` a `.env` y ajustar sus valores. Exporta cada variable antes de iniciar la aplicación o cárgalas desde ese archivo manualmente:

```bash
export MOOLAH_SECRET_KEY="tu-clave-super-secreta"
export DATABASE_URL="sqlite:///./moolah.db"
```

## Ejecución del servidor

Inicia el servidor de desarrollo con:

```bash
uvicorn moolah_backend.app.main:app --reload
```

Si has establecido la variable `DATABASE_URL`, ejecútalo de la siguiente forma:

```bash
DATABASE_URL=postgresql://usuario:clave@localhost/dbname \
    uvicorn moolah_backend.app.main:app --reload
```

Al ejecutarse por primera vez se creará automáticamente la base de datos SQLite `moolah.db` cuando no se defina `DATABASE_URL`.

Si deseas poblarla con datos de demostración ejecuta:

```bash
python seed_db.py
```

### Poblado de datos de ejemplo

El script `seed_db.py` crea categorías de gasto, varios usuarios de demostración
con sus metas de ahorro, presupuestos mensuales y transacciones. Es una forma
rápida de contar con información inicial para probar la API.

Antes de ejecutarlo asegúrate de haber definido las variables de entorno
`MOOLAH_SECRET_KEY` y, si corresponde, `DATABASE_URL`.

```bash
python seed_db.py
```

Solo debería ejecutarse sobre una base de datos vacía. Si necesitas
re-seedear los datos, elimina el archivo `moolah.db` o borra las tablas
existentes antes de volver a ejecutarlo. También puedes usar
`python seed_db.py --reset` para descartar todas las tablas automáticamente.

## Endpoints principales

- `POST /token` – Obtiene un token de acceso.
- `POST /users/` – Registra un usuario nuevo.
- `GET /users/me/` – Datos del usuario autenticado.
- `POST /transactions/`, `GET /transactions/`, `PUT /transactions/{id}` y `DELETE /transactions/{id}` – Gestión de transacciones.
- `POST /goals/`, `GET /goals/`, `PUT /goals/{id}`, `PATCH /goals/{id}/complete` y `DELETE /goals/{id}` – Metas de ahorro.
- `POST /categories/`, `GET /categories/`, `PUT /categories/{id}` y `DELETE /categories/{id}` – Categorías de gasto.
- `POST /budgets/`, `GET /budgets/`, `PUT /budgets/{id}` y `DELETE /budgets/{id}` – Presupuestos mensuales.
- A partir de esta versión, si un gasto supera el límite mensual configurado en un presupuesto, la transacción no se guarda y se devuelve un error.
- `GET /rewards/` – Puntos acumulados y recompensas.
- `GET /summary/monthly` y `GET /summary/category` – Resúmenes de transacciones por mes o por categoría.

Al completar una meta con `PATCH /goals/{id}/complete` se añaden a tu perfil los puntos equivalentes al monto objetivo, lo que puede desbloquear nuevas recompensas.

El endpoint `GET /transactions/` admite los parámetros opcionales `start_date` y `end_date` (en formato ISO 8601) para filtrar por rango de fechas, y `category_id` para limitar los resultados a una categoría concreta.

Todas las operaciones, excepto el registro y la obtención del token, requieren un token Bearer en la cabecera `Authorization`.

## Estructura de carpetas

```
requirements.txt        Lista de dependencias
moolah_backend/app/     Código de la aplicación FastAPI
    __init__.py
    database.py         Configuración de SQLAlchemy
    models.py           Modelos ORM
    schemas.py          Esquemas Pydantic
    crud.py             Lógica de negocio y autenticación
    dependencies.py     Dependencias comunes
    main.py             Punto de entrada de la API
    routers/            Módulos con las rutas
        auth.py
        users.py
        transactions.py
        goals.py
        categories.py
        budgets.py
        rewards.py
        analytics.py
```

## Tests

Para ejecutar la suite de pruebas instala previamente las dependencias y herramientas de desarrollo (incluye la versión fijada `bcrypt==3.2.0`):

```bash
pip install -r requirements-dev.txt
```

Luego ejecuta las pruebas con:

```bash
pytest
```

## Despliegue

### Backend

1. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

3. Define las variables de entorno necesarias:
   - `MOOLAH_SECRET_KEY` (obligatoria) para la firma de los JWT.
   - `DATABASE_URL` si quieres usar otra base de datos distinta a SQLite.

4. Inicia el servidor de la API:

   ```bash
   uvicorn moolah_backend.app.main:app --host 0.0.0.0 --port 8000
   ```

   La documentación interactiva estará disponible en `http://localhost:8000/docs`.

5. (Opcional) Pobla la base de datos con información de prueba ejecutando:

   ```bash
   python seed_db.py
   ```

Si deseas ejecutarlo en producción puedes utilizar `gunicorn` con workers de Uvicorn:

```bash
gunicorn moolah_backend.app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Asegúrate de mantener las variables de entorno configuradas y de utilizar un servidor 
frontal como Nginx para manejar HTTPS y balanceo de carga.

### Frontend Flutter

La aplicación móvil escrita en Flutter consume esta API para registrar gastos, metas y presupuestos.
Para usarla por primera vez accede a la carpeta `moolah_frontend` y descarga sus dependencias:

```bash
flutter pub get
```

Luego inicia la app en un emulador o dispositivo conectado con:

```bash
flutter run
```

La URL del backend puede configurarse con la variable de entorno `API_BASE_URL` o modificando `assets/config.json`. Si no se establece, se usará `http://localhost:8000`.

Para generar una versión de distribución puedes emplear los comandos estándar de Flutter, por ejemplo:

```bash
   flutter build apk
   ```

Consulta el archivo [moolah_frontend/README.md](moolah_frontend/README.md) para instrucciones completas.

## Contribución

Sigue estos pasos para preparar el entorno de desarrollo y validar tus cambios:

1. Instala las dependencias y herramientas de desarrollo (incluye la versión fijada `bcrypt==3.2.0`):

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Ejecuta la suite de pruebas para asegurarte de que todo funciona:

   ```bash
   pytest
   ```

3. Comprueba el estilo de código con **ruff**:

   ```bash
   ruff check .
   ```

### Troubleshooting

Si al iniciar la aplicación o ejecutar las pruebas aparece el error:

```
AttributeError: module 'bcrypt' has no attribute '__about__'
```

instala las dependencias exactas mediante:

```bash
pip install -r requirements.txt
```

La versión fijada `bcrypt==3.2.0` evita este problema. El conflicto aparece al
usar `bcrypt>=4` junto con versiones antiguas de `passlib` (como la 1.7.x
incluida en este proyecto).


## Notas

Este proyecto es un ejemplo educativo. Para usarlo en producción, considera integrar una base de datos más robusta, aplicar medidas de seguridad adicionales y manejar las migraciones adecuadamente. También se recomienda ejecutar la suite de pruebas (`pytest`) antes de desplegar cambios. El código está probado con FastAPI 0.115.14 y Pydantic 2.11.7 ó versiones posteriores.
