from pathlib import Path
import sys
import tempfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from models.funcion import Funcion
from services.funcion_service import FuncionService


def funcion_valida_kwargs():
    return {
        "pelicula": 1,
        "sala": 1,
        "fecha": "2026-06-01",
        "hora": "18:30",
        "precio": 15.0,
    }


@pytest.fixture
def service():
    with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
        yield FuncionService(str(Path(tempdir) / "funciones.json"))


def crear_funcion(**overrides):
    data = funcion_valida_kwargs()
    data.update(overrides)
    return Funcion(**data)


# PE
def test_pe_funcion_valida_acepta_creacion():
    funcion = crear_funcion()
    assert funcion.pelicula == 1
    assert funcion.sala == 1
    assert funcion.fecha == "2026-06-01"
    assert funcion.hora == "18:30"
    assert funcion.precio == 15.0


def test_pe_pelicula_vacia_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(pelicula=None)


def test_pe_sala_vacia_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(sala=None)


def test_pe_fecha_vacia_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(fecha="")


def test_pe_hora_vacia_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(hora="")


def test_pe_precio_negativo_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(precio=-1)


def test_pe_precio_cero_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(precio=0)


# AVL
def test_avl_precio_minimo_valido():
    funcion = crear_funcion(precio=0.01)
    assert funcion.precio == 0.01


def test_avl_precio_justo_debajo_del_minimo_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(precio=0)


def test_avl_fecha_limite_inferior_valida():
    funcion = crear_funcion(fecha="1900-01-01")
    assert funcion.fecha == "1900-01-01"


def test_avl_fecha_limite_superior_valida():
    funcion = crear_funcion(fecha="9999-12-31")
    assert funcion.fecha == "9999-12-31"


def test_avl_fecha_formato_invalido_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(fecha="2026/06/01")


def test_avl_hora_limite_inferior_valida():
    funcion = crear_funcion(hora="00:00")
    assert funcion.hora == "00:00"


def test_avl_hora_limite_superior_valida():
    funcion = crear_funcion(hora="23:59")
    assert funcion.hora == "23:59"


def test_avl_hora_fuera_de_limite_rechaza():
    with pytest.raises(ValueError):
        crear_funcion(hora="24:00")


# Gherkin
def test_gherkin_registrar_funcion_correctamente(service):
    funcion = service.crear_funcion(**funcion_valida_kwargs())
    assert funcion.id_funcion == 1
    assert len(service.obtener_todas()) == 1


def test_gherkin_registrar_funcion_con_precio_invalido(service):
    datos = funcion_valida_kwargs()
    datos["precio"] = 0
    with pytest.raises(ValueError):
        service.crear_funcion(**datos)
    assert service.obtener_todas() == []


def test_gherkin_registrar_funcion_sin_pelicula(service):
    datos = funcion_valida_kwargs()
    datos["pelicula"] = None
    with pytest.raises(ValueError):
        service.crear_funcion(**datos)


def test_gherkin_listar_funciones_registradas(service):
    service.crear_funcion(**funcion_valida_kwargs())
    assert len(service.obtener_todas()) == 1


def test_gherkin_actualizar_funcion_existente(service):
    funcion = service.crear_funcion(**funcion_valida_kwargs())
    actualizada = service.actualizar_funcion(
        funcion.id_funcion,
        pelicula=1,
        sala=1,
        fecha="2026-06-02",
        hora="20:00",
        precio=18.5,
    )
    assert actualizada.fecha == "2026-06-02"
    assert actualizada.hora == "20:00"
    assert actualizada.precio == 18.5


def test_gherkin_eliminar_funcion_existente(service):
    funcion = service.crear_funcion(**funcion_valida_kwargs())
    eliminada = service.eliminar_funcion(funcion.id_funcion)
    assert eliminada.id_funcion == funcion.id_funcion
    assert service.obtener_todas() == []
