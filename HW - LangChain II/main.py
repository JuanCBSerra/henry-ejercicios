"""
Sistema de Atención al Cliente Automatizado con LangChain

Este sistema clasifica automáticamente las consultas de clientes y las enruta a:
1. Consulta de CSV - Para balances de cuenta por cédula
2. Base de conocimientos (RAG) - Para información sobre procesos bancarios
3. Rechazo cortés - Para preguntas fuera del contexto bancario

Flujo:
1. Usuario hace una pregunta
2. Router/Clasificador determina el tipo de consulta
3. Se ejecuta la herramienta apropiada o se rechaza si no es bancaria
4. Se retorna la respuesta al usuario
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Imports de LangChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Cargar variables de entorno
load_dotenv()

# Configuración
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CSV_PATH = "data/saldos.csv"
INDEX_PATH = "index"
KNOWLEDGE_BASE_PATH = "knowledge_base"

# Verificar API key
if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY no está configurada en el archivo .env")

print("=" * 70)
print("🏦 SISTEMA DE ATENCIÓN AL CLIENTE - BANCO HENRY")
print("=" * 70)
print()

# ============================================================================
# 1. INICIALIZACIÓN DE COMPONENTES
# ============================================================================

print("🔧 Inicializando componentes...")

# LLM - Usando Groq (rápido y gratuito)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY
)
print("   ✅ LLM inicializado (Groq - llama-3.3-70b-versatile)")

# Cargar CSV de balances
df_saldos = pd.read_csv(CSV_PATH)
print(f"   ✅ CSV cargado: {len(df_saldos)} registros")

# Cargar índice FAISS (base de conocimientos vectorial)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
vector_store = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
print("   ✅ Base de conocimientos vectorial cargada")

print()

# ============================================================================
# 2. HERRAMIENTAS (TOOLS)
# ============================================================================

def consultar_balance(cedula: str) -> str:
    """
    Herramienta 1: Consulta balance de cuenta en el CSV
    
    Args:
        cedula: ID de cédula (ejemplo: V-12345678)
    
    Returns:
        Información del balance o mensaje de error
    """
    print(f"   🔍 Buscando balance para cédula: {cedula}")
    
    # Buscar en el DataFrame
    resultado = df_saldos[df_saldos['ID_Cedula'] == cedula]
    
    if resultado.empty:
        return f"⚠️ No se encontró información para la cédula {cedula}. Verifique que el número de cédula sea correcto."
    
    # Extraer datos
    nombre = resultado.iloc[0]['Nombre']
    balance = resultado.iloc[0]['Balance']
    
    return f"""✅ Información de cuenta encontrada:

👤 Titular: {nombre}
🆔 Cédula: {cedula}
💰 Balance: ${balance:,.2f}

¿Necesitas algo más?"""


def consultar_knowledge_base(pregunta: str) -> str:
    """
    Herramienta 2: Consulta en la base de conocimientos usando RAG
    
    Args:
        pregunta: Pregunta sobre procesos bancarios
    
    Returns:
        Respuesta generada usando contexto de documentos
    """
    print(f"   📚 Buscando en base de conocimientos: '{pregunta[:50]}...'")
    
    # Recuperar documentos relevantes
    docs = retriever.invoke(pregunta)
    
    # Construir contexto
    contexto = "\n\n".join([doc.page_content for doc in docs])
    
    # Prompt para RAG
    template = """Eres un asistente del BANCO HENRY. Usa la siguiente información para responder la pregunta del cliente de manera clara y profesional.

INFORMACIÓN DISPONIBLE:
{contexto}

PREGUNTA DEL CLIENTE:
{pregunta}

RESPUESTA:
Proporciona una respuesta clara, paso a paso si es necesario, usando la información proporcionada. Si la información no es suficiente, indícalo cortésmente."""

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    respuesta = chain.invoke({
        "contexto": contexto,
        "pregunta": pregunta
    })
    
    return respuesta


# ============================================================================
# 3. ROUTER / CLASIFICADOR DE CONSULTAS
# ============================================================================

def clasificar_consulta(consulta: str) -> str:
    """
    Clasifica la consulta del usuario en una de estas categorías:
    - "balance": Consultas sobre saldos de cuenta
    - "knowledge": Preguntas sobre procesos bancarios
    - "fuera_contexto": Preguntas que NO son sobre temas bancarios
    
    Args:
        consulta: Pregunta del usuario
    
    Returns:
        Categoría de la consulta
    """
    print(f"\n🔄 Clasificando consulta: '{consulta[:60]}...'")
    
    template = """Eres un clasificador de consultas bancarias del BANCO HENRY. Debes clasificar la consulta en UNA de estas categorías:

CATEGORÍAS:
1. "balance" - Si la consulta pregunta por el balance, saldo o dinero de una cuenta, Y menciona una cédula o ID
2. "knowledge" - Si pregunta sobre procesos bancarios como: abrir cuentas, solicitar tarjetas, hacer transferencias, requisitos, pasos, horarios del banco, tasas de interés, servicios bancarios, etc.
3. "fuera_contexto" - Si la pregunta NO tiene nada que ver con temas bancarios o financieros

EJEMPLOS:
- "¿Cuál es el balance de la cuenta V-12345678?" -> balance
- "¿Cuál es el saldo de la cédula V-87654321?" -> balance
- "¿Cómo abro una cuenta de ahorros?" -> knowledge
- "¿Qué necesito para solicitar una tarjeta de crédito?" -> knowledge
- "¿Qué horario tiene el banco?" -> knowledge
- "¿Cuál es la tasa de interés?" -> knowledge
- "¿Cuál es el sentido de la vida?" -> fuera_contexto
- "¿Qué día es hoy?" -> fuera_contexto
- "¿Quién ganó el mundial de fútbol?" -> fuera_contexto
- "¿Cómo se hace una pizza?" -> fuera_contexto

IMPORTANTE:
- Responde ÚNICAMENTE con una palabra: "balance", "knowledge" o "fuera_contexto"
- NO agregues explicaciones ni puntuación
- Si la pregunta no es sobre banca/finanzas, SIEMPRE clasifícala como "fuera_contexto"

CONSULTA DEL USUARIO:
{consulta}

CATEGORÍA:"""

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    categoria = chain.invoke({"consulta": consulta}).strip().lower()
    
    # Validar categoría
    if categoria not in ["balance", "knowledge", "fuera_contexto"]:
        print(f"   ⚠️ Categoría no válida: '{categoria}', usando 'fuera_contexto' por defecto")
        categoria = "fuera_contexto"
    
    print(f"   ✅ Categoría identificada: {categoria.upper()}")
    
    return categoria


# ============================================================================
# 4. PROCESADOR PRINCIPAL
# ============================================================================

def procesar_consulta(consulta: str) -> str:
    """
    Función principal que procesa la consulta del usuario
    
    Args:
        consulta: Pregunta del usuario
    
    Returns:
        Respuesta apropiada según el tipo de consulta
    """
    # Paso 1: Clasificar la consulta
    categoria = clasificar_consulta(consulta)
    
    # Paso 2: Ejecutar la herramienta apropiada
    print(f"   🎯 Ejecutando herramienta para categoría: {categoria}")
    
    if categoria == "balance":
        # Extraer cédula de la consulta
        # Buscar patrón V-XXXXXXXX en la consulta
        import re
        match = re.search(r'V-\d+', consulta)
        
        if match:
            cedula = match.group(0)
            return consultar_balance(cedula)
        else:
            return "⚠️ No se pudo identificar el número de cédula en tu consulta. Por favor, proporciona la cédula en formato V-XXXXXXXX"
    
    elif categoria == "knowledge":
        return consultar_knowledge_base(consulta)
    
    else:  # fuera_contexto
        return """⚠️ Lo siento, solo puedo ayudarte con consultas relacionadas con servicios bancarios del BANCO HENRY.

Puedo asistirte con:
• Consultas de balance de cuentas (necesito tu número de cédula)
• Información sobre cómo abrir cuentas
• Solicitud de tarjetas de crédito
• Procesos de transferencias
• Otros servicios bancarios

¿En qué servicio bancario puedo ayudarte?"""


# ============================================================================
# 5. INTERFAZ DE USUARIO (CLI)
# ============================================================================

def main():
    """
    Función principal - Interfaz de línea de comandos
    """
    print("=" * 70)
    print("💬 Chat iniciado - Escribe 'salir' o 'exit' para terminar")
    print("=" * 70)
    print()
    
    # Ejemplos de consultas para probar
    print("📝 Ejemplos de consultas que puedes hacer:")
    print("   • ¿Cuál es el balance de la cuenta de la cédula V-91827364?")
    print("   • ¿Cómo abro una cuenta de ahorros en el banco?")
    print("   • ¿Cómo solicito una tarjeta de crédito?")
    print("   • ¿Qué horarios tiene el banco?")
    print()
    print("⚠️  NOTA: Solo respondo preguntas relacionadas con servicios bancarios")
    print()
    print("-" * 70)
    print()
    
    while True:
        try:
            # Leer entrada del usuario
            consulta = input("👤 Usuario: ").strip()
            
            # Verificar si quiere salir
            if consulta.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Gracias por usar nuestro sistema! Hasta pronto.")
                break
            
            # Verificar que no esté vacío
            if not consulta:
                print("⚠️ Por favor, escribe una consulta.\n")
                continue
            
            # Procesar la consulta
            respuesta = procesar_consulta(consulta)
            
            # Mostrar respuesta
            print(f"\n🤖 Asistente:\n{respuesta}\n")
            print("-" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


# ============================================================================
# 6. MODO DE PRUEBA (DESCOMENTAR PARA TESTING)
# ============================================================================

def modo_prueba():
    """
    Función de prueba con consultas predefinidas
    Útil para validar que todo funcione correctamente
    """
    print("\n" + "=" * 70)
    print("🧪 MODO DE PRUEBA - Ejecutando consultas de ejemplo")
    print("=" * 70)
    
    consultas_prueba = [
        "¿Cuál es el balance de la cuenta de la cédula V-91827364?",
        "¿Cómo abro una cuenta de ahorros en el banco?",
        "¿Cuál es el sentido de la vida?"  # Esta debe ser rechazada
    ]
    
    for i, consulta in enumerate(consultas_prueba, 1):
        print(f"\n{'='*70}")
        print(f"PRUEBA {i}/3")
        print(f"{'='*70}")
        print(f"👤 Consulta: {consulta}")
        
        respuesta = procesar_consulta(consulta)
        
        print(f"\n🤖 Respuesta:\n{respuesta}")
        print()


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    # Modo normal (interactivo)
    main()
    
    # Para ejecutar modo de prueba en lugar del interactivo, comenta la línea anterior y descomenta la siguiente:
    # modo_prueba()
