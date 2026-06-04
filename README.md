# Sistema de Gestión de Cine (MVP)

Este proyecto es un Producto Mínimo Viable (MVP) desarrollado para la solución y automatización de la administración interna de un complejo de cine. El sistema implementa un enfoque de **Desarrollo Guiado por Comportamiento (BDD)** y metodologías de control de calidad estrictas, asegurando un blindaje sintáctico y semántico completo en todos sus módulos para evitar el ingreso de datos inconsistentes.

---

## Características Principales

El sistema está dividido en cuatro módulos interconectados que controlan el ciclo completo del negocio:

* **Gestión de Películas:** Controla el catálogo de películas (título, género y duración) garantizando restricciones semánticas de tiempo antes de su asignación.
* **Gestión de Salas:** Administra el inventario de las salas físicas del cine, controlando de manera estricta el rango de capacidad de asientos (de 1 a 300) y limitando el identificador comercial a un máximo de 50 salas.
* **Gestión de Funciones:** Actúa como el puente del sistema, permitiendo programar películas en salas específicas con controles de fecha, hora y tarifas.
* **Gestión de Ventas (Taquilla):** Permite realizar la compra y reserva física de asientos para las funciones disponibles. Cuenta con una restricción de compra de un mínimo de 1 y un máximo de 10 asientos por transacción, calculando el total automáticamente y evitando la duplicidad de asientos ocupados en una misma función.

## Catálogo de Requisitos MVP

A continuación se detallan los requerimientos funcionales que abarca el sistema:

### Módulo de Películas

| ID | Nombre | Descripción | Reglas de Negocio |
| --- | --- | --- | --- |
| **RF-P01** | Registrar película | Crear película con título, género y duración. | Título 1-100 caracteres. Duración 60-240 min. Género del catálogo. |
| **RF-P02** | Listar películas | Listado paginado ordenado por título. | Respuesta menor a 2 segundos. |
| **RF-P03** | Ver detalle | Consultar datos completos por ID. | El ID debe existir. |
| **RF-P04** | Editar película | Modificar título, género o duración. | Reevaluar todas las validaciones. |
| **RF-P05** | Eliminar película | Dar de baja del catálogo. | No se permite si tiene funciones asociadas. |

### Módulo de Salas

| ID | Nombre | Descripción | Reglas de Negocio |
| --- | --- | --- | --- |
| **RF-S01** | Registrar sala | Crear sala con número y capacidad. | Número entero mayor igual que 1 y único. |
| **RF-S02** | Listar salas | Mostrar salas ordenadas por número. | Orden ascendente. |
| **RF-S03** | Buscar sala | Localizar la sala por número exacto. | Coincidencia exacta del campo número. |
| **RF-S04** | Editar sala | Modificar número o capacidad. | Reevaluar unicidad y rangos. |
| **RF-S05** | Eliminar sala | Dar de baja del sistema. | No se permite si tiene funciones programadas. |

### Módulo de Funciones

| ID | Nombre | Descripción | Reglas de Negocio |
| --- | --- | --- | --- |
| **RF-F01** | Registrar función | Crear función con película, sala, fecha, hora y precio. | Todos los campos obligatorios. El precio no puede ser negativo. |
| **RF-F02** | Listar funciones | Mostrar todas las funciones registradas. | Incluye datos de película y sala relacionados. |
| **RF-F03** | Buscar función | Obtener datos de una función por ID. | El ID debe existir. |
| **RF-F04** | Editar función | Actualizar datos de una función. | Reevaluar todas las validaciones al actualizar. |
| **RF-F05** | Eliminar función | Dar de baja una función. | Solo si el ID indicado existe. |

### Módulo de Ventas

| ID | Nombre | Descripción | Regla de Negocio |
| --- | --- | --- | --- |
| **RF-V01** | Registrar venta | Registrar la compra de entradas para una función seleccionando asientos disponibles. | Mínimo 1 asiento, máximo 10 por venta. No se permiten asientos ya ocupados en esa función. |
| **RF-V02** | Seleccionar asientos | El usuario elige asientos visualmente de un mapa de hasta 20 asientos por función. | Los asientos ocupados se muestran deshabilitados. No se permiten asientos repetidos en la misma venta. |
| **RF-V03** | Calcular total | El sistema calcula automáticamente el total de la venta según cantidad de entradas. | Precio unitario fijo de S/ 15.00. Total = cantidad × precio. |
| **RF-V04** | Validar capacidad | Antes de confirmar, verificar que haya cupo disponible en la sala. | Capacidad de sala entre 20 y 300 asientos. Si la venta supera el cupo restante, se rechaza. |
| **RF-V05** | Listar ventas | Mostrar todas las ventas registradas, filtrables por película. | Se muestra ID, película, función, cantidad, total, fecha y estado. |

---

## Stack Tecnológico

El software utiliza un conjunto de herramientas nativas y frameworks estándar de la industria para asegurar un sistema modular, robusto y fácil de probar:

* **Python v3.14**: Lenguaje de programación base utilizado para toda la lógica de negocio, aplicando tipado estricto y programación defensiva.
* **Tkinter / ttk**: Librería nativa empleada para el diseño de la interfaz gráfica de usuario (UI), incluyendo tablas dinámicas (`Treeview`) y alertas visuales (`messagebox`).
* **JSON**: Formato de almacenamiento local en archivos planos (`.json`) para gestionar la persistencia física de datos sin dependencias externas complejas.
* **Pytest & Unittest**: Frameworks de automatización utilizados para la suite de pruebas unitarias y de integración, cubriendo casos de Partición de Equivalencia (PE) y Análisis de Valores Límite (AVL).
* **GitHub Copilot CLI**: Asistente de código basado en Inteligencia Artificial, alineado metodológicamente para la agilización de la documentación técnica, estructuración de escenarios BDD (Gherkin) y asistencia en el refactor del código.

---

## Estructura del Proyecto

```text
MVPGestionDeCine/
│
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
│
├── src/                    # Código fuente del sistema
│   ├── models/             # Modelos de dominio (Película, Sala, Venta, etc.)
│   ├── services/           # Capa de lógica de negocio y servicios
│   ├── storage/            # Capa de persistencia (Repositorios y archivos .json)
│   └── ui/                 # Interfaces gráficas de usuario (Tkinter)
│
├── tests/                  # Suite de pruebas automatizadas (Pytest / Unittest)
└── features/               # Escenarios de comportamiento en lenguaje Gherkin
```

## Instalación y Ejecución

**Requisitos Previos:** Asegúrate de tener instalado Python v3.14 o superior en tu sistema.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/MVPGestionDeCine.git
cd MVPGestionDeCine
```

### 2. Instalar dependencias

Instala los frameworks necesarios para el entorno de pruebas:

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Para iniciar el entorno gráfico del sistema, ejecuta desde la raíz del proyecto:

```bash
python main.py
```

## Ejecución de las Pruebas

Para validar el correcto funcionamiento de los blindajes lógicos y pasar la suite de control de calidad, ejecuta Pytest desde la terminal en la raíz del proyecto:

```bash
# Ejecutar todas las pruebas del sistema
pytest

# Ejecutar específicamente las pruebas del módulo de salas
pytest tests/test_sala.py

# Ejecutar específicamente las pruebas del módulo de ventas
python tests/test_venta.py
```

## Integrantes del Grupo

* Barrios Medina Mathias Alonso
* Cuno Salazar Eduardo Joel
* Hancco Mullisaca Sergio Danilo
* Suclle Suca Michael Benjamin