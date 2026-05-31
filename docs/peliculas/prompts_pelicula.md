# Primer Prompt:
Actúa como Analista de Requisitos y QA.
Genera la documentación completa para el módulo Película de un Sistema de Gestión de Cine.

Campos:
- id_pelicula
- titulo
- genero
- duracion

Genera:
1. Objetivo del módulo.
2. Requisitos funcionales.
3. Requisitos no funcionales.
4. Reglas de negocio.
5. Escenarios Gherkin.
6. Casos de Partición de Equivalencia (PE).
7. Casos de Análisis de Valores Límite (AVL).

La salida debe estar lista para colocar en:
docs/peliculas/requisitos.md
features/pelicula.feature
docs/peliculas/casos_pe_avl.md

# Segundo Prompt

Actúa como QA Engineer experto en Pytest.
Basándote en los requisitos, reglas de negocio, PE, AVL y escenarios Gherkin del módulo Película que se muestran a continuación:
docs/peliculas/*
features/pelicula.feature
Genera el archivo completo tests/test_pelicula.py.

Requisitos:
- Utilizar pytest.
- Crear una prueba por cada caso PE.
- Crear una prueba por cada caso AVL.
- Crear pruebas para los escenarios Gherkin.
- Utilizar nombres descriptivos.
- Utilizar pytest.raises(ValueError) cuando corresponda.

No generar la implementación de la clase Pelicula.
Solo generar test_pelicula.py.

# Tercer prompt 
Actúa como desarrollador Python senior.
Implementa models/pelicula.py para que todos los tests de test_pelicula.py pasen correctamente.

Debe incluir:
- Constructor.
- Validaciones.
- Métodos auxiliares.
- Manejo de excepciones mediante ValueError.
- Código limpio y orientado a objetos.

No generar interfaz gráfica.
No generar almacenamiento JSON.

# Cuarto Prompt
Actúa como desarrollador Python.
Genera un repositorio JSON para almacenar películas.
Archivos:
- data/peliculas.json

Funciones:
- guardar()
- listar()
- buscar_por_titulo()
- actualizar()
- eliminar()

Utiliza la clase Pelicula previamente creada.

# Quito Prompt:
Actúa como desarrollador Tkinter.
Genera ui/pelicula_ui.py.

Requisitos:
- Registrar película.
- Listar películas.
- Editar película.
- Eliminar película.

Utilizar:
- ttk.Treeview
- messagebox
- Combobox para género

Conectar con el repositorio JSON.
