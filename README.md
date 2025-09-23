Actividad VISE:

Maria Paula Salamanca Gómez

Introducción a la actividad:
La empresa VISE está buscando construir una plataforma para procesar diferentes pagos con
tarjetas.
Para ello, la empresa requiere de un desarrollador que pueda diseñar e implementar una API
REST con JSON que procese compras para los distintos tipos de tarjeta que cuenta un cliente
de VISE. En un principio se va a requerir que se implementen las restricciones y los beneficios
de cada tipo de tarjeta:


Restricciones del proyecto:

• Classic: No posee restricciones

• Gold: Se requiere que posea un ingreso mínimo de 500 USD mensuales.

• Platinum:
‣ Se requiere que posea un ingreso mínimo de 1000 USD mensuales.
‣ Debe poseer la suscripción VISE CLUB.

• Black:
‣ Se requiere que posea un ingreso mínimo de 2000 USD mensuales.
‣ Debe poseer la suscripción VISE CLUB.
‣ No puede ser un cliente que viva en los siguientes países: China, Vietnam, India e Irán.

• White:
‣ Posee las mismas restricciones que el Black

Beneficios:

• Classic: No tiene beneficios.

• Gold:
‣ Los lunes, martes y miércoles, las compras mayores a 100 USD poseen un 15% de
descuento.

• Platinum:
‣ Los lunes, martes y miércoles, las compras mayores a 100 USD poseen un 20% de
descuento.
‣ Los sábados, las compras mayores a 200 USD poseen un 30% de descuento.
‣ Las compras realizadas en el exterior poseen un 5% de descuento.

• Black:
‣ Los lunes, martes y miércoles, las compras mayores a 100 USD poseen un 25% de
descuento.
‣ Los sábados, las compras mayores a 200 USD poseen un 35% de descuento.
‣ Las compras realizadas en el exterior (si el país origen de la compra es distinto al país de
residencia del cliente) poseen un 5% de descuento.

• White:
‣ Del lunes a viernes, las compras mayores a 100 USD poseen un 25% de descuento.
‣ Los sábados y domingos, las compras mayores a 200 USD poseen un 35% de descuento.
‣ Las compras realizadas en el exterior poseen un 5% de descuento.



Las peticiones JSON deben tener la siguientes rutas y estructura:
1. POST /client:
Registra un cliente sí es apto para solicitar un tipo de tarjeta.
• Cuerpo JSON de la petición:
{
 "name": "John Doe",
 "country": "USA",
 "monthlyIncome": 1200,
 "viseClub": true,
 "cardType": "Platinum"
}
• Respuesta JSON cuando la petición es válida:
{
 "clientId": 1,
 "name": "John Doe",
 "cardType": "Platinum",
 "status": "Registered",
 "message": "Cliente apto para tarjeta Platinum"
}
Cuando es valida la petición, el cliente queda registrado con sus datos y el tipo de tarjeta
solicitada.
• Respuesta JSON cuando la petición es invalida:
{
 "status": "Rejected",
 "error": "El cliente no cumple con la suscripción VISE CLUB requerida para
Platinum"
}


2. POST /purchase:
Recibe el identificador del cliente (registrado previamente) junto con los datos de la compra.
Aplica las restricciones y beneficios de la tarjeta asignada.
• Cuerpo JSON de la petición:
{
 "clientId": 1,
 "amount": 250,
 "currency": "USD",
 "purchaseDate": "2025-09-20T14:30:00Z",
 "purchaseCountry": "France"
}
• Respuesta (cuando la compra es aprobada con beneficio):
{
 "status": "Approved",
 "purchase": {
 "clientId": 1,
 "originalAmount": 250,
 "discountApplied": 75,
 "finalAmount": 175,
 "benefit": "Sábado - Descuento 30%"
 }
}
• Respuesta cuando la compra es rechazada por restricción
{
 "status": "Rejected",
 "error": "El cliente con tarjeta Black no puede realizar compras desde China"
}