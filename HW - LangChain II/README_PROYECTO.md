# 🏦 Sistema de Atención al Cliente Automatizado con LangChain

> **Sistema inteligente de atención bancaria con IA que clasifica y responde consultas automáticamente**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.0-green.svg)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 ¿Qué hace este proyecto?

Un **chatbot bancario inteligente** que:
- ✅ Consulta balances de cuenta desde CSV
- ✅ Responde preguntas sobre procesos bancarios usando RAG
- ✅ Rechaza preguntas no bancarias cortésmente
- ✅ Clasifica automáticamente cada consulta

**Tecnologías:** Python + LangChain + Groq (LLM) + FAISS + Sentence Transformers

---

## 🚀 Inicio Rápido

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar API key en .env
GROQ_API_KEY=tu_clave_aqui

# 3. Generar índice
python indexer.py

# 4. Ejecutar
python main.py
```

**👉 [Guía completa de instalación en 5 minutos](INICIO_RAPIDO.md)**

---

## 📋 Descripción General

Sistema inteligente de atención al cliente para el **BANCO HENRY** que utiliza Inteligencia Artificial para clasificar y responder automáticamente consultas bancarias. El sistema enruta cada pregunta a la fuente de información más apropiada:

- **🔍 Consultas de balance**: Extrae información de archivo CSV con datos de cuentas
- **📚 Información bancaria**: Usa RAG (Retrieval-Augmented Generation) con base de conocimientos vectorial para procesos bancarios
- **🚫 Restricción de contexto**: Rechaza cortésmente preguntas que no sean sobre temas bancarios

### **¿Qué hace este sistema?**

Imagina un asistente bancario virtual que puede:
1. **Consultar tu balance** si le das tu número de cédula
2. **Explicar procesos** como abrir cuentas o solicitar tarjetas
3. **Rechazar preguntas** que no estén relacionadas con el banco

**Ejemplo de uso:**
```
👤 Usuario: "¿Cuál es el balance de la cédula V-91827364?"
🤖 Bot: ✅ Balance: $2,580.00 - Titular: Luis Méndez

👤 Usuario: "¿Cómo abro una cuenta?"
🤖 Bot: [Explica paso a paso el proceso]

👤 Usuario: "¿Cuál es el sentido de la vida?"
🤖 Bot: ⚠️ Solo puedo ayudarte con temas bancarios
```

## 🏗️ Arquitectura del Sistema

### **Diagrama de Flujo**

```
┌─────────────────────────────────────────────────────────────┐
│                    👤 USUARIO (CLI)                         │
│            "¿Cuál es mi balance V-91827364?"                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         🧠 CLASIFICADOR / ROUTER (LLM Groq)                 │
│  Analiza la pregunta y determina la categoría:             │
│  • "balance" → Consulta de saldo                            │
│  • "knowledge" → Información bancaria                       │
│  • "fuera_contexto" → Pregunta no bancaria                  │
└────────────┬────────────┬────────────┬─────────────────────┘
             │            │            │
    ┌────────▼────┐  ┌───▼──────┐  ┌──▼──────────────┐
    │  📊 TOOL 1  │  │ 📚 TOOL 2│  │  🚫 RECHAZO     │
    │   Balance   │  │    RAG   │  │  No bancario    │
    │   (Pandas)  │  │  (FAISS) │  │                 │
    └─────────────┘  └──────────┘  └─────────────────┘
         │               │                   │
         ▼               ▼                   ▼
    saldos.csv    knowledge_base/    Mensaje cortés
    (10 cuentas)   (3 documentos)    de rechazo
                   + embeddings
```

### **Flujo Detallado Paso a Paso**

1. **Usuario escribe consulta** → CLI captura input
2. **Clasificador analiza** → LLM determina categoría usando few-shot prompting
3. **Sistema ejecuta acción apropiada:**
   - **Balance:** Busca cédula en CSV con Pandas → Retorna datos
   - **Knowledge:** Busca en FAISS (k=2) → Genera respuesta con RAG
   - **Fuera de contexto:** Retorna mensaje de rechazo cortés
4. **Usuario recibe respuesta** → Formateada y profesional

## 🔧 Componentes Principales

### **📄 1. indexer.py - Generador de Base de Conocimientos**

**¿Qué hace?**
Convierte documentos de texto en una base de datos de vectores para búsqueda semántica ultrarrápida.

**Proceso:**
1. **Lee archivos** de `knowledge_base/` (nueva_cuenta.txt, tarjeta_credito.txt, etc.)
2. **Genera embeddings** usando el modelo `sentence-transformers/all-MiniLM-L6-v2`
   - Convierte texto en vectores numéricos que representan el significado
   - Por ejemplo: "abrir cuenta" se convierte en [0.23, -0.45, 0.67, ...]
3. **Crea índice FAISS** - Base de datos vectorial optimizada para búsquedas
4. **Guarda en disco** (`index/`) para reutilización

**¿Por qué es importante?**
Sin este paso, no podríamos hacer búsquedas semánticas. FAISS permite encontrar documentos relevantes en milisegundos.

**Ejecutar:**
```bash
python indexer.py
```

**Cuándo ejecutarlo:**
- Primera vez que usas el sistema
- Cuando agregas/modificas archivos en `knowledge_base/`
- Si borras la carpeta `index/`

---

### **🚀 2. main.py - Aplicación Principal**

El corazón del sistema. Contiene:

#### **🔍 Herramienta 1: consultar_balance(cedula)**

**¿Qué hace?**
Busca información de cuenta en el CSV usando el ID de cédula.

**Funcionamiento:**
```python
1. Recibe cédula (ej: "V-91827364")
2. Busca en DataFrame de Pandas
3. Si encuentra → Retorna nombre, cédula y balance
4. Si NO encuentra → Mensaje de error amigable
```

**Ejemplo:**
```
Input: "V-91827364"
Output: 
✅ Información encontrada:
👤 Titular: Luis Méndez
🆔 Cédula: V-91827364
💰 Balance: $2,580.00
```

---

#### **📚 Herramienta 2: consultar_knowledge_base(pregunta)**

**¿Qué hace?**
Sistema RAG (Retrieval-Augmented Generation) completo para información bancaria.

**Funcionamiento paso a paso:**
- Lee archivo `data/saldos.csv`
- Busca por ID de cédula
- Retorna balance y datos del titular

#### **Herramienta 2: consultar_knowledge_base(pregunta)**
- Sistema RAG completo
- Busca documentos relevantes en FAISS
- Genera respuesta contextual con LLM
- Usa información de `knowledge_base/`

#### **Herramienta 3: respuesta_general(pregunta)**
- LLM directo (sin contexto externo)
- Para preguntas generales
- Mantiene contexto bancario

#### **Router: clasificar_consulta(consulta)**
- Usa LLM para clasificación
- Few-shot prompting con ejemplos
- Retorna: "balance", "knowledge" o "general"

## 📁 Estructura de Archivos

```
HW - LangChain II/
├── 📂 data/
│   └── saldos.csv              # Base de datos de balances (10 clientes)
├── 📂 knowledge_base/
│   ├── nueva_cuenta.txt        # Info sobre abrir cuentas
│   ├── tarjeta_credito.txt     # Info sobre tarjetas de crédito
│   └── transferencia.txt       # Info sobre transferencias
├── 📂 index/                   # Base de datos vectorial FAISS (auto-generada)
│   ├── index.faiss
│   └── index.pkl
├── 📂 venv/                    # Entorno virtual Python
├── 📄 .env                     # Configuración (API keys) - NO SUBIR A GIT
├── 📄 .env.example             # Plantilla de configuración
├── 📄 .gitignore               # Archivos ignorados por Git
├── 📄 requirements.txt         # Dependencias Python
├── 📄 indexer.py               # Generador de índice vectorial ⚙️
├── 📄 main.py                  # Aplicación principal 🚀
├── 📄 test_system.py           # Pruebas automatizadas 🧪
├── 📄 README_PROYECTO.md       # Esta documentación 📖
├── 📄 GUIA_TECNICA.md          # Guía técnica detallada 🎓
└── 📄 INICIO_RAPIDO.md         # Setup en 5 minutos ⚡
```

### **📚 Guía de Documentación**

| Documento | ¿Para qué? | ¿Cuándo leerlo? |
|-----------|-----------|-----------------|
| **`INICIO_RAPIDO.md`** | Setup en 5 minutos | ⭐ **Empieza aquí** si es tu primera vez |
| **`README_PROYECTO.md`** | Documentación general | Después del setup, para entender el proyecto |
| **`GUIA_TECNICA.md`** | Funcionamiento interno detallado | Cuando quieras entender cómo funciona cada componente |
| **`README.md`** | Tarea original del curso | Para ver los requisitos originales |

## 🚀 Instalación y Ejecución

### **Prerrequisitos**
- Python 3.10+
- pip
- Cuenta gratuita en Groq (https://console.groq.com/)

### **Paso 1: Clonar/Descargar el proyecto**
```bash
cd "HW - LangChain II"
```

### **Paso 2: Crear entorno virtual**
```bash
python -m venv venv
```

### **Paso 3: Activar entorno virtual**

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### **Paso 4: Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 5: Configurar variables de entorno**
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env y agregar tu API key de Groq
# GROQ_API_KEY=tu_clave_aqui
```

### **Paso 6: Generar índice vectorial**
```bash
python indexer.py
```

Este comando:
- Lee archivos de `knowledge_base/`
- Genera embeddings
- Crea índice FAISS en carpeta `index/`
- Solo necesitas ejecutarlo una vez (o cuando cambies la knowledge base)

### **Paso 7: Ejecutar el sistema**
```bash
python main.py
```

## 🧪 Casos de Prueba

### **Prueba 1: Consulta de Balance**
```
Usuario: ¿Cuál es el balance de la cuenta de la cédula V-91827364?

Clasificación: balance
Herramienta: consultar_balance()
Resultado esperado: Información de Luis Méndez con balance $2,580.00
```

### **Prueba 2: Información Bancaria**
```
Usuario: ¿Cómo abro una cuenta de ahorros en el banco?

Clasificación: knowledge
Herramienta: consultar_knowledge_base() [RAG]
Resultado esperado: Pasos detallados desde knowledge_base/nueva_cuenta.txt
```

### **Prueba 3: Pregunta General**
```
Usuario: ¿Cuál es el sentido de la vida?

Clasificación: general
Herramienta: respuesta_general()
Resultado esperado: Respuesta filosófica del LLM
```

## 🛠️ Tecnologías Utilizadas

### **Stack Tecnológico Completo**

| Tecnología | Propósito | ¿Por qué? | Versión |
|------------|-----------|-----------|---------|
| **Python** | Lenguaje de programación | Ecosistema maduro para IA/ML | 3.12+ |
| **LangChain** | Framework de orquestación | Simplifica integración de LLMs y herramientas | 1.2.0 |
| **Groq** | LLM (llama-3.3-70b) | API gratuita, latencia ultra-baja (~0.5s) | - |
| **FAISS** | Base de datos vectorial | Búsqueda semántica ultrarrápida (usado por Meta) | 1.13.1 |
| **Sentence Transformers** | Generación de embeddings | Modelo local, gratuito, optimizado para búsqueda | 5.2.0 |
| **Pandas** | Procesamiento de CSV | Estándar para manipulación de datos tabulares | 2.3.3 |
| **HuggingFace** | Hub de modelos | Acceso a modelos pre-entrenados | - |

### **Conceptos Clave Explicados**

#### **🧠 LLM (Large Language Model)**
Modelo de lenguaje grande como GPT o Llama. En nuestro caso, usamos **llama-3.3-70b** a través de Groq.
- **Función:** Entender y generar texto
- **Uso en el proyecto:** Clasificar consultas y generar respuestas

#### **🔍 RAG (Retrieval-Augmented Generation)**
Técnica que combina búsqueda de información + generación de texto.
```
RAG = Recuperar documentos relevantes + Generar respuesta basada en ellos
```
**Ventaja:** El LLM responde con información actualizada y específica, no solo con su conocimiento general.

#### **📊 Embeddings**
Representación numérica del significado de un texto.
```
"abrir cuenta" → [0.23, -0.45, 0.67, 0.12, ...]
"crear cuenta" → [0.25, -0.43, 0.65, 0.14, ...]  # Similar!
```
**Ventaja:** Podemos calcular similitud matemática entre textos.

#### **⚡ FAISS (Facebook AI Similarity Search)**
Base de datos especializada en buscar vectores similares muy rápido.
- Desarrollada por Meta (Facebook)
- Puede buscar en millones de vectores en milisegundos
- En nuestro proyecto: busca los 2 documentos más relevantes (k=2)

## 🔑 Características Clave

### **1. Router Inteligente**
- Clasificación automática usando LLM
- Few-shot prompting para mejor precisión
- Fallback a categoría "general"

### **2. Sistema RAG Completo**
- Embeddings con modelo local (no requiere API)
- Búsqueda semántica ultra-rápida con FAISS
- Generación contextual con LLM

### **3. Búsqueda en CSV**
- Extracción automática de cédula con regex
- Manejo de errores (cédula no encontrada)
- Formato de respuesta profesional

### **4. Interfaz CLI Amigable**
- Loop interactivo
- Ejemplos de uso
- Manejo de errores graceful
- Comando "salir" para terminar

## 📊 Flujo de Procesamiento

```
1. Usuario ingresa consulta
   ↓
2. clasificar_consulta(consulta)
   ├─ Envía consulta al LLM
   ├─ LLM analiza y clasifica
   └─ Retorna: "balance" | "knowledge" | "general"
   ↓
3. procesar_consulta() ejecuta herramienta apropiada
   ├─ balance → consultar_balance(cedula)
   │   ├─ Extrae cédula con regex
   │   ├─ Busca en CSV con Pandas
   │   └─ Retorna datos formateados
   │
   ├─ knowledge → consultar_knowledge_base(pregunta)
   │   ├─ Retriever busca en FAISS (k=2)
   │   ├─ Construye contexto con docs relevantes
   │   ├─ Genera prompt RAG
   │   └─ LLM genera respuesta contextual
   │
   └─ general → respuesta_general(pregunta)
       ├─ Construye prompt simple
       └─ LLM genera respuesta directa
   ↓
4. Retorna respuesta al usuario
```

## 🎯 Decisiones de Diseño

### **¿Por qué Groq?**
- API gratuita
- Latencia ultra-baja (~0.5s)
- Modelos potentes (llama-3.3-70b)
- Más rápido que OpenAI para este caso de uso

### **¿Por qué FAISS?**
- Búsqueda vectorial extremadamente rápida
- Funciona localmente (sin APIs)
- Escalable a millones de documentos
- Usado por Meta en producción

### **¿Por qué sentence-transformers?**
- Modelo gratuito y local
- Optimizado para búsqueda semántica
- Pequeño (90MB) pero efectivo
- No requiere GPU

### **¿Por qué LangChain?**
- Abstracciones poderosas para LLM apps
- Integración fácil con múltiples LLMs
- Ecosistema maduro y bien documentado
- Soporte nativo para RAG

## 🐛 Troubleshooting

### **Error: ModuleNotFoundError**
```bash
# Asegúrate de tener el venv activado
.\venv\Scripts\Activate.ps1

# Reinstala dependencias
pip install -r requirements.txt
```

### **Error: GROQ_API_KEY no configurada**
```bash
# Verifica que .env existe y tiene la key
cat .env

# Debe contener:
GROQ_API_KEY=gsk_...
```

### **Error: No se encuentra index/**
```bash
# Ejecuta el indexer primero
python indexer.py
```

### **Respuestas lentas**
- Groq es muy rápido (~0.5s)
- Si es lento, verifica tu conexión a internet
- El modelo de embeddings carga la primera vez (tarda ~10s)

## 📈 Mejoras Futuras

1. **Interfaz Web con Streamlit**
   - UI más amigable
   - Visualización de documentos encontrados
   - Historial de conversación

2. **Más Herramientas**
   - Consulta de transacciones
   - Generación de reportes
   - Programación de citas

3. **Memoria de Conversación**
   - LangChain ConversationBufferMemory
   - Contexto entre preguntas

4. **Mejores Prompts**
   - Ajustar temperatura según caso
   - Few-shot learning para cada herramienta
   - Validación de respuestas

5. **Base de Datos Real**
   - Reemplazar CSV con PostgreSQL
   - Caché de consultas frecuentes

## 👨‍💻 Autor

Proyecto desarrollado como parte del curso de IA y LangChain.

## 📄 Licencia

MIT License - Uso libre para fines educativos.

---

**¿Preguntas o problemas?** Abre un issue o contacta al instructor.
