# Challenge Técnico ML

Este repositorio contiene mi resolución en Python al desafío técnico que me fue propuesto para el puesto de `Cybersecurity Engineer`

## Consideraciones particulares

- Versión de python: 3.12.6
- Decidí utilizar `ABC`s para representar la idea de una interfaz (Si bien en algún momento del desarrollo estuvieron explícitamente definidas en la versión actual son una clase más por conflictos en la herencia múltiple con la clase `Base` de SQLAlchemy). Sé que no es necesario por tratarse de un lenguaje "levemente tipado" (tipado dinámico), pero a mi forma de ver, la utilización de dichas clases abstractas no sólo no perjudican de manera significativa la performance sino que aportan un gran nivel de semántica facilitando la comprensión de la idea detrás del código y reduciendo la necesidad de utilizar comentarios y documentación externa.
- Con la intensión de implementar una solución más declarativa y por ello menos propensa a errores, decidí investigar e implementar [SQLAlchemy](https://www.sqlalchemy.org/), un popular ORM para python. 
- Decidí utilizar un mapeo de herencia de tipo _JOINED_ para la representación de la herencia existente entre `DatabaseMetadataAdapter` y sus hijos (de momento sólo `MySQLDatabaseMetadataAdapter`) ya que la idea detras de esa abstracción era permitir la fácil adaptación de este sistema a nuevos tipos de motores, que podrían, potencialmente, requerir configuraciones particulares. Debido a esto, un mapeo de herencia utilizando una estrategia _SINGLE-TABLE_ iría en contra del objetivo, ya que cada vez que se desee agregar un nuevo motor, habría que, potencialmente, modificar la estructura de la tabla `databases` lo que resultaría tedioso y más dificil de mantener. 
- Decidí utilizar un mapeo de herencia de tipo _SINGLE-TABLE_ para la representación de la herencia existente entre `Control` y sus clases "hijas" debido a que las diferentes implementaciones de `Control` tienen como objetivo establecer "lógica" específica y no así atributos. Adicionalmente, el no tener que modificar la estructura de la base de datos para agregar nuevos tipos de control facilita la mantenibilidad del sistema.
- Decidí guardar la información relevante de los controles como un atributo de la tabla `controls` para permitir la creación de nuevos controles en runtime, posibilitando incluso la creación de nuevos controles por parte de un usuario con permisos de administrador. Agregar controles de un tipo existente (Por ejemplo, `RegExOnFieldNameControl`) resulta tan simple como agregar los registros a la base de datos que definen al mismo. 
- Asumo que todos los controles se realizan a nivel campo y no a nivel tabla o esquema.
- Decidí utilizar una librería de criptografía llamada Fernet debido a su popularidad en el ámbito de SQLAlchemy. Sin embargo, debido a la implementación utilizada para cifrar los campos utilizando un [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator), la adaptación de este sistema a otros métodos criptográficos resulta trivial.

## Documentación

### Variables de entorno requeridas

- DATABASE_ENCRYPTION_KEY: Debe ser un string de 32 bytes encodeado utilizando el formato UrlSafe-Base64

### Diagrama de clases UML
![Diagrama de clases UML](/documentation/Diagrama%20de%20clases%20UML.svg)
> Nota: El diagrama de clases sólo incluye las clases que son relevantes para la comprensión del diseño. Las clases auxiliares para la persistencia como la clase `Base` y los atributos cuyo único fin es la persistencia fueron excluidos del diagrama con la intención de reducir el ruido y facilitar el entendimiento de los aspectos más importantes. 

### Diagrama entidad relación (DER)
![DER](/documentation/DER.png)