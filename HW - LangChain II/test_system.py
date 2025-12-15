"""
Script de Pruebas Automatizadas
Valida que los tres flujos de trabajo funcionen correctamente
"""

import sys
from main import procesar_consulta, llm, df_saldos, vector_store

print("=" * 70)
print("🧪 SISTEMA DE PRUEBAS AUTOMATIZADAS")
print("=" * 70)
print()

# Contador de pruebas
pruebas_totales = 0
pruebas_exitosas = 0

def prueba(nombre, consulta, validacion_fn):
    """
    Ejecuta una prueba y valida el resultado
    
    Args:
        nombre: Nombre descriptivo de la prueba
        consulta: Consulta a probar
        validacion_fn: Función que valida si la respuesta es correcta
    """
    global pruebas_totales, pruebas_exitosas
    pruebas_totales += 1
    
    print(f"\n{'='*70}")
    print(f"PRUEBA {pruebas_totales}: {nombre}")
    print(f"{'='*70}")
    print(f"📝 Consulta: {consulta}")
    print()
    
    try:
        respuesta = procesar_consulta(consulta)
        print(f"\n✅ Respuesta recibida ({len(respuesta)} caracteres)")
        print(f"📄 Contenido: {respuesta[:200]}...")
        
        if validacion_fn(respuesta):
            print("\n✅ PRUEBA EXITOSA")
            pruebas_exitosas += 1
            return True
        else:
            print("\n❌ PRUEBA FALLIDA: Validación no pasó")
            return False
            
    except Exception as e:
        print(f"\n❌ PRUEBA FALLIDA: {e}")
        return False


# ============================================================================
# PRUEBA 1: Consulta de Balance en CSV
# ============================================================================

def validar_balance(respuesta):
    """Valida que la respuesta contenga información de balance"""
    return (
        "Luis Méndez" in respuesta and
        "V-91827364" in respuesta and
        "2,580" in respuesta
    )

prueba(
    "Consulta de Balance - CSV",
    "¿Cuál es el balance de la cuenta de la cédula V-91827364?",
    validar_balance
)


# ============================================================================
# PRUEBA 2: Información de Knowledge Base - RAG
# ============================================================================

def validar_knowledge(respuesta):
    """Valida que la respuesta contenga pasos para abrir cuenta"""
    keywords = ["cuenta", "banco", "paso", "formulario"]
    return any(keyword.lower() in respuesta.lower() for keyword in keywords)

prueba(
    "Información Bancaria - RAG",
    "¿Cómo abro una cuenta de ahorros en el banco?",
    validar_knowledge
)


# ============================================================================
# PRUEBA 3: Rechazo de Consultas Fuera de Contexto
# ============================================================================

def validar_rechazo(respuesta):
    """Valida que rechace preguntas no bancarias"""
    keywords = ["solo puedo", "servicio", "bancari", "banco"]
    return any(keyword.lower() in respuesta.lower() for keyword in keywords)

prueba(
    "Rechazo de Pregunta No Bancaria",
    "¿Cuál es el sentido de la vida?",
    validar_rechazo
)


# ============================================================================
# PRUEBA 4: Manejo de Cédula No Encontrada
# ============================================================================

def validar_no_encontrada(respuesta):
    """Valida que maneje correctamente cédula inexistente"""
    return "no se encontró" in respuesta.lower() or "no encontrada" in respuesta.lower()

prueba(
    "Cédula No Encontrada - Error Handling",
    "¿Cuál es el balance de V-99999999?",
    validar_no_encontrada
)


# ============================================================================
# PRUEBA 5: Otra Consulta de Knowledge Base
# ============================================================================

def validar_tarjeta(respuesta):
    """Valida información sobre tarjeta de crédito"""
    keywords = ["tarjeta", "crédito", "solicitar", "banca"]
    return any(keyword.lower() in respuesta.lower() for keyword in keywords)

prueba(
    "Información Tarjeta - RAG",
    "¿Cómo solicito una tarjeta de crédito?",
    validar_tarjeta
)


# ============================================================================
# REPORTE FINAL
# ============================================================================

print("\n" + "=" * 70)
print("📊 REPORTE FINAL DE PRUEBAS")
print("=" * 70)
print(f"Total de pruebas: {pruebas_totales}")
print(f"Pruebas exitosas: {pruebas_exitosas}")
print(f"Pruebas fallidas: {pruebas_totales - pruebas_exitosas}")
print(f"Porcentaje de éxito: {(pruebas_exitosas/pruebas_totales)*100:.1f}%")
print()

if pruebas_exitosas == pruebas_totales:
    print("✅ ¡TODAS LAS PRUEBAS PASARON!")
    print("🎉 El sistema está funcionando correctamente")
    sys.exit(0)
else:
    print("⚠️ ALGUNAS PRUEBAS FALLARON")
    print("🔍 Revisa los logs anteriores para más detalles")
    sys.exit(1)
