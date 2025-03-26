# Challenge Técnico ML

Este repositorio contiene mi resolución en Python al desafío técnico que me fue propuesto para el puesto de `Cybersecurity Engineer`

## Consideraciones particulares

- Versión de python: 3.12.6
- Decidí utilizar `ABC`s para representar la idea de una interfaz. Sé que no es necesario por tratarse de un lenguaje "levemente tipado" (tipado dinámico), pero a mi forma de ver, la utilización de dichas clases abstractas no sólo no perjudican de manera significativa la performance sino que aportan un gran nivel de semántica facilitando la comprensión de la idea detrás del código y reduciendo la necesidad de utilizar comentarios y documentación externa.
    > Nota: Si bien en algún momento del desarrollo estuvieron explícitamente definidas como hijas de `ABC`, en la versión actual por conflictos en la herencia múltiple con la clase `DeclarativeBase` de SQLAlchemy, son una clase más llevando sólo la semantica de un ABC.
- Con la intensión de implementar una solución más declarativa y por ello menos propensa a errores, decidí investigar e implementar [SQLAlchemy](https://www.sqlalchemy.org/), un popular ORM para python. 
- Decidí utilizar un mapeo de herencia de tipo _JOINED_ para la representación de la herencia existente entre `DatabaseMetadataAdapter` y sus hijos (de momento sólo `MySQLDatabaseMetadataAdapter`) ya que la idea detras de esa abstracción era permitir la fácil adaptación de este sistema a nuevos tipos de motores, que podrían, potencialmente, requerir configuraciones particulares. Debido a esto, un mapeo de herencia utilizando una estrategia _SINGLE-TABLE_ iría en contra del objetivo, ya que cada vez que se desee agregar un nuevo motor, habría que, potencialmente, modificar la estructura de la tabla `databases` lo que resultaría tedioso y más dificil de mantener. 
- Decidí utilizar un mapeo de herencia de tipo _SINGLE-TABLE_ para la representación de la herencia existente entre `Control` y sus clases "hijas" debido a que las diferentes implementaciones de `Control` tienen como objetivo establecer "lógica" específica y no así atributos. Adicionalmente, el no tener que modificar la estructura de la base de datos para agregar nuevos tipos de control facilita la mantenibilidad del sistema.
- Decidí guardar la información relevante de los controles como un atributo de la tabla `controls` para permitir la creación de nuevos controles en runtime, posibilitando incluso la creación de nuevos controles por parte de un usuario con permisos de administrador. Agregar controles de un tipo existente (Por ejemplo, `RegExOnFieldNameControl`) resulta tan simple como agregar los registros a la base de datos que definen al mismo. 
- Asumo que todos los controles se realizan a nivel campo y no a nivel tabla o esquema.
- Decidí utilizar una librería de criptografía llamada Fernet debido a su popularidad en el ámbito de SQLAlchemy. Sin embargo, debido a la implementación utilizada para cifrar los campos utilizando un [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator), la adaptación de este sistema a otros métodos criptográficos resulta trivial.

## Deudas técnicas
- Los creadores de [FastAPI sugieren](https://fastapi.tiangolo.com/tutorial/sql-databases) una forma más elegante de retornar los datos pero requiere modelar las entidades con un objeto proxy creado por ellos que se encuentra en una versión beta. Si bien tiene gran parte de la funcionalidad de SQLAlchemy, debido a la complejidad de los mapeos de herencia utilizados y a que no soporta completamente las funcionalidades de SQLAlchemy no fui capaz de adaptar fácilmente la solución al nuevo modelo. No digo que sea imposible sino que tras dedicarle aproximadamente 6hs, considero que los beneficios obtenibles de lograr dicha implementación no compensan el tiempo invertido en hacerlo. En caso de contar con tiempo adicional luego de satisfacer los demás requerimientos, retomaré la tarea de refactorizar el modelo utilizando las clases provistas por [SQLModel](https://sqlmodel.tiangolo.com/)

## Documentación

### Endpoints

> Nota: Los endpoints de encuentran documentados en mayor profundidad a través de SwaggerUI. Pueden encontrar dicha documentación dentro de la aplicación en la ruta `/docs`

|Verbo|Ruta|Descripción|Require autenticación|Requiere rol administrador|
|-|-|-|-|-|
|POST|`/api/v1/token`|Crea un nuevo JWT. Recibe usuario y clave del usuario, devuelve el token y el tipo.|:x:|:x:|
|GET|`/api/v1/users`|Retorna id, nombre y un booleano indicando si son administrador para todos los usuarios disponibles|:white_check_mark:|:white_check_mark:|
|POST|`/api/v1/users`|Crea un nuevo usuario en el sistema y retorna su informaicón. Recibe los campos `username` y `password`. **Importante: Este es el único endpoint de la API cuyo Content-Type no es JSON**. Debido a los requerimientos del estandard de OAuth2, el Content-Type de este endpoint es **application/x-www-form-urlencoded**|:white_check_mark:|:white_check_mark:|
|GET|`/api/v1/tags`|Retorna id, nombre y descripción de todos los DataType tags disponibles|:white_check_mark:|:white_check_mark:|
|POST|`/api/v1/tags`|Crea un nuevo DataType tag y retorna su id|:white_check_mark:|:white_check_mark:|
|GET|`/api/v1/controls`|Retorna id, nombre, tipo y raw_data de todos los controles disponibles|:white_check_mark:|:white_check_mark:|
|POST|`/api/v1/controls/regexOnFieldName`|Crea un nuevo control de tipo `RegexOnFieldNameControl`y retorna su id|:white_check_mark:|:white_check_mark:|
|GET|`/api/v1/databases`|Retorna id y nombre de todas las bases de datos disponibles para escanear|:white_check_mark:|:x:|
|POST|`/api/v1/databases/mysql`|Agrega una nueva base de datos de tipo MySQL a las disponibles para escanear|:white_check_mark:|:x:|
|POST|`/api/v1/databases/{id}/scans`|Escanea la base de datos con el id indicado. Devuelve el id del escaneo|:white_check_mark:|:x:|
|GET|`/api/v1/databases/{id}/scans`|Obtiene el listado de resultados de escaneo disponibles para la base de datos con el id indicado. No devuelve los resultados, sólo sus id y fecha de escaneo|:white_check_mark:|:x:|
|GET|`/api/v1/databases/{id}/scans/last`|Obtiene los resultados del último escaneo de la base de datos con el id indicado|:white_check_mark:|:x:|
|GET|`/api/v1/databases/scans/{id}`|Obtiene los resultados del escaneo con el id indicado|:white_check_mark:|:x:|

### Variables de entorno
- `DATABASE_ENCRYPTION_KEY`: Debe ser generada utilizando un string aleatorio de 32 bytes encodeado con `URL-Safe Base64`
- `DATABASE_USER`: Nombre de usuario para la conexión con la base de datos que guardará la información del sistema
- `DATABASE_PASSWORD`: Clave para el usuario especificado en `DATABASE_USER`
- `DATABASE_HOST`: IP o [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) de la base de datos que gruardará la información del sistema 
- `DATABASE_PORT`: Puerto de la base de datos que guardará la información del sistema
- `DATABASE_NAME`: Nombre de la base de datos que guardará la información del sistema
- `JWT_SECRET`: String aleatorio para la creación de tokens. Se recomienda una longitud mínima de 64 caracteres aleatorios.
- `JWT_ALGORITHM`: Algoritmo a utilizar en el JWT. Se recomienda `HS256`
- `JWT_EXPIRATION_MINUTES`: Duración en minutos del `JWT` una vez emitido

### Diagrama de clases UML

#### Versión simplificada
> Nota: Debido a la candidad de relaciones de uso existentes entre los objetos y con la intención de facilitar la comprensión de la idea detrás del modelo, decidí generar una versión simplificada del modelo de objetos contemplando sólo las relaciones de pertenencia y composición más importantes. 

![Diagrama de clases UML - Simplificado](/documentation/Diagrama%20de%20clases%20UML%20-%20Simplificado.svg)

#### Versión completa
![Diagrama de clases UML](/documentation/Diagrama%20de%20clases%20UML.svg)
> Nota: El diagrama de clases sólo incluye las clases que son relevantes para la comprensión del diseño. Las clases auxiliares para la persistencia como la clase `Base` y los atributos cuyo único fin es la persistencia fueron excluidos del diagrama con la intención de reducir el ruido y facilitar el entendimiento de los aspectos más importantes. También fueron excluidos del diagrama de clases los modelos de Pydantic utilizados para formatear la información devuelta al cliente HTTP.

### Diagrama entidad relación (DER)
![DER](/documentation/DER.png)