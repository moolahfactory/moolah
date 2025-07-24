# Moolah Frontend

Aplicación móvil en Flutter que integra las funciones de **Moolah** con la API de WhatsApp Business. Permite manejar tus finanzas y comunicarte con tus usuarios a través de WhatsApp.

## Configuración

1. Instala [Flutter](https://docs.flutter.dev/get-started/install) y asegúrate de que esté en el `PATH`.
2. Verifica que tienes la **Android SDK Platform 34** y se recomienda **JDK 17** (evita JDK 21/22 ya que genera errores de D8).
3. Si no existe la carpeta `android/`, créala con:
   ```bash
   flutter create .
   ```

## Ejecución

Dentro de esta carpeta ejecuta:

```bash
flutter pub get
flutter run
```

### Variables de entorno

- `API_BASE_URL`: URL base de la API de WhatsApp. Si no se establece, se usa `https://graph.facebook.com/v18.0`. También puedes definirla en `assets/config.json` mediante la clave `apiBaseUrl`.
- `BACKEND_BASE_URL`: URL del backend de Moolah para iniciar sesión y obtener los datos financieros. Se puede definir en `assets/config.json` con `backendBaseUrl`.
- `PHONE_NUMBER_ID`: Identificador de tu número de empresa en WhatsApp Business. Puede establecerse como variable de entorno o en `assets/config.json` a través de `phoneNumberId`.

### Autenticación con el backend

La aplicación se autentica contra `moolah_backend` enviando las credenciales del usuario al endpoint `/token`. El servicio `ApiService` guarda el *access token* JWT en `FlutterSecureStorage` y lo envía en la cabecera `Authorization` de las peticiones posteriores.

## Pantallas y funcionalidades

- **Inicio de sesión y registro** para autenticarte en el backend.
- **Inicio** con accesos rápidos a todas las secciones de finanzas.
- **Transacciones** permite registrar gastos o ingresos y filtrarlos por fecha y categoría.
- **Metas de ahorro** muestra tus objetivos y te otorga puntos al completarlos.
- **Presupuestos y categorías** gestionan tus límites de gasto mensuales y las categorías asociadas.
- **Recompensas** consulta tus puntos acumulados y canjéalos.
- **Análisis** ofrece resúmenes mensuales y por categoría.
- **Perfil** gestiona la información básica del usuario.
- **Integración con WhatsApp** lista tus chats y permite enviar mensajes mediante la API de WhatsApp Business.

