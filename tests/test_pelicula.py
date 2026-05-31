from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from models.pelicula import Pelicula
from services.pelicula_service import PeliculaService


def pelicula_valida_kwargs():
    return {
        "titulo": "Matrix",
        "genero": "Ciencia Ficcion",
        "duracion": 136,
    }


@pytest.fixture
def service():
    return PeliculaService()


def crear_pelicula(**overrides):
    data = pelicula_valida_kwargs()
    data.update(overrides)
    return Pelicula(**data)


# PE - titulo
def test_pe_ti_01_titulo_valido_matrix():
    pelicula = crear_pelicula(titulo="Matrix")
    assert pelicula.titulo == "Matrix"


def test_pe_ti_02_titulo_valido_minimo():
    pelicula = crear_pelicula(titulo="A")
    assert pelicula.titulo == "A"


def test_pe_ti_03_titulo_vacio_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(titulo="")


def test_pe_ti_04_titulo_solo_espacios_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(titulo="   ")


def test_pe_ti_05_titulo_mas_100_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(titulo="A" * 101)


def test_pe_ti_06_titulo_duplicado_rechaza(service):
    service.registrar(**pelicula_valida_kwargs())
    with pytest.raises(ValueError):
        service.registrar(
            titulo=" matrix ",
            genero="Ciencia Ficcion",
            duracion=136,
        )


# PE - genero
def test_pe_ge_01_genero_accion_valido():
    pelicula = crear_pelicula(genero="Accion")
    assert pelicula.genero == "Accion"


def test_pe_ge_02_genero_fantasia_valido():
    pelicula = crear_pelicula(genero="Fantasia")
    assert pelicula.genero == "Fantasia"


def test_pe_ge_03_genero_fuera_catalogo_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(genero="Western")


def test_pe_ge_04_genero_vacio_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(genero="")


# PE - duracion
def test_pe_du_01_duracion_90_valida():
    pelicula = crear_pelicula(duracion=90)
    assert pelicula.duracion == 90


def test_pe_du_02_duracion_1_valida():
    pelicula = crear_pelicula(duracion=1)
    assert pelicula.duracion == 1


def test_pe_du_03_duracion_0_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=0)


def test_pe_du_04_duracion_301_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=301)


def test_pe_du_05_duracion_negativa_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=-10)


def test_pe_du_06_duracion_decimal_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=90.5)


def test_pe_du_07_duracion_no_numerica_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion="noventa")


# AVL - titulo
def test_avl_ti_01_longitud_0_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(titulo="")


def test_avl_ti_02_longitud_1_acepta():
    pelicula = crear_pelicula(titulo="A")
    assert pelicula.titulo == "A"


def test_avl_ti_03_longitud_100_acepta():
    titulo = "A" * 100
    pelicula = crear_pelicula(titulo=titulo)
    assert pelicula.titulo == titulo


def test_avl_ti_04_longitud_101_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(titulo="A" * 101)


# AVL - duracion
def test_avl_du_01_valor_0_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=0)


def test_avl_du_02_valor_1_acepta():
    pelicula = crear_pelicula(duracion=1)
    assert pelicula.duracion == 1


def test_avl_du_03_valor_300_acepta():
    pelicula = crear_pelicula(duracion=300)
    assert pelicula.duracion == 300


def test_avl_du_04_valor_301_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(duracion=301)


# AVL - genero
def test_avl_ge_01_catalogo_primero_acepta():
    pelicula = crear_pelicula(genero="Accion")
    assert pelicula.genero == "Accion"


def test_avl_ge_02_catalogo_ultimo_acepta():
    pelicula = crear_pelicula(genero="Fantasia")
    assert pelicula.genero == "Fantasia"


def test_avl_ge_03_fuera_catalogo_rechaza():
    with pytest.raises(ValueError):
        crear_pelicula(genero="Western")


# Gherkin
def test_gherkin_registrar_pelicula_valida(service):
    pelicula = service.registrar(**pelicula_valida_kwargs())
    assert pelicula.titulo == "Matrix"
    assert any(p.titulo == "Matrix" for p in service.listar())


def test_gherkin_rechazar_duracion_fuera_rango(service):
    with pytest.raises(ValueError):
        service.registrar(
            titulo="Corta",
            genero="Comedia",
            duracion=0,
        )
    assert service.listar() == []


def test_gherkin_evitar_duplicidad_titulo(service):
    service.registrar(**pelicula_valida_kwargs())
    with pytest.raises(ValueError):
        service.registrar(
            titulo=" matrix ",
            genero="Ciencia Ficcion",
            duracion=136,
        )
    assert len(service.listar()) == 1


def test_gherkin_editar_pelicula(service):
    service.registrar(**pelicula_valida_kwargs())
    pelicula = service.actualizar("Matrix", duracion=140)
    assert pelicula.duracion == 140
    assert service.listar()[0].duracion == 140


def test_gherkin_eliminar_pelicula_sin_funciones(service):
    service.registrar(**pelicula_valida_kwargs())
    service.eliminar("Matrix")
    assert service.listar() == []


def test_gherkin_bloquear_eliminacion_con_funciones(service):
    service.registrar(**pelicula_valida_kwargs())
    service.asociar_funcion("Matrix")
    with pytest.raises(ValueError):
        service.eliminar("Matrix")
    assert len(service.listar()) == 1
