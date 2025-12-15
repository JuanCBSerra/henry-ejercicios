"""
Indexer - Generador de Base de Conocimientos Vectorial

Este script procesa los documentos de la carpeta knowledge_base/
y crea un índice FAISS para búsqueda semántica eficiente.

Flujo:
1. Lee todos los archivos .txt de knowledge_base/
2. Genera embeddings usando sentence-transformers
3. Crea un índice FAISS
4. Guarda el índice localmente para uso posterior
"""

import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

def load_documents_from_knowledge_base(kb_path="knowledge_base"):
    """
    Carga todos los documentos de texto de la carpeta knowledge_base/
    
    Args:
        kb_path: Ruta a la carpeta con los documentos
    
    Returns:
        Lista de objetos Document de LangChain
    """
    documents = []
    kb_folder = Path(kb_path)
    
    print(f"📁 Leyendo documentos de: {kb_folder.absolute()}")
    
    # Buscar todos los archivos .txt
    for file_path in kb_folder.glob("*.txt"):
        print(f"   📄 Procesando: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Crear un Document de LangChain con metadata
            doc = Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "path": str(file_path)
                }
            )
            documents.append(doc)
    
    print(f"✅ Total de documentos cargados: {len(documents)}\n")
    return documents

def create_vector_store(documents, index_path="index"):
    """
    Crea el índice vectorial FAISS a partir de los documentos
    
    Args:
        documents: Lista de documentos a indexar
        index_path: Carpeta donde se guardará el índice
    
    Returns:
        Vector store FAISS
    """
    print("🔄 Generando embeddings...")
    
    # Configurar el modelo de embeddings
    # Este modelo es gratuito y corre localmente (no necesita API)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # Usar CPU (cambiar a 'cuda' si tienes GPU)
    )
    
    # Dividir documentos en chunks más pequeños si son muy largos
    # Esto mejora la precisión de las búsquedas
    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separator="\n"
    )
    
    split_docs = text_splitter.split_documents(documents)
    print(f"   📝 Documentos divididos en {len(split_docs)} chunks")
    
    # Crear el vector store con FAISS
    print("   🧮 Creando índice FAISS...")
    vector_store = FAISS.from_documents(split_docs, embeddings)
    
    # Guardar el índice localmente
    print(f"💾 Guardando índice en: {index_path}/")
    os.makedirs(index_path, exist_ok=True)
    vector_store.save_local(index_path)
    
    print("✅ Índice creado y guardado exitosamente!\n")
    return vector_store

def test_vector_store(vector_store):
    """
    Prueba el vector store con una consulta de ejemplo
    
    Args:
        vector_store: El vector store FAISS a probar
    """
    print("🧪 Probando el índice con una consulta de ejemplo...")
    
    test_query = "¿Cómo abro una cuenta?"
    print(f"   Consulta: '{test_query}'")
    
    # Buscar los 2 documentos más similares
    results = vector_store.similarity_search(test_query, k=2)
    
    print(f"   📊 Se encontraron {len(results)} resultados relevantes:")
    for i, doc in enumerate(results, 1):
        print(f"\n   Resultado {i}:")
        print(f"   Fuente: {doc.metadata.get('source', 'N/A')}")
        print(f"   Contenido (primeros 100 chars): {doc.page_content[:100]}...")

def main():
    """
    Función principal que ejecuta todo el proceso de indexación
    """
    print("=" * 60)
    print("🚀 INDEXER - Generador de Base de Conocimientos Vectorial")
    print("=" * 60)
    print()
    
    # Paso 1: Cargar documentos
    documents = load_documents_from_knowledge_base()
    
    if not documents:
        print("❌ Error: No se encontraron documentos en knowledge_base/")
        return
    
    # Paso 2: Crear y guardar el índice vectorial
    vector_store = create_vector_store(documents)
    
    # Paso 3: Probar que funciona
    test_vector_store(vector_store)
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado exitosamente!")
    print("=" * 60)
    print("\n💡 El índice está listo para ser usado en main.py")

if __name__ == "__main__":
    main()
