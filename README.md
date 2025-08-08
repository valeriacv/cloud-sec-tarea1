# Seguridad en la Nube 
## Tarea 01 

En este repositorio se encuentra la representación de la arquitectura de la aplicación Omnione OpenDID, que es un proyecto que desarrolló un sistema de identificación digital de código libre. 

### Descripción del proyecto
En el Instituto Tecnológico de Costa Rica se busca utilizar esta herramienta para autenticar de forma confiable y segura la identidad de estudiantes y colaboradores de esta institución. Actualmente se utiliza un carnet físico, con OpenDID la idea sería ir migrando a un identificación en formato digital que brinde mayor seguridad y confiabilidad.

### Descripción de la arquitectura
La arquitectura tiene una capa externa conformada por zonas DNS para la definición de dominios del sistema y las politicas de seguridad del DNS que definen reglas de seguridad para poder entrar al sistema.

En la parte externa tambien hay una capa llama Legacy, que contiene servicios legacy es decir servicios usados anteriormente que de alguna forma tienen que convivir OpenDID.

Luego esta la capa del VPC que genera como un encapsulamiento del sistema del resto del internet para que sus partes no puedan ser accedidas de forma libre, si no que se define un unico punto de entrada al sistema y ese punto se comunica con los demás elementos.

Dentro de la VPC se encuentra un servicio de correos para poder enviar notificaciones por este medio y 3 capas más, la capa de presentación, la capa de aplicación y la capa de base datos.

La capa de presentación tiene un Amazon CloudFront para la distribución de contenido estático, como una página web estática. Un Web Application Firewall Policies (WAF) como parte de la seguridad de esta capa para realizar filtración y bloqueo de trafico indeseado. Por ultimo en esta capa se tiene el Amazon API Gateway que va a permitir exponer fuera del VPC el API del sistema hacia los consumidores.

En la capa de aplicación se encuentra diferente servicios en un cluster de kubernetes, el primer sericio que se tiene es el de verifier que se encarga de recibir y verificar las identidades. El servicio de issuer que conoce o tiene la identidad del usuario y en base a eso le genera una  identificación digital. Luego esta el servicio del wallet que contiene los servicios del usuarios además del CApp y el wallet que se encargan de revisar y verificar el estado del app del usuario y el wallet que utiliza. Toda esta capa tiene un unico punto de ingreso que se encarga de ordenar el trafico hacia adentro de la capa. Luego esta la capa del legacy API middleware que es el encargado de poder comunicar los servicio legacy al nuevo sistema. Y por ultimo estan dos capaz de servicios de notificaciones una externa y una del agente de confianza.

Por ultimo se tiene la capa de base de datos que contiene dos servicios, una Amazon RDS con una base de datos postgress para el almacenamiento de datos y el Hyperledger Fabric que es una plataforma de blockchain que permite el manejo de transacciones de forma segura y que sean verificables.


### Recomendación de seguridad
Una recomendación de seguridad para la arquitectura seria utilizar algún servicio como Cognito que permita la generación de API keys para realizar la autenticación cuando se da comunicación entre servicios fuera de la VPC, por ejemplo con los legacy services, además el servicio de API Gateway puede ser configurado para verificar las credenciales por medio de Lambda Authorizers, esta medida ayuda a que al sistema dentro del VPC solo ingresen request de servicios autorizados, de igual forma si la comunicación es hacia afuera, por ejemplo con los legacy services ellos también deben permitir solo request de servicios autorizados, ya que si los servicios legacy se ven comprometidos puede llegar a afectar el sistema dentro de la VPC

Otra recomendación de seguridad que puede ser más para tomar acciones reactivas en lugar de preventivas, es el uso de servicios de monitoreo, en este caso que hay varios servicios de amazon involucrados se puede utilizar Cloudwatch permitiendo hacer monitoreo de los request e incluso generando alarmas si hay volumenes altos de accesos o request en diferentes servicios como el API Gateway o la base de datos, permitiendo tomar acciones de defensa en cortos periodos de tiempo.

### Links importantes
[Omnione OpenDID](https://opendid.omnione.net/community/)
[Componentes de OpenDID](https://omnioneid.github.io/?locale=en&version=V1.0.0#/V1.0.0/docs/concepts/components?id=open-did-components)








