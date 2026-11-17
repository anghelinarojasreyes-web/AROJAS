# EcoTech Solutions

**Asignatura:** Programación Orientada a Objetos Seguro  
**Estudiante:** Anghelina Rojas

## 1.Descripción del proyecto

EcoTech Solutions es un programa hecho en Python para administrar empleados, gerentes, departamentos y proyectos,también permite registrar las horas que trabajan los empleados.

Para guardar los datos usamos SQLite y organizamos el código en modelos, vistas y controladores

## 2.Funciones del programa

El programa tiene distintas opciones según el tipo de usuario que ingrese

- Registrar empleados, gerentes y administradores.
- Administrar departamentos y proyectos.
- Registrar las horas trabajadas.
- Iniciar sesión con correo y contraseña.
- Consultar el clima de ciudades de Chile.

## 3.API del clima

Agregamos una opción para consultar el clima usando Open-Meteo, el programa se conecta a la API con `urllib` y recibe los datos en formato JSON, de ahí sacamos la temperatura, humedad, estado del tiempo y velocidad del viento

## 4.Seguridad

Las contraseñas no se guardan tal como las escribe el usuario, sino que se protegen usando PBKDF2 y SHA-256, también agregamos validaciones para los correos y contraseñas. Si alguien se equivoca tres veces al iniciar sesión, ese correo queda bloqueado durante 30 segundos

Cada usuario puede acceder a distintas funciones dependiendo de su rol

## 5.Manejo de errores

Usamos `try/except` para controlar errores del programa. Por ejemplo, si falla Internet o la API no responde, aparece un mensaje en vez de que el programa se cierre, también revisamos los errores HTTP y los datos que ingresa el usuario

## 6.Uso de IA

Usé ChatGPT para ayudarme con algunas partes del proyecto, principalmente para revisar errores y mejorar la seguridad.

Le pregunté cómo proteger las contraseñas, limitar los intentos de inicio de sesión y controlar los errores de la API, también lo utilicé para revisar el problema de los correos repetidos en la base de datos y con esa ayuda fui haciendo cambios en el código y probando que las funciones siguieran funcionando

## 7.Tecnologías utilizadas

- Python
- SQLite
- Visual Studio Code
- Open-Meteo
- GitHub
- ChatGPT

## 8.Conclusión

Con este trabajo pude practicar lo visto en clases, como el uso de clases, bases de datos, conexión con una API y seguridad para iniciar sesión, igual aprendí a revisar errores y hacer cambios en el código para mejorar el funcionamiento del programa