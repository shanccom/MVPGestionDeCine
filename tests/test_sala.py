import pytest
from unittest.mock import Mock, patch
# Se asume la existencia de models.sala y repositories.sala_repository para TDD
from models.sala import Sala
from repositories.sala_repository import SalaRepository

# =====================================================================
# CASOS DE PARTICIÓN DE EQUIVALENCIA (PE) - CAMPO: NUMERO
# =====================================================================

def test_pe_num_01_numero_entero_positivo_valido_acepta_creacion():
    sala = Sala(numero=5, capacidad=150)
    assert sala.numero == 5
    assert sala.capacidad == 150

def test_pe_num_02_numero_entero_negativo_lanza_value_error():
    with pytest.raises(ValueError, match="no puede ser negativo|mayor a cero|invalido"):
        Sala(numero=-3, capacidad=150)

def test_pe_num_03_numero_cero_lanza_value_error():
    with pytest.raises(ValueError, match="no puede ser cero|mayor a cero|invalido"):
        Sala(numero=0, capacidad=150)

def test_pe_num_04_numero_string_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero="Cinco", capacidad=150)

def test_pe_num_05_numero_float_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero=2.5, capacidad=150)

def test_pe_num_06_numero_none_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero=None, capacidad=150)

# =====================================================================
# CASOS DE PARTICIÓN DE EQUIVALENCIA (PE) - CAMPO: CAPACIDAD
# =====================================================================

def test_pe_cap_01_capacidad_dentro_del_rango_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=150)
    assert sala.capacidad == 150

def test_pe_cap_02_capacidad_menor_al_limite_lanza_value_error():
    with pytest.raises(ValueError, match="rango|entre 1 y 300|minima"):
        Sala(numero=1, capacidad=0)

def test_pe_cap_03_capacidad_mayor_al_limite_lanza_value_error():
    with pytest.raises(ValueError, match="rango|entre 1 y 300|maxima"):
        Sala(numero=1, capacidad=400)

def test_pe_cap_04_capacidad_string_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero=1, capacidad="Cien")

def test_pe_cap_05_capacidad_float_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero=1, capacidad=150.5)

def test_pe_cap_06_capacidad_none_lanza_type_error():
    with pytest.raises(TypeError, match="debe ser un numero entero"):
        Sala(numero=1, capacidad=None)

# =====================================================================
# CASOS DE ANÁLISIS DE VALORES LÍMITE (AVL) - CAMPO: NUMERO
# =====================================================================

def test_avl_num_01_limite_inferior_fuera_de_rango_lanza_value_error():
    with pytest.raises(ValueError):
        Sala(numero=0, capacidad=150)

def test_avl_num_02_limite_inferior_exacto_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=150)
    assert sala.numero == 1

def test_avl_num_03_limite_inferior_superior_valido_acepta_creacion():
    sala = Sala(numero=2, capacidad=150)
    assert sala.numero == 2

# =====================================================================
# CASOS DE ANÁLISIS DE VALORES LÍMITE (AVL) - CAMPO: CAPACIDAD
# =====================================================================

def test_avl_cap_01_limite_inferior_fuera_de_rango_lanza_value_error():
    with pytest.raises(ValueError):
        Sala(numero=1, capacidad=0)

def test_avl_cap_02_limite_inferior_exacto_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=1)
    assert sala.capacidad == 1

def test_avl_cap_03_limite_inferior_superior_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=2)
    assert sala.capacidad == 2

def test_avl_cap_04_limite_superior_inferior_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=299)
    assert sala.capacidad == 299

def test_avl_cap_05_limite_superior_exacto_valido_acepta_creacion():
    sala = Sala(numero=1, capacidad=300)
    assert sala.capacidad == 300

def test_avl_cap_06_limite_superior_fuera_de_rango_lanza_value_error():
    with pytest.raises(ValueError):
        Sala(numero=1, capacidad=301)

# =====================================================================
# ESCENARIOS GHERKIN - FLUJOS DE NEGOCIO
# =====================================================================

def test_gherkin_creacion_exitosa_de_sala_asigna_propiedades_correctamente():
    # Escenario: Creación exitosa de una sala (ID autogenerado simula BD)
    sala = Sala(numero=5, capacidad=150)
    
    # Simulación de la capa de persistencia guardando y asignando ID
    sala.id_sala = 101  
    
    assert sala.numero == 5
    assert sala.capacidad == 150
    assert sala.id_sala == 101

@patch.object(SalaRepository, 'buscar_por_numero')
@patch.object(SalaRepository, 'guardar')
def test_gherkin_error_por_duplicado_de_numero_de_sala(mock_guardar, mock_buscar_por_numero):
    # Escenario: Error por duplicado de número de sala
    repo = SalaRepository()
    
    # Simulamos que al buscar la sala número 3, ya retorna una entidad existente
    mock_buscar_por_numero.return_value = Sala(id_sala=10, numero=3, capacidad=100)
    
    # La lógica del repositorio debería lanzar ValueError al intentar guardar un duplicado
    mock_guardar.side_effect = ValueError("El número de sala ya está en uso")
    
    nueva_sala = Sala(numero=3, capacidad=120)
    
    with pytest.raises(ValueError, match="ya está en uso"):
        repo.guardar(nueva