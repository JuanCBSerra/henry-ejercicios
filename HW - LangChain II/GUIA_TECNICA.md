# 📖 GUÍA DETALLADA DE FUNCIONAMIENTO INTERNO

## 🎯 Tabla de Contenidos
1. [Flujo Completo de una Consulta](#flujo-completo)
2. [Clasificador en Detalle](#clasificador)
3. [Sistema RAG Explicado](#rag)
4. [Búsqueda en CSV](#csv)
5. [Conceptos Técnicos](#conceptos)

---

## 🔄 Flujo Completo de una Consulta

### **Ejemplo Real: "¿Cuál es el balance de V-91827364?"**

#### **Paso 1: Usuario ingresa consulta**
```
👤 Input del usuario: "¿Cuál es el balance de V-91827364?"
```

#### **Paso 2: Clasificación (LLM)**
```python
# El sistema envía al LLM un prompt con ejemplos (few-shot learning)
Prompt al LLM:
"""
Eres un clasificador. Clasifica esto:
"¿Cuál es el balance de V-91827364?"

Ejemplos:
- "balance de V-12345" → balance
- "cómo abro cuenta" → knowledge
- "sentido de la vida" → fuera_contexto
"""

# LLM responde:
"balance"
```

#### **Paso 3: Extracción de datos**
```python
# El sistema usa regex para extraer la cédula
import re
cedula = re.search(r'V-\d+', consulta).group(0)
# Resultado: "V-91827364"
```

#### **Paso 4: Búsqueda en CSV**
```python
# Pandas busca en el DataFrame
resultado = df_saldos[df_saldos['ID_Cedula'] == 'V-91827364']

# Encuentra:
# ID_Cedula     | Nombre      | Balance
# V-91827364    | Luis Méndez | 2580.0
```

#### **Paso 5: Formateo de respuesta**
```python
respuesta = f"""
✅ Información encontrada:
👤 Titular: Luis Méndez
🆔 Cédula: V-91827364
💰 Balance: $2,580.00
"""
```

#### **Paso 6: Usuario recibe respuesta**
```
🤖 Bot muestra la respuesta formateada
```

---

## 🧠 Clasificador en Detalle

### **¿Cómo decide el clasificador?**

El clasificador usa **Few-Shot Learning**: le damos ejemplos al LLM para que aprenda el patrón.

```python
template = """
Clasifica en: "balance", "knowledge", "fuera_contexto"

EJEMPLOS (Few-Shot):
- "balance de V-12345" → balance
- "cómo abrir cuenta" → knowledge  
- "sentido de la vida" → fuera_contexto

CONSULTA: {consulta}
CATEGORÍA:
"""
```

### **Ventajas de usar LLM para clasificación**

✅ **Flexible:** Entiende variaciones ("saldo", "balance", "cuánto tengo")
✅ **Inteligente:** Detecta contexto ("V-12345" indica consulta de balance)
✅ **Fácil de ajustar:** Solo cambiamos el prompt, no entrenamos modelo

### **Alternativas descartadas**

❌ **Reglas fijas (if/else):** Muy rígido
❌ **Modelo ML entrenado:** Requiere datos de entrenamiento
✅ **LLM + Few-Shot:** Balance perfecto

---

## 📚 Sistema RAG Explicado

### **¿Qué es RAG?**

**RAG = Retrieval (Recuperar) + Augmented (Aumentado) + Generation (Generación)**

Es como tener un asistente que:
1. **Busca** en documentos relevantes (Retrieval)
2. **Lee** y entiende la información (Augmented)
3. **Escribe** una respuesta natural (Generation)

### **Flujo RAG Detallado**

#### **Ejemplo: "¿Cómo abro una cuenta?"**

**1. Usuario pregunta:**
```
👤 "¿Cómo abro una cuenta?"
```

**2. Embedding de la pregunta:**
```python
# Convertimos la pregunta a vector
pregunta_vector = embedding_model.encode("¿Cómo abro una cuenta?")
# Resultado: [0.23, -0.45, 0.67, ...] (384 dimensiones)
```

**3. Búsqueda en FAISS:**
```python
# FAISS busca los vectores más similares
docs = vector_store.similarity_search(pregunta, k=2)

# Encuentra 2 documentos:
# Doc 1: nueva_cuenta.txt (similitud: 0.92)
# Doc 2: tarjeta_credito.txt (similitud: 0.65)
```

**4. Construcción del contexto:**
```python
contexto = """
DOCUMENTO 1 (nueva_cuenta.txt):
Para abrir una cuenta en BANCO HENRY:
1. Visita la página web...
2. Completa el formulario...
[...resto del documento...]

DOCUMENTO 2 (tarjeta_credito.txt):
Para solicitar una tarjeta...
[...contenido...]
"""
```

**5. Generación de respuesta:**
```python
prompt = f"""
Eres asistente del BANCO HENRY.

INFORMACIÓN DISPONIBLE:
{contexto}

PREGUNTA DEL CLIENTE:
¿Cómo abro una cuenta?

Responde de forma clara usando la información.
"""

# LLM genera respuesta natural basada en el contexto
```

**6. Usuario recibe respuesta:**
```
🤖 Para abrir una cuenta en BANCO HENRY, sigue estos pasos:
1. Visita la página web y haz clic en "Abrir Cuenta"
2. Elige el tipo de cuenta (Ahorros, Corriente, etc.)
[...continúa con información del documento...]
```

### **¿Por qué RAG es mejor que LLM solo?**

| Aspecto | LLM Solo | RAG |
|---------|----------|-----|
| **Información actualizada** | ❌ Solo conocimiento hasta fecha de entrenamiento | ✅ Usa documentos actuales |
| **Información específica** | ❌ Puede alucinar datos | ✅ Cita documentos reales |
| **Fuentes** | ❌ No puede citar | ✅ Sabemos de dónde viene la info |
| **Control** | ❌ Difícil controlar qué sabe | ✅ Controlamos los documentos |

---

## 💾 Búsqueda en CSV

### **¿Cómo funciona la búsqueda?**

Usamos **Pandas**, la biblioteca estándar de Python para datos tabulares.

#### **Estructura del CSV**

```csv
ID_Cedula,Nombre,Balance
V-12345678,Juan Pérez,1250.5
V-87654321,María Gómez,6820.75
V-91827364,Luis Méndez,2580.0
```

#### **Proceso de búsqueda**

```python
# 1. Cargar CSV en memoria
df_saldos = pd.read_csv("data/saldos.csv")

# 2. Buscar por cédula
resultado = df_saldos[df_saldos['ID_Cedula'] == 'V-91827364']

# 3. Verificar si existe
if resultado.empty:
    return "No encontrado"
else:
    # 4. Extraer datos
    nombre = resultado.iloc[0]['Nombre']
    balance = resultado.iloc[0]['Balance']
    
    # 5. Formatear respuesta
    return f"Titular: {nombre}, Balance: ${balance:,.2f}"
```

### **Manejo de Errores**

```python
# Cédula no encontrada
if resultado.empty:
    return "⚠️ No se encontró información para la cédula V-99999999"

# Cédula mal formateada
if not re.match(r'V-\d+', cedula):
    return "⚠️ Formato de cédula inválido. Usa V-XXXXXXXX"
```

---

## 🔧 Conceptos Técnicos

### **1. Few-Shot Learning**

**Definición:** Enseñar al modelo con pocos ejemplos en el prompt.

**Ejemplo en nuestro código:**
```python
"""
Clasifica en una categoría:

EJEMPLOS:
- "balance de V-12345" → balance
- "cómo abrir cuenta" → knowledge

CONSULTA: {nueva_consulta}
"""
```

**Ventajas:**
- No requiere reentrenamiento
- Rápido de implementar
- Fácil de ajustar

### **2. Embeddings (Vectores Semánticos)**

**Concepto:** Representar texto como números que capturan significado.

```python
# Palabras similares tienen vectores similares
embedding("gato")  = [0.8, 0.2, -0.5, ...]
embedding("gatito") = [0.7, 0.3, -0.4, ...]  # Muy similar

embedding("perro")  = [0.6, 0.1, -0.3, ...]  # Algo similar (animal)
embedding("casa")   = [-0.2, 0.9, 0.1, ...]  # Muy diferente
```

**Similitud Coseno:**
Medida matemática de qué tan similares son dos vectores.
```
similitud("gato", "gatito") = 0.95  # Muy similar
similitud("gato", "casa")   = 0.12  # Poco similar
```

### **3. Índice Vectorial (FAISS)**

**Problema:** Calcular similitud entre millones de vectores es lento.
**Solución:** FAISS crea un índice optimizado para búsquedas rápidas.

```python
# Sin índice (búsqueda lineal): O(n) - lento
for doc in todos_los_documentos:
    calcular_similitud(consulta, doc)

# Con FAISS (búsqueda aproximada): O(log n) - rapidísimo
faiss.search(consulta_vector, k=2)  # Milisegundos
```

**Tipos de índices FAISS:**
- `IndexFlatL2`: Búsqueda exacta, más lento
- `IndexIVFFlat`: Búsqueda aproximada, más rápido
- `IndexHNSW`: El más rápido para datasets grandes

### **4. Prompt Engineering**

**Definición:** Arte de escribir prompts efectivos para LLMs.

**Técnicas usadas en nuestro proyecto:**

#### **a) Few-Shot Prompting**
```python
# Damos ejemplos para que aprenda
"Ejemplos: ..."
```

#### **b) Chain of Thought (Implícito)**
```python
# Guiamos el razonamiento
"Analiza la consulta..."
"Determina la categoría..."
```

#### **c) Restricciones claras**
```python
# Limitamos las respuestas posibles
"Responde ÚNICAMENTE: balance, knowledge o fuera_contexto"
```

#### **d) Contexto de rol**
```python
# Definimos personalidad
"Eres un asistente del BANCO HENRY..."
```

### **5. Token y Context Window**

**Token:** Unidad básica de texto para un LLM.
```
"Hola mundo" = ~2 tokens
"¿Cómo abrir una cuenta?" = ~6 tokens
```

**Context Window:** Máximo de tokens que el LLM puede procesar.
```
llama-3.3-70b: ~8,000 tokens
GPT-4: ~128,000 tokens
```

**En nuestro proyecto:**
- Documentos largos se dividen en chunks (500 caracteres)
- Solo enviamos los 2 documentos más relevantes al LLM
- Mantenemos el contexto bajo el límite

---

## 🎓 Glosario de Términos

| Término | Definición | Ejemplo en el proyecto |
|---------|-----------|------------------------|
| **LLM** | Large Language Model - Modelo de IA que entiende/genera texto | Groq llama-3.3-70b |
| **RAG** | Retrieval-Augmented Generation - Combina búsqueda + generación | Sistema de knowledge base |
| **Embedding** | Vector numérico que representa significado de texto | [0.23, -0.45, 0.67, ...] |
| **FAISS** | Biblioteca de Meta para búsqueda vectorial rápida | Busca docs similares |
| **Few-Shot** | Enseñar con pocos ejemplos en el prompt | Ejemplos de clasificación |
| **Vector Store** | Base de datos de vectores | Índice FAISS |
| **Retriever** | Componente que busca documentos relevantes | `vector_store.as_retriever()` |
| **Token** | Unidad de texto para el LLM | ~4 caracteres |
| **Prompt** | Instrucciones que le damos al LLM | Template con contexto |
| **Chain** | Secuencia de operaciones en LangChain | `prompt \| llm \| parser` |

---

## 🔍 Debugging y Entendimiento

### **¿Cómo ver qué está pasando internamente?**

El código incluye **logging detallado**:

```python
# Muestra la clasificación
print(f"✅ Categoría identificada: {categoria.upper()}")

# Muestra qué herramienta se ejecuta
print(f"🎯 Ejecutando herramienta para categoría: {categoria}")

# Muestra búsquedas
print(f"🔍 Buscando balance para cédula: {cedula}")
print(f"📚 Buscando en base de conocimientos: '{pregunta}'")
```

### **¿Cómo probar cada componente?**

```bash
# Probar indexer
python indexer.py

# Probar sistema completo
python main.py

# Probar con casos predefinidos
python test_system.py
```

---

## 💡 Tips y Mejores Prácticas

### **Para Desarrolladores**

1. **Siempre ejecuta `indexer.py` primero**
   - Sin el índice, el sistema RAG no funciona

2. **Revisa los logs**
   - El sistema muestra qué categoría detectó
   - Útil para debugging

3. **Prueba casos edge**
   - Cédulas inexistentes
   - Preguntas ambiguas
   - Formato incorrecto

### **Para Mejorar el Sistema**

1. **Agregar más documentos a `knowledge_base/`**
   - Más info = mejores respuestas RAG

2. **Ajustar el prompt de clasificación**
   - Más ejemplos = mejor precisión

3. **Cambiar `k` en el retriever**
   - `k=2`: Busca 2 documentos
   - `k=5`: Busca 5 documentos (más contexto, pero más tokens)

---

## 📚 Recursos para Aprender Más

1. **LangChain Docs:** https://python.langchain.com/
2. **FAISS Docs:** https://faiss.ai/
3. **Sentence Transformers:** https://www.sbert.net/
4. **RAG Explained:** https://docs.llamaindex.ai/en/stable/getting_started/concepts.html
5. **Groq API:** https://console.groq.com/docs

---

**¿Preguntas?** Revisa el `README_PROYECTO.md` o ejecuta `python test_system.py` para validar que todo funcione.
