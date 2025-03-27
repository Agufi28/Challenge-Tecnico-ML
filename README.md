# Challenge Técnico ML

Este repositorio contiene mi resolución en Python al desafío técnico que me fue propuesto para el puesto de `Cybersecurity Engineer`

## Deploy

Este repositorio compila automáticamente una imagen de docker ubicada en ghcr.io.

Ejemplo de Docker compose:

```yml
version: "2.2"

services:
  db:
    container_name: challengeml_db
    image: mysql:8.0.26
    command: --sql_mode="NO_ENGINE_SUBSTITUTION" --default-authentication-plugin=mysql_native_password --max-allowed-packet=67108864

    environment:
      - MYSQL_ROOT_PASSWORD=reallyPleaseChangeMe!
      - MYSQL_USER=appUser
      - MYSQL_PASSWORD=changeMe!!
      - MYSQL_DATABASE=challengeml
      - TZ=America/Buenos_Aires
    cap_add:
      - SYS_NICE
    restart: unless-stopped
    ports:
      - 1000:3306

  app:
    container_name: challengeml_api_python
    image: ghcr.io/agufi28/challenge-tecnico-ml:v1.0.0-python
    environment:
      - DATABASE_ENCRYPTION_KEY=NjAxMTc5NjA4MzQ3NzMwNjc3NTk1MDY5ODk1NTkzNjk=
      - DATABASE_USER=root
      - DATABASE_PASSWORD=reallyPleaseChangeMe!
      - DATABASE_HOST=db
      - DATABASE_PORT=3306
      - DATABASE_NAME=challengeml
    restart: unless-stopped
    ports:
      - 1001:80 #You should probably change the out port(1001) to one you like
```


## Documentación - Consideraciones particulares

### Sobre las dependencias
- Versión de python: 3.12.6
- Con la intensión de implementar una solución más declarativa y por ello menos propensa a errores, decidí investigar e implementar [SQLAlchemy](https://www.sqlalchemy.org/), un popular ORM para python. De esta forma se reducen las probabilidades tanto de que el sistema resulte vulnerable a [SQLi](https://owasp.org/www-community/attacks/SQL_Injection) como los errores accidentales derivados de armar consultas SQL manualmente que quedan hardcodeadas en el código carentes de una validación sintáctica por parte del IDE, y eso sin considerar las validaciones semánticas.
- Decidí utilizar una librería de criptografía llamada Fernet debido a su popularidad en el ámbito de SQLAlchemy. Sin embargo, debido a la implementación utilizada para cifrar los campos basada en un [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator), la adaptación de este sistema a otros métodos criptográficos resulta trivial.
- Decidí utilizar una librería de `logging` llamada [Loguru](https://loguru.readthedocs.io/en/stable/) debido a su simpleza y amplio soporte por parte de la comunidad de Python. Provee soporte extensible para diversas estrategias de logueo incluyendo, entre otras, logueo hacia `stdout`, `stderror` y archivos; teniendo incluso para estos últimos mecanismos de rotación ya incorporados.

### Sobre el modelo de objetos
#### General
- Decidí utilizar [`ABC`](https://docs.python.org/3/library/abc.html)s para representar la idea de una interfaz. Sé que no es necesario por tratarse de un lenguaje "levemente tipado" (tipado dinámico), pero a mi forma de ver, la utilización de dichas clases abstractas no sólo no perjudican de manera significativa la performance sino que aportan un gran nivel de semántica facilitando la comprensión de la idea detrás del código y reduciendo la necesidad de utilizar comentarios y documentación externa.
    > Nota: Si bien en algún momento del desarrollo estuvieron explícitamente definidas como hijas de `ABC`, en la versión actual por conflictos en la herencia múltiple con la clase `DeclarativeBase` de SQLAlchemy, son una clase más llevando sólo la semantica de un ABC.
- Soy consciente de la existencia de una mezcla en los criterios de nombre para las variables. Fue resultado de haber tomado la decisión de mantener la estructura de la base de datos consistentemente en `snake_case`. Por ello, los atributos de los modelos que representan directamente campos de la base de datos se encuentran en ese formato, mientras que el resto del proyecto está desarrollado en `camelCase`

#### Bases de datos

Con la intención de poder soportar fácilmente bases de datos a escanear de diferentes motores, decidí que el sistema sea mayormente agnóstico al tipo de base de datos (MySQL, Postgresql, MSSQL, etc.) que se está escaneando. Para ello, tomando inspiración del [patrón adapter](https://es.wikipedia.org/wiki/Adaptador_(patr%C3%B3n_de_dise%C3%B1o)), decidí abstraer la idea de una base de datos a un ABC llamado `DatabaseMetadataAdapter` siendo este quien actúe de "interfaz" y me permita tratar polimórficamente todas las bases de datos, independiente de su tipo. 

![Diagrama relacion entre DatabaseMetadataAdapter e hijos](/documentation/Diagrama%20de%20relacion%20entre%20DatabaseMetadataAdapter%20y%20sus%20hijos.svg)

Para ello, la clase `DatabaseMetadataAdapter` define dos métodos abstractos que deben ser implementados por el "adaptador" de cada **tipo de base de datos**. Los métodos a implementar por parte de las clases hijas son `scanStructure` y `fetchSamples` y cuyas firmas son las siguientes:
```py
def scanStructure(self, requestedBy: User=None, dataSampleSize=0) -> ScanResult:
    pass

def fetchSamples(self,  dataSampleSize:str, structure:list[DatabaseSchema], cursor) -> None:
    pass
```

Como su nombre lo indica, el método `scanStructure` es responsable de realizar las consultas necesarias a la base de datos cliente para obtener la información de su estructura. Debe obtener información sobre:
- Los esquemas existentes en la base de datos
- Las tablas contenidas en cada uno de los esquemas encontrados
- Los campos pertenecientes a cada una de las tablas encontradas
- El tipo de dato de cada campo encontrado

Para estandarizar los tipos de datos y permitir que los controles sean completamente agnósticos al motor, decidí crear el siguiente enum:
```py
class FieldDataTypes(Enum):
    STRING = 1
    INTEGER = 2
    DECIMAL = 3
    BOOLEAN = 4
    BINARY = 5
    TIME = 6
    DATE = 7
    DATETIME = 8
```

Cada clase adaptador es responsable adicionalmente de convertir el tipo de dato particular del campo al valor de `FieldDataTypes` que más se le aproxime. 

> Nota: Se que esta implementación tiene falencias, pero tras evaluar pros y contras, consideré que la ventaja de poder generalizar los tipos de datos y que los controles se ejecuten sin depender en forma alguna del motor que tuviera la base de datos escaneada superaba la desventaja de tener que excepcionalmente modificar el código para contemplar nuevos tipos de dato primitivos. 

Como parte de este POC desarrollé sólo un adaptador para MySQL, pero debido a las abstracciones antes mencionadas debería resultar relativamente simple extender este sistema a cualquier otro motor que se base en una estructura de `esquema→tabla→campos`

Finalmente, el método `fetchSamples` es responsable de obtener, para cada campo detectado, una muestra aleatoria de `dataSampleSize` datos. Siendo las consultas necesarias para lograr dicho objetivo responsabilidad de cada una de las implementaciones de `DatabaseMetadataAdapter`

> Nota: En caso de existir menos registros en la base de dato que muestras solicitadas, se deberán obtener todos los registros existentes.

Por una cuestión de seguridad, los datos obtenidos en el muestreo **no son persistidos** como parte del resultado. Sólo existen en memoria hasta que los controles finalizan, luego son eliminados. De esta forma se preserva la **confidencialidad** de los mismos.

#### Controles

Decidí abstraer la idea de un control a un ABC llamado `Control`. Esta clase lleva toda la estructura básica de un control excepto su lógia de detección. Es decir, guarda toda la información necesaria para ejecutar el control y posee todos los métodos para interactuar con el resto de la aplicación, con la exepción de un método privado que define si el campo que está siendo escaneado coincide con lo que el control está buscando. La implementación de este método es responsabilidad de las clases hijas que serán las encargadas de definir los **tipos de control** existentes en el sistema.

![Diagrama UML Control e hijos](/documentation/Diagrama%20de%20relacion%20entre%20Control%20y%20sus%20hijos.svg)
> Nota: En la imagen de ejemplo, los **tipos de control** existentes serían `RegExOnFieldNameControl` y `RegExOnSampledDataControl`

La firma del método privado que deben definir con la lógica de detección particular de cada tipo de control es la siguiente
```py
    def __conditionMatches(self, field: DatabaseField) -> bool:
        pass
```

Con la intención de proveer la mayor flexibilidad posible a quienes deseen extender de `Control` implementando nuevos tipos de validaciones, **toda la información necesaria para que el control ejecute es almacenada en formato `JSON` dentro del campo `raw_data`**. Debido a esto, la clase padre `Control` provee adicionalmente un método para obtener dicha información en un objeto de tipo `dict[str, Any]`
```py
    def getData(self) -> dict[str, Any]:
        return json.loads(self.raw_data)
```

Gracias a estas dos decisiones, **es posible crear nuevos controles en runtime**. Agregar controles de un tipo existente (Por ejemplo, `RegExOnFieldNameControl`) resulta tan simple como agregar los registros a la base de datos que definen al mismo y será automágicamente contemplado por los futuros escaneos. 

> Nota: Esto sólo aplica para **tipos de control preexistentes**. En principio no es posible agregar nuevos **tipos de control** en runtime ya que esto requiere la creación de nuevas clases dentro del sistema.

##### Controles sobre los datos

Como se menciona en el apartado sobre [Bases de datos](#bases-de-datos), el proceso de escaneo contempla la obtención de una muestra de datos para cada campo detectado. De esta forma es posible realizar controles no sólo sobre la información del campo como su nombre o tipo sino también sobre pequeñas muestras de la información contenida en ellos. 

Para acceder a estas muestras desde un control, se debe utilizar el atributo `dataSample` del campo o en su defecto, si se desea ignorar los valores nulos, el método `getDataSampleWithoutNones()`.

```py
    def _Control__conditionMatches(self, field: DatabaseField):
        # Así podemos validar el tipo de dato genérico contenido en el campo
        if field.type != FieldDataTypes.STRING:
            return False
        
        # Así podemos obtener todos los puntos de datos muestreados
        allSampledData = field.dataSample

        # Así podemos obtener los puntos de datos muestreados que no sean nulos
        sampledDataWithoutNulls = field.getDataSampleWithoutNones()
```

#### Otros posibles tipos de control

Mientras desarrollaba el sistema, contemple implementar otros tipos de controles que me resultaron interesantes. Sin embargo, los descarté por cuestiones de tiempo. Algunos de los controles que pensé son:

- Verificar los datos muestreados del campo contra un diccionario de nombres típicos de la región donde se ejecuta el sistema
- Verificar los datos muestreados del campo contra una API externa que me indique si se trata, por ejemplo, de una tarjeta de crédito
- Verificar los campos de tipo numérico se encuentren en un rango específico, por ejemplo, para identificar números de DNI
- Verificar los datos muestreados del campo utilizando una aplicación de consola como [`hash-identifier`](https://www.kali.org/tools/hash-identifier/) para detectar algoritmos vulnerables u obsoletos


### Sobre el mecanismo de detección

Debido a que el sistema fue pensado para ejecutar múltiples controles diferentes sobre la estructura de la base de datos y a que éstos pueden no estar de acuerdo en el tipo de dato asociado a los campos escaneados, tomé la decisión de utilizar un sistema de etiquetado con peso. 

Cada control tiene asociadas una o varias etiquetas(`tags`) con un peso a cada una. Por ejemplo, si el control se basa en buscar el string "name" en el nombre del campo, podría tener asociadas las siguientes etiquetas:

|Etiqueta|Peso|
|-|-|
|`USERNAME`|20|
|`NAME`|80|
|`LAST_NAME`|20|
|`FIRST_NAME`|20|

En caso de que el control "matchee" en un campo determinado, le agregará todas sus etiquedas asociadas con sus respectivos pesos. En caso de que alguna etiqueta ya estuviera presente en el campo, sólo le sumará el peso aportado por el control actual para dicha etiqueta. 

Por ejemplo, si tuviera un campo `username` que ya se encuentra cuenta con la etiqueta `USERNAME(80)`, tras ejecutarse este control el campo pasaría a estar etiquetado con los siguientes pesos:

Campo: "username"
|Etiqueta|Peso|
|-|-|
|`USERNAME`|100|
|`NAME`|80|
|`LAST_NAME`|20|
|`FIRST_NAME`|20|

Nótese que el peso de "username" ya no es los 80 puntos que tenía antes, ni los 20 que provee el control actual, sinó 100. Que resulta de la suma entre el peso con el que entró al control y el valor aportado por el mismo. 

> Nota: Si bien la estructura soporta pesos negativos, es decir, la posibilidad de que un control determine que un campo "no es algo", personalmente recomiendo tener especial cuidado con esta práctica ya que podría resultar en datos poco intuitivos o difíciles de interpretar. 

### Sobre el mapeo Objetos-Relacional
- Decidí utilizar un mapeo de herencia de tipo _JOINED_ para la representación de la herencia existente entre `DatabaseMetadataAdapter` y sus hijos (de momento sólo `MySQLDatabaseMetadataAdapter`) ya que la idea detras de esa abstracción era permitir la fácil adaptación de este sistema a nuevos tipos de motores, que podrían, potencialmente, requerir configuraciones particulares. Debido a esto, un mapeo de herencia utilizando una estrategia _SINGLE-TABLE_ iría en contra del objetivo, ya que cada vez que se desee agregar un nuevo motor, habría que, potencialmente, modificar la estructura de la tabla `databases` lo que resultaría tedioso y más dificil de mantener. 
- Decidí utilizar un mapeo de herencia de tipo _SINGLE-TABLE_ para la representación de la herencia existente entre `Control` y sus clases "hijas" debido a que las diferentes implementaciones de `Control` tienen como objetivo establecer "lógica" específica y no así atributos. Adicionalmente, el no tener que modificar la estructura de la base de datos para agregar nuevos tipos de control facilita la mantenibilidad del sistema.

### Asunciones
- Asumo que todos los controles se realizan a nivel campo y no a nivel tabla o esquema.
- Asumo que es de interés poder obtener los resultados de escaneos pasados
- Asumo que es de interés dejar el sistema abierto a nuevos tipos de bases de datos

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
|POST|`/api/v1/controls/regExOnSampledDataControl`|Crea un nuevo control de tipo `RegExOnSampledDataControl`y retorna su id|:white_check_mark:|:white_check_mark:|
|GET|`/api/v1/databases`|Retorna id y nombre de todas las bases de datos disponibles para escanear|:white_check_mark:|:x:|
|POST|`/api/v1/databases/mysql`|Agrega una nueva base de datos de tipo MySQL a las disponibles para escanear|:white_check_mark:|:x:|
|POST|`/api/v1/databases/{id}/scans`|Escanea la base de datos con el id indicado. Devuelve el id del escaneo|:white_check_mark:|:x:|
|GET|`/api/v1/databases/{id}/scans`|Obtiene el listado de resultados de escaneo disponibles para la base de datos con el id indicado. No devuelve los resultados, sólo sus id y fecha de escaneo|:white_check_mark:|:x:|
|GET|`/api/v1/databases/{id}/scans/last`|Obtiene los resultados del último escaneo de la base de datos con el id indicado|:white_check_mark:|:x:|
|GET|`/api/v1/databases/scans/{id}`|Obtiene los resultados del escaneo con el id indicado|:white_check_mark:|:x:|

#### Justificación sobre modificaciones en la API

- Con el objetivo de cumplir con el requerimiento adicional de Autenticación y Autorización decidí agregar el endpoint `POST /api/v1/token` que recibe `username` y `password` y en caso de ser correctos, devuelve un [JWT](https://datatracker.ietf.org/doc/html/rfc7519). El tiempo de expiración del mismo es configurable a través de la variable de entorno `JWT_EXPIRATION_MINUTES`.
    > Nota: Debido a la decisión de respetar el estandar de OAuth2 para la autenticación, este endpoint es el único que recibe sus parametros en formato **application/x-www-form-urlencoded**.
- Como les comenté por email y en pos de poder soportar múltiples motores de base de datos decidí modificar el endpoint de alta de una nueva base de datos de `POST /api/v1/database` a `POST /api/v1/databases/{tipo}`. Siendo la única implementación existente en el POC `POST /api/v1/databases/mysql`.
- Con la intención de mantenerme lo más cercano posible a una arquitectura REST decidí renombrar el endpoint `POST /api/v1/database/scan/{id}` a `POST /api/v1/database/{id}/scan`

Debido a la decisción de diseño tomada sobre mantener el registro de todos los escaneos realizados sobre una base de datos debí realizar las siguientes modificaciones:
- `GET /api/v1/database/{id}/scan` ya no tiene sentido porque potencialmente existen múltiples escaneos asociados a una base de datos. Por ello, para preservar el objetivo de poder obtener el último escaneo realizado decidí agregar el endpoint `GET /api/v1/databases/{id}/scans/last`. El mismo devolverá los resultados del último escaneo o un mensaje de error en caso que aún no se haya realizado ninguno sobre esa base de datos.
- Agregué el endpoint `GET /api/v1/databases/{id}/scans` para obtener información sobre los escaneos realizandos a una base de datos determinada.
>Nota: Por una cuestión de performance, este endpoint sólo devuelve información sobre los escaneos, no así sus respectivos resultados
- Agregué el endpoint `GET /api/v1/databases/scans/{id}` para poder obtener información sobre los resultados de cualquier escaneo conociendo su `id`. 

Adicionalmente, con la intención de brindar completitud a la API, decidí agregar para los usuarios de tipo **administrador** los siguientes endpoints de administración:
- `GET /api/v1/users`: Para obtener información sobre los usuarios existentes en el sistema
- `POST /api/v1/users`: Para agregar nuevos usuarios al sistema, tanto administradores como usuarios "normales"
- `GET /api/v1/tags`: Para obtener información sobre los `DataTypeTags` existentes en el sistema
- `POST /api/v1/tags`: Para agregar nuevos `DataTypeTags` al sistema
- `GET /api/v1/controls`: Para obtener información sobre los controles existentes
- `POST /api/v1/controls/regexOnFieldName`: Para crear nuevos controles de tipo `RegexOnFieldNameControl`. Como recordatorio, estos son los que se basan en evaluar una RegEx sobre el nombre de los campos. 
- `POST /api/v1/controls/regExOnSampledDataControl`: Para crear nuevos controles de tipo `RegExOnSampledDataControl`. Como recordatorio, estos son los que se basan en evaluar una RegEx sobre los datos muestreados del campo. 

    Finalmente, decidí agregar para todos los usuarios el endpoint `GET /api/v1/databases` para obtener información básica sobre las bases de datos existentes en el sistema sobre las cuales se pueden ejecutar los escaneos.

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


## Documentación - Diagramas

### Diagrama de clases UML

#### Versión simplificada
> Nota: Debido a la candidad de relaciones de uso existentes entre los objetos y con la intención de facilitar la comprensión de la idea detrás del modelo, decidí generar una versión simplificada del modelo de objetos contemplando sólo las relaciones de pertenencia y composición más importantes. También se excluyó de este modelo la clase User ya que sólo resulta relevante a fines de Autenticación, Autorización y Trazabilidad, que si bien son funcionalidades importantes, no constituyen el objetivo central de este sistema.

![Diagrama de clases UML - Simplificado](/documentation/Diagrama%20de%20clases%20UML%20-%20Simplificado.svg)

#### Versión completa
![Diagrama de clases UML](/documentation/Diagrama%20de%20clases%20UML.svg)
> Nota: El diagrama de clases sólo incluye las clases que son relevantes para la comprensión del diseño. Las clases auxiliares para la persistencia como la clase `Base` y los atributos cuyo único fin es la persistencia fueron excluidos del diagrama con la intención de reducir el ruido y facilitar el entendimiento de los aspectos más importantes. También fueron excluidos del diagrama de clases los modelos de Pydantic utilizados para formatear la información devuelta al cliente HTTP.

### Diagrama entidad relación (DER)
![DER](/documentation/DER.png)

### Diagrama de secuencia al realizar un escaneo

 Debido a la complejidad asociada al proceso de escaneo, consideré oportuno incluir como parte de la documentación un diagrama de secuencia que exclique la interacción entre los diferentes modelos al recibir una solicitud de escaneo por parte del usuario.

![Diagrama de secuencias al escanear](/documentation/Diagrama%20de%20secuencia%20al%20ejecutar%20un%20escaneo.svg)

## Documentacion - FrontEnd

Dado que el FrontEnd era secundario en este caso y a que mis habilidades más fuertes se encuentran en el back, decidí utilizar librerías que me ayuden a llegar a una versión no tan horrible de la GUI. 

En particular, para desarrollar el Front-End utilicé:
- [Boostrap](https://getbootstrap.com/) para armar las tablas, modals y botones
- [SweetAlert2](https://sweetalert2.github.io/) para armar los pup up indicando mensajes de error o exito
- [jQuery](https://jquery.com/) para interactuar con la API y obtener/enviar la información necesaria en cada caso


## Deudas técnicas
- Los creadores de [FastAPI sugieren](https://fastapi.tiangolo.com/tutorial/sql-databases) una forma más elegante de retornar los datos pero requiere modelar las entidades con un objeto proxy creado por ellos que se encuentra en una versión beta. Si bien tiene gran parte de la funcionalidad de SQLAlchemy, debido a la complejidad de los mapeos de herencia utilizados y a que no soporta completamente las funcionalidades de SQLAlchemy no fui capaz de adaptar fácilmente la solución al nuevo modelo. No digo que sea imposible sino que tras dedicarle aproximadamente 6hs, considero que los beneficios obtenibles de lograr dicha implementación no compensan el tiempo invertido en hacerlo. En caso de contar con tiempo adicional luego de satisfacer los demás requerimientos, retomaré la tarea de refactorizar el modelo utilizando las clases provistas por [SQLModel](https://sqlmodel.tiangolo.com/)
- Testeos exhaustivos: Debido a las complejidades inherentes a que la mayoría de las entidades estén atadas a información provista por la base de datos y a que me concentré en desarrollar una API lo más completa y flexible posible y a documentar lo mejor que pude con la intención de hacerles llegar mi idea detrás del modelo desarrollado, no hice a tiempo de testear el proyecto de forma exhaustiva. Soy consciente de que esto no es una buena práctia y es por eso que lo estoy agregando como deuda técnica. Testee lo más que pude, pero sé que fué poco.
- Loggin exhaustivo: Si bien la aplicación loguea todas las acciones realizadas por los usuarios y muchos de las excepciones intenamente lanzadas, no está todo contemplado. Sería necesario realizar una refactorización del código agregando loggeos de tipo `info`, `debug` y `error` dentro del modelo de objetos según corresponda.
- Por motivos de trazabilidad y no repudio decidí registrar el usuario que realizó cada operación de creación (POST). Sin embargo, por conflictos con las relaciones recursivas en SQLAlchemy no fui capaz de implementar este control para el caso de `POST /api/v1/users`. Queda pendiente buscar algún mecanismo para solventar la incompatibilidad de SQLAlchemy con este tipo de relaciones.
- Definir y enforzar una política de contraseñas para los usuarios. Ej. Mínimo 8 caracteres, mayúsculas, minúsculas, símbolos, etc.
- Debido al limitado tiempo, la GUI sólo contempla las operaciones básicas permitidas por la API. Queda pendiente implementar las demás. Las operaciones actualmente contempladas son:
    - Listar las bases de datos existentes
    - Solicitar el escaneo a una de las bases de datos listadas
    - Ver los resultados del último escaneo realizado a alguna de las bases de datos listadas con sus correspondientes esquemas, tablas, campos y lo más importante, las etiquetas (tags) asignadas a cada campo con su respectivo peso


## Estructura de la base de datos

Como parte del script que genera la estructura de la base de datos para utilizar la aplicación decidí incluir registros de prueba para que la base de datos sea inicializada con información básica

### Usuarios de prueba

|Id|Usuario|Clave|Admin|
|-|-|-|-|
|1|`testAdmin`|`adminPassword`|:white_check_mark:|
|2|`testUser`|`userPassword`|:x:|

### Controles de prueba
|Id|Name|Type|Regex|
|-|-|-|-|
|1|Check for the literal string username|RegExOnFieldName|`username\|USERNAME`|
|2|Search for the string user|RegExOnFieldName|`.*(user\|USER).*`|
|3|Search for the string name|RegExOnFieldName|`.*(name\|NAME).*`|
|4|Search for common ways of reffering to the last_name|RegExOnFieldName|`(last\|LAST\|SUR\|sur)(_\|-)?(name\|NAME)`|
|5|Search for common ways of reffering to the first_name|RegExOnFieldName|`(first\|FIRST)(_\|-)?(name\|NAME)`|
|6|Search for various ways of naming an email field|RegExOnFieldName|`(first\|FIRST)(_\|-)?(name\|NAME)`|
|7|Search for various any pattern containing combinations of credit and card|RegExOnFieldName|`.*(CREDIT\|credit)(_\|-)?(CARD\|card).*`|
|8|Email address pattern|RegExOnSampledData|`[^@]+@[^@]+\.[^@]+`|

### Archivos de generación

[**Script para la creación de la BD principal**](/sql/database_creation.sql)

[**Script para la creación de la BD de pruebas**](/sql/test_database_creation.sql)