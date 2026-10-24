<div align="center">

# HeadSalud · Sistema Web de Gestión de Citas Médicas

**Proyecto de Examen Parcial II** — Desarrollo web con PHP y PostgreSQL
Caso de estudio: *Clínica Vida Salud*

[![PHP](https://img.shields.io/badge/PHP-8.3-777BB4?logo=php&logoColor=white)](#tecnologías)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](#base-de-datos)
[![PDO](https://img.shields.io/badge/PDO-pdo__pgsql-0d9488)](#seguridad)
[![Vercel](https://img.shields.io/badge/Demo-Vercel-000?logo=vercel)](https://headsalud.vercel.app)

**Demo en línea:** https://headsalud.vercel.app · **Repositorio:** https://github.com/Kato-001/headsalud

| Repositorio | Demo |
|:-:|:-:|
| <img src="Docs/qr-repositorio.png" width="150" alt="QR del repositorio"> | <img src="Docs/qr-demo.png" width="150" alt="QR de la demo"> |

</div>

---

## Integrantes

| Integrante | Registro |
|---|---|
| Sergio Estaca Paco | 221089421 |
| Frank Miguel Yerbales Molina | 218164629 |

**Grupo:** _(completar)_ · **Materia:** _(completar)_ · **Docente:** _(completar)_

---

## Tabla de contenido

1. [Descripción](#descripción)
2. [Objetivos](#objetivos)
3. [Funcionalidades](#funcionalidades)
4. [Roles y permisos](#roles-y-permisos)
5. [Tecnologías](#tecnologías)
6. [Arquitectura](#arquitectura)
7. [Base de datos](#base-de-datos)
8. [Reglas de negocio](#reglas-de-negocio-cómo-se-cumplen)
9. [Seguridad](#seguridad)
10. [Instalación local](#instalación-local)
11. [Despliegue en Vercel](#despliegue-en-vercel)
12. [Cuentas de prueba](#cuentas-de-prueba)
13. [Pruebas](#pruebas)
14. [Estructura del proyecto](#estructura-del-proyecto)

---

## Descripción

La Clínica Vida Salud administraba sus citas con cuadernos, llamadas y hojas de cálculo, lo que provocaba citas duplicadas, datos de pacientes perdidos, desconocimiento de los horarios disponibles y falta de reportes.

**HeadSalud** centraliza esa información en una aplicación web: registra pacientes, médicos, especialidades y horarios, **programa citas mostrando solo los horarios realmente libres** y controla sus estados (programada, confirmada, atendida, cancelada, inasistencia). Incluye agenda médica, historial por paciente, atención médica con tratamientos, reportes administrativos y un portal donde el paciente reserva y sigue sus propias citas.

## Objetivos

**General.** Desarrollar un sistema web de gestión de citas médicas con PHP y PostgreSQL que mejore el registro, la programación, el seguimiento y el control de las citas de la clínica.

**Específicos**
- Analizar los procesos de registro y programación de citas de la clínica.
- Diseñar una base de datos relacional normalizada con claves primarias y foráneas.
- Implementar el registro, la consulta, la modificación y la desactivación de pacientes y médicos.
- Gestionar especialidades y horarios de atención.
- Programar citas verificando la disponibilidad del médico en el servidor.
- Controlar los estados de las citas y sus transiciones.
- Generar reportes por fecha, médico, especialidad y estado.
- Aplicar validaciones y mecanismos de seguridad.
- Verificar el funcionamiento con pruebas.

## Funcionalidades

| Requerimiento | Implementación |
|---|---|
| **RF01** Inicio de sesión y control de acceso | Login con usuario, correo o CI (pacientes). `password_hash()` / `password_verify()`, sesión regenerada al ingresar, menú según permisos, cierre de sesión y bloqueo tras 5 intentos fallidos por IP. |
| **RF02** Gestión de pacientes | Registro con código autogenerado (`PAC-0001`), búsqueda por CI, nombre o apellido, edición, desactivación sin perder el historial, historia clínica y contactos de emergencia. CI único. |
| **RF03** Gestión de médicos | Registro con su cuenta de acceso, una o varias especialidades, búsqueda por nombre o especialidad, ficha con agenda y activación/desactivación. |
| **RF04** Especialidades | CRUD con estado. No se repiten nombres normalizados ("Pediatría" = "pediatria "). |
| **RF05** Horarios de atención | Horarios por día con validación de rangos y cruces, duración de cita configurable y bloqueos de agenda (feriados, vacaciones, permisos). |
| **RF06** Registro de citas | Asistente paso a paso: paciente → especialidad → médico → fecha → **solo horarios libres**. Genera el código `CM-0001` y la fecha de registro. |
| **RF07** Prevención de duplicados | Verificación en PHP dentro de una transacción con bloqueo (`SELECT … FOR UPDATE`) y restricción `EXCLUDE USING gist` en PostgreSQL. |
| **RF08** Reprogramación | Muestra los nuevos horarios libres del mismo médico, guarda el motivo y deja el historial anterior → nuevo. |
| **RF09** Cancelación | Exige un motivo, no borra la cita y libera el horario. |
| **RF10** Asistencia y estados | Programada → Confirmada → Atendida / Inasistencia / Cancelada. Las transiciones inválidas se rechazan en PHP y en un trigger. |
| **RF11** Agenda médica | Por fecha, médico y estado, con los bloques libres intercalados. El médico ve solo su agenda. |
| **RF12** Historial por paciente | Todas sus citas (incluidas canceladas) con médico, especialidad, estado y fecha de registro, además de sus consultas y tratamientos. |
| **RF13** Reportes | Resumen del período, citas por fecha, médico, especialidad y estado, pacientes registrados y agenda diaria. Filtros por rango, totales, **exportación a CSV** e impresión a PDF. |
| Portal del paciente (3.4) | Autoregistro, perfil (datos personales, información médica, contactos de emergencia, cuenta), reserva y cancelación de citas, historial médico y recordatorios automáticos. |
| Atención médica | El médico registra signos vitales, diagnóstico y tratamientos; la cita pasa a *Atendida* en la misma transacción. |
| Auditoría | Bitácora de inicios de sesión, intentos fallidos y cada operación, con usuario, fecha e IP. |

## Roles y permisos

Los permisos se asignan por rol desde **Administración → Roles y permisos** (tabla `ROLPERMISO`). Cada ruta del sistema exige un permiso concreto (RN12).

| Permiso | Admin | Recepción | Médico | Paciente |
|---|:-:|:-:|:-:|:-:|
| Usuarios, roles, configuración, bitácora | ✔ | | | |
| Especialidades, médicos, horarios | ✔ | consulta | | |
| Pacientes | ✔ | ✔ | | |
| Programar, reprogramar y cancelar citas | ✔ | ✔ | | |
| Confirmar e inasistencia | ✔ | ✔ | | |
| Agenda de todos los médicos | ✔ | ✔ | | |
| Agenda propia y atender citas | | | ✔ | |
| Reportes | ✔ | ✔ | | |
| Portal del paciente | | | | ✔ |

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | PHP 8.3 sin framework, con arquitectura MVC propia |
| Acceso a datos | PDO con el controlador `pdo_pgsql` y consultas parametrizadas |
| Base de datos | PostgreSQL 17 (Supabase) con las extensiones `btree_gist` y `pgcrypto` |
| Frontend | HTML5, CSS3 (variables, modo claro/oscuro, animaciones) y JavaScript sin librerías |
| Servidor local | Apache (XAMPP/Laragon) o el servidor integrado de PHP |
| Producción | Vercel (`vercel-php`, región São Paulo) y Supabase (región São Paulo) |

## Arquitectura

```
Navegador ──HTTP──▶ api/index.php (controlador frontal + rutas)
                         │
                         ▼
               app/core  ── Router · Auth · Csrf · Session · Validator · View · Database (PDO)
                         │
        ┌────────────────┼──────────────────┐
        ▼                ▼                  ▼
 app/controllers   app/services       app/views
 (reciben la       (reglas de          (plantillas PHP
  petición,         negocio: citas,     por paquete P1…P6
  validan)          disponibilidad)     y portal)
        │                │
        └──────▶ app/models (acceso a datos con SQL parametrizado)
                         │
                         ▼
                PostgreSQL (esquema "clinica": tablas, restricciones y triggers)
```

- **Separación de responsabilidades:**
  - Los controladores no contienen SQL.
  - Los modelos no generan HTML.
  - Las reglas de citas están en `services/CitaService.php` y `services/Disponibilidad.php`.
- **Patrón Post/Redirect/Get** con mensajes *flash*: al recargar la página no se reenvía el formulario.
- **Organización por paquetes** del análisis: P1 Seguridad, P2 Gestión médica, P3 Pacientes, P4 Citas, P5 Atención médica, P6 Reportes.

## Base de datos

- **Diagrama de clases:** [`Docs/Diagrama de Clinica.svg`](Docs/Diagrama%20de%20Clinica.svg)
- **Scripts:** en [`Bakend/database/`](Bakend/database). Se ejecutan en orden:

| Script | Contenido |
|---|---|
| `01_esquema.sql` | 21 tablas del diagrama más `PERMISO`, `ROLPERMISO` y `SESION`. PK, FK, `UNIQUE`, `CHECK` y restricciones `EXCLUDE`. |
| `02_reglas_negocio.sql` | Trigger `validar_cita` (RN04–RN08, RF08, RF10), protección de roles del sistema y RLS. |
| `03_datos_iniciales.sql` | Roles, permisos, configuración, estados, especialidades, médicos con horarios, pacientes y unas 240 citas de ejemplo alrededor de la fecha actual. |
| `04_usuario_app.sql` | Usuario de base de datos con privilegios mínimos para la aplicación. |
| `00_limpiar_version_anterior.sql` | (Opcional) borra una versión de prueba anterior. |

**Relaciones principales:**
- Un paciente tiene muchas citas, y un médico atiende muchas citas.
- Médico ↔ especialidad es una relación muchos a muchos (`MEDICOESPECIALIDAD`).
- Un médico tiene varios horarios y varios bloqueos de agenda.
- Una cita tiene un historial de cambios (`HISTORIALCITA`), una consulta y notificaciones.
- Una consulta tiene tratamientos y estudios.

## Reglas de negocio (cómo se cumplen)

| Regla | PHP | PostgreSQL |
|---|---|---|
| RN01 / RN02 Identificador único | Código autogenerado | `PRIMARY KEY`, `UNIQUE (codigo)`, `UNIQUE (ci)` |
| RN03 Paciente y médico válidos | `CitaService::programar` | `FOREIGN KEY` |
| RN04 Médico activo | `Disponibilidad::bloques` | trigger `validar_cita` |
| RN05 Dentro del horario | Solo se ofrecen bloques del horario | trigger `validar_cita` |
| RN06 Sin fechas pasadas | `Validator::fecha(min: hoy)` | trigger `validar_cita` |
| RN07 Sin superposición | Transacción + `FOR UPDATE` + verificación | `EXCLUDE USING gist (idmedico WITH =, tsrange WITH &&)` |
| RN08 Duración configurada | Bloques de `DURACION_CITA_MINUTOS` | trigger `validar_cita` |
| RN09 Canceladas no ocupan | `estadocita.ocupahorario` | `EXCLUDE … WHERE codigoestado <> 'CANCELADA'` |
| RN10 Historial de atendidas | No se borran citas | `HISTORIALCITA` |
| RN11 No eliminar con historial | Solo se activa o desactiva | `FOREIGN KEY` sin `CASCADE` |
| RN12 Solo usuarios autorizados | `Auth::requerir('permiso')` en cada acción | El usuario `headsalud_app` solo tiene permisos de datos |
| RN13 Disponibilidad en el servidor | Se vuelve a comprobar dentro de la transacción | Restricción `EXCLUDE` |
| RN14 Persistencia en PostgreSQL | PDO | — |

## Seguridad

- **Contraseñas:** se guardan con `password_hash()` (bcrypt) y se verifican con `password_verify()`. El hash se actualiza automáticamente con `password_needs_rehash()`.
- **Inyección SQL:** todas las consultas usan PDO con parámetros (`:nombre`). Nunca se concatenan datos del usuario.
- **XSS:** toda salida pasa por `e()` (`htmlspecialchars`).
- **CSRF:** cada formulario POST lleva un token de sesión que se verifica con `hash_equals`.
- **Sesiones:**
  - Cookies `HttpOnly`, `SameSite=Lax` y `Secure` en HTTPS.
  - El ID de sesión se regenera al iniciar sesión.
  - Las sesiones caducan tras 2 horas de inactividad.
  - Se guardan en la tabla `SESION`, porque Vercel es serverless.
- **Control de acceso:**
  - Cada petición recarga el usuario y sus permisos.
  - Una cuenta desactivada pierde la sesión de inmediato.
  - Ninguna página interna se puede abrir sin sesión.
- **Fuerza bruta:** se bloquea tras 5 intentos fallidos por IP en 10 minutos, y cada intento queda registrado en la bitácora.
- **Errores:**
  - En producción no se muestran detalles internos: se registran en el log y el usuario ve un mensaje claro.
  - Los errores de PostgreSQL se traducen (`AppException::desdePdo`).
- **Validación doble:** JavaScript en el navegador y `Validator` en PHP aplican las mismas reglas. Se rechaza cualquier texto que no sea UTF-8 válido.
- **Credenciales:** van en variables de entorno (`.env` local, panel de Vercel) y **nunca se suben al repositorio**.

## Instalación local

**Requisitos:** PHP 8.1 o superior con `pdo_pgsql` y `mbstring` (Laragon y XAMPP lo traen), y PostgreSQL 14 o superior (local o Supabase).

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Kato-001/headsalud.git && cd headsalud
   ```
2. **Crear la base de datos.** En PostgreSQL local, por ejemplo con pgAdmin:
   ```sql
   CREATE DATABASE headsalud;
   ```
   Luego ejecute en orden `01_esquema.sql`, `02_reglas_negocio.sql`, `03_datos_iniciales.sql` y `04_usuario_app.sql` (cambie `CAMBIAR_CLAVE` por su contraseña). Los scripts funcionan igual en PostgreSQL local y en Supabase.
3. **Configurar el entorno**
   ```bash
   cp .env.example .env
   # DATABASE_URL=postgresql://headsalud_app:SU_CLAVE@localhost:5432/headsalud?sslmode=disable
   ```
4. **Ejecutar**, con una de estas dos opciones:
   - **Servidor integrado de PHP:**
     ```bash
     php -S localhost:8000 router.php
     ```
     Luego abra http://localhost:8000.
   - **Apache (XAMPP/Laragon):** copie la carpeta en `htdocs` / `www`. El `.htaccess` envía todo a `api/index.php` y bloquea el acceso a `app/`, `.env` y los scripts SQL.

## Despliegue en Vercel

PHP corre en Vercel gracias al runtime comunitario [`vercel-php`](https://github.com/vercel-community/php) (configurado en `vercel.json`).

```bash
npx vercel link
npx vercel env add DATABASE_URL production   # cadena del pooler de Supabase (puerto 6543)
npx vercel env add APP_ENV production         # valor: production
npx vercel deploy --prod
```

- **Archivos estáticos:** las rutas `/assets/*` se sirven desde `public/`.
- **Rutas:** todo lo demás pasa por `api/index.php`.
- **Pooler de Supabase:** se usa en modo transacción, por eso `PDO::ATTR_EMULATE_PREPARES` está activo.

## Cuentas de prueba

Contraseña de todas: **`HeadSalud2026`** (cámbiela en *Mi cuenta*).

| Rol | Usuario | Qué puede hacer |
|---|---|---|
| Administrador | `admin` | Todo el sistema |
| Recepcionista | `mrojas` | Pacientes, citas, agenda y reportes |
| Médico | `cmendoza`, `lvargas`, `rsuarez`, `pmolina` | Su agenda y la atención de sus pacientes |
| Paciente | `jperez` (o CI `1234567`), `mlopez` | Portal del paciente |

## Pruebas

Pruebas mínimas del enunciado, ejecutadas contra el sistema:

| N.º | Prueba | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| 1 | Registrar un paciente nuevo | Queda guardado | ✅ «Paciente registrado correctamente» y se generó `PAC-0009` |
| 2 | Paciente con CI duplicado | Se rechaza | ✅ «Ya existe un paciente registrado con ese CI» |
| 3 | Cita en horario disponible | Queda registrada | ✅ «Cita CM-0245 programada…» |
| 4 | Cita superpuesta, mismo médico | Se impide | ✅ «El horario de las 08:00 ya no está disponible: el médico tiene otra cita» |
| 5 | Cita fuera del horario | Se rechaza | ✅ «La hora elegida está fuera del horario de atención del médico» |
| 6 | Cancelar una cita | Queda cancelada y conserva el historial | ✅ Estado *Cancelada*, el horario queda libre y el historial se conserva |
| 7 | Historial de un paciente | Aparecen sus citas | ✅ Lista con la cita cancelada incluida |
| 8 | Citas de un médico por fecha | Resultados correctos | ✅ Agenda filtrada por médico, fecha y estado |
| 9 | Página interna sin sesión | Acceso denegado | ✅ Redirige a `/login` (302) |
| 10 | Datos inválidos | El servidor rechaza | ✅ CI con letras, fecha futura y correo inválido se rechazan aunque se salte el JavaScript |

**Pruebas adicionales**
- **En la base de datos:** insertando por SQL directo se rechazan el cruce de citas, las fechas pasadas, las horas fuera del horario, la duración incorrecta, las transiciones de estado inválidas, el borrado de pacientes con citas, el CI duplicado, las especialidades repetidas y los horarios cruzados.
- **Permisos por rol:** la recepción, el médico y el paciente reciben **403** en las páginas que no les corresponden.
- **Portal:** un paciente no puede cancelar citas de otro (404).

## Estructura del proyecto

```
headsalud/
├── api/index.php              # Controlador frontal y tabla de rutas
├── app/
│   ├── bootstrap.php          # Arranque: entorno, errores, autoload, sesión
│   ├── core/                  # Router, Auth, Csrf, Session, Validator, View, Database…
│   ├── controllers/           # Un controlador por caso de uso o módulo
│   ├── models/                # Acceso a datos (SQL parametrizado)
│   ├── services/              # CitaService (reglas de citas) y Disponibilidad
│   └── views/                 # P1_SeguridadAcceso … P6_Reportes, Portal, layouts, partials
├── public/assets/             # CSS (diseño y animaciones) y JS (validación y asistente de citas)
├── Bakend/database/           # Scripts SQL de PostgreSQL
├── Docs/                      # Diagrama de clases y códigos QR
├── router.php                 # Enrutador para `php -S`
├── .htaccess                  # Reglas para Apache (XAMPP)
├── vercel.json                # Despliegue en Vercel
└── .env.example               # Plantilla de configuración
```

---

<div align="center">
<sub>Clínica Vida Salud es un caso ficticio con fines académicos.</sub>
</div>
