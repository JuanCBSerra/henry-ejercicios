# 🚀 INICIO RÁPIDO - 5 Minutos

¿Primera vez usando el sistema? Sigue estos pasos exactos:

## ✅ Checklist Rápido

- [ ] Python 3.10+ instalado
- [ ] Cuenta en Groq (gratis)
- [ ] 5 minutos de tiempo

---

## 📝 Paso 1: Preparar el Entorno (1 min)

```powershell
# Ir al directorio del proyecto
cd "HW - LangChain II"

# Crear entorno virtual
python -m venv venv

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activar (Windows CMD)
.\venv\Scripts\activate.bat

# Activar (Linux/Mac)
source venv/bin/activate
```

**✅ Verificar:** Deberías ver `(venv)` al inicio de tu terminal

---

## 📦 Paso 2: Instalar Dependencias (2 min)

```powershell
pip install -r requirements.txt
```

**⏳ Esto tarda ~2 minutos.** Instalará:
- LangChain
- FAISS
- Sentence Transformers
- Pandas
- Groq SDK
- Otras dependencias

**✅ Verificar:** Al terminar, no debe haber errores

---

## 🔑 Paso 3: Configurar API Key (1 min)

### **Opción A: Ya tienes API key de Groq**
```powershell
# Copiar plantilla
copy .env.example .env

# Editar .env (puedes usar notepad)
notepad .env
```

Pega tu API key:
```
GROQ_API_KEY=gsk_tu_clave_aqui
```

### **Opción B: No tienes API key**
1. Ve a: https://console.groq.com/
2. Crea cuenta (gratis)
3. Ve a "API Keys"
4. Crea nueva key
5. Cópiala y pégala en `.env`

**✅ Verificar:** El archivo `.env` existe y tiene tu key

---

## 🏗️ Paso 4: Generar Índice Vectorial (1 min)

```powershell
python indexer.py
```

**Lo que verás:**
```
🚀 INDEXER - Generador de Base de Conocimientos Vectorial
📁 Leyendo documentos...
   📄 Procesando: nueva_cuenta.txt
   📄 Procesando: tarjeta_credito.txt
   📄 Procesando: transferencia.txt
✅ Total de documentos cargados: 3
🔄 Generando embeddings...
💾 Guardando índice en: index/
✅ Índice creado exitosamente!
```

**✅ Verificar:** Se creó la carpeta `index/`

---

## 🎉 Paso 5: ¡Ejecutar el Sistema!

```powershell
python main.py
```

**Lo que verás:**
```
======================================================================
🏦 SISTEMA DE ATENCIÓN AL CLIENTE - BANCO HENRY
======================================================================

🔧 Inicializando componentes...
   ✅ LLM inicializado (Groq - llama-3.3-70b-versatile)
   ✅ CSV cargado: 10 registros
   ✅ Base de conocimientos vectorial cargada

======================================================================
💬 Chat iniciado - Escribe 'salir' o 'exit' para terminar
======================================================================

👤 Usuario: _
```

---

## 🧪 Probar el Sistema

### **Prueba 1: Consulta de Balance**
```
👤 Usuario: ¿Cuál es el balance de la cédula V-91827364?
```

**Respuesta esperada:**
```
✅ Información de cuenta encontrada:
👤 Titular: Luis Méndez
🆔 Cédula: V-91827364
💰 Balance: $2,580.00
```

### **Prueba 2: Información Bancaria**
```
👤 Usuario: ¿Cómo abro una cuenta de ahorros?
```

**Respuesta esperada:**
```
Para abrir una cuenta en BANCO HENRY, sigue estos pasos:
1. Visita la página web...
[continúa con información detallada]
```

### **Prueba 3: Pregunta Fuera de Contexto**
```
👤 Usuario: ¿Cuál es el sentido de la vida?
```

**Respuesta esperada:**
```
⚠️ Lo siento, solo puedo ayudarte con consultas relacionadas con servicios bancarios del BANCO HENRY.

Puedo asistirte con:
• Consultas de balance de cuentas
• Información sobre cómo abrir cuentas
• Solicitud de tarjetas de crédito
...
```

---

## 🎯 Comandos Útiles

```powershell
# Ejecutar sistema
python main.py

# Ejecutar pruebas automatizadas
python test_system.py

# Re-generar índice (si cambias knowledge_base/)
python indexer.py

# Salir del venv
deactivate
```

---

## ❌ Solución de Problemas Comunes

### **Error: "GROQ_API_KEY no está configurada"**
```
❌ Problema: Falta API key
✅ Solución: Asegúrate que el archivo .env existe y tiene:
   GROQ_API_KEY=tu_clave_aqui
```

### **Error: "ModuleNotFoundError: No module named 'pandas'"**
```
❌ Problema: Dependencias no instaladas
✅ Solución: 
   1. Activa el venv: .\venv\Scripts\Activate.ps1
   2. Instala: pip install -r requirements.txt
```

### **Error: "No se encuentra index/"**
```
❌ Problema: Índice no generado
✅ Solución: Ejecuta python indexer.py
```

### **Respuestas lentas**
```
❌ Problema: Primera ejecución carga modelos
✅ Solución: Es normal. La primera vez tarda ~10s
   Las siguientes serán rápidas (~0.5s)
```

---

## 📊 Estructura de Archivos (Referencia)

```
HW - LangChain II/
├── 📄 main.py              ← Ejecutar esto
├── 📄 indexer.py           ← Ejecutar primero (solo una vez)
├── 📄 test_system.py       ← Pruebas automatizadas
├── 📄 requirements.txt     ← Dependencias
├── 📄 .env                 ← Tu API key (crear)
├── 📂 data/
│   └── saldos.csv          ← Datos de cuentas
├── 📂 knowledge_base/
│   ├── nueva_cuenta.txt    ← Info bancaria
│   ├── tarjeta_credito.txt
│   └── transferencia.txt
├── 📂 index/               ← Se genera automáticamente
│   ├── index.faiss
│   └── index.pkl
└── 📂 venv/                ← Entorno virtual
```

---

## 🎓 Siguiente Paso

Una vez que el sistema funcione:

1. **Lee la documentación completa:** `README_PROYECTO.md`
2. **Entiende cómo funciona:** `GUIA_TECNICA.md`
3. **Experimenta:** Agrega más documentos a `knowledge_base/`
4. **Mejora:** Ajusta los prompts en `main.py`

---

## 💬 ¿Necesitas Ayuda?

- **Documentación completa:** `README_PROYECTO.md`
- **Guía técnica:** `GUIA_TECNICA.md`
- **Pruebas:** `python test_system.py`

---

**🎉 ¡Listo! En 5 minutos deberías tener el sistema funcionando.**
