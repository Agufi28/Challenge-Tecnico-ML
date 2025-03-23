# Challenge Técnico ML

Este repositorio contiene mi resolución en Python al desafío técnico que me fue propuesto para el puesto de `Cybersecurity Engineer`

## Consideraciones particulares

- Versión de python: 3.12.6
- Decidí utilizar `ABC`s para representar la idea de una interfaz. Sé que no es necesario por tratarse de un lenguaje "levemente tipado" (tipado dinámico), pero a mi forma de ver, la utilización de dichas clases abstractas no sólo no perjudican de manera significativa la performance sino que aportan un gran nivel de semántica facilitando la comprensión de la idea detrás del código y reduciendo la necesidad de utilizar comentarios y documentación externa.
- Con la intensión de implementar una solución más declarativa y por ello menos propensa a errores, decidí investigar e implementar [SQLAlchemy](https://www.sqlalchemy.org/), un popular ORM para python. 

## Documentación

### Diagrama de clases UML
![Diagrama de clases UML](/documentation/ChallengeTecnicoML.svg)
> Nota: El diagrama de clases sólo incluye las clases que son relevantes para la comprensión del diseño. Las clases auxiliares para la persistencia como la clase `Base` y los atributos cuyo único fin es la persistencia fueron excluidos del diagrama con la intención de reducir el ruido y facilitar el entendimiento de los aspectos más importantes. 