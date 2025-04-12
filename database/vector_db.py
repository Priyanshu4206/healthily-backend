import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from datasets import load_dataset

class VectorDatabase:
    _instance = None
    
    @classmethod
    def get_instance(cls, config):
        """Singleton pattern to ensure database is only created once"""
        print("\n[INFO] Checking for existing vector database instance...")
        if cls._instance is None:
            print("[INFO] No existing instance found. Creating or loading database.")
            cls._instance = cls._create_or_load_db(config)
        else:
            print("[INFO] Using existing database instance.")
        return cls._instance
    
    @staticmethod
    def _create_or_load_db(config):
        """Create a new vector database or load an existing one"""
        db_path = config['db_path']
        index_path = os.path.join(db_path, "faiss_index")
        store_path = os.path.join(db_path, "faiss_store.pkl")
        
        print(f"\n[INFO] Database Path: {db_path}")
        
        # Create embeddings
        print("[INFO] Initializing HuggingFace embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Check if database exists
        if os.path.exists(index_path) and os.path.exists(store_path):
            print(f"[INFO] Found existing FAISS database at {db_path}")
            
            # Load the index
            print("[INFO] Loading FAISS index from storage...")
            vector_store = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("[SUCCESS] FAISS index loaded successfully!")

            # Load additional metadata from pickle
            with open(store_path, "rb") as f:
                stored_data = pickle.load(f)
                print(f"[SUCCESS] FAISS metadata loaded: {stored_data.keys()}")

            print("[SUCCESS] FAISS index loaded successfully!")

        else:
            print("[INFO] No existing FAISS database found. Creating a new one...")
            os.makedirs(db_path, exist_ok=True)
            
            # Load dataset
            print("[INFO] Loading dataset for vectorization...")
            documents = VectorDatabase._load_dataset()

            
            # Split documents
            print(f"[INFO] Splitting {len(documents)} documents into smaller chunks...")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            split_documents = text_splitter.split_documents(documents)
            print(f"[SUCCESS] Split into {len(split_documents)} chunks.")

            # Create vector database with progress tracking
            print("[INFO] Creating FAISS vector database...")
            total_docs = len(split_documents)
            batch_size = 100  # Adjust based on your needs
            vector_store = None

            for i in range(0, total_docs, batch_size):
                end_idx = min(i + batch_size, total_docs)
                current_batch = split_documents[i:end_idx]
                
                print(f"[INFO] Processing batch {i//batch_size + 1}/{(total_docs+batch_size-1)//batch_size}: "
                    f"documents {i} to {end_idx-1} of {total_docs} ({(end_idx/total_docs)*100:.1f}%)")
                
                # For the first batch, create the vector store
                if vector_store is None:
                    vector_store = FAISS.from_documents(current_batch, embeddings)
                # For subsequent batches, add to the existing store
                else:
                    vector_store.add_documents(current_batch)

            # Save the FAISS index
            print("[INFO] Saving FAISS index to disk...")
            vector_store.save_local(index_path)

            # Save metadata using pickle
            with open(store_path, "wb") as f:
                pickle.dump({"doc_count": len(split_documents)}, f)

            print("[SUCCESS] Vector database created and stored successfully!")

        return vector_store
    
    @staticmethod
    def _load_dataset(limit=None):
        """Load and process the dataset"""
        print("\n[INFO] Loading FirstAidInstructionsDataset from Hugging Face...")
        dataset = load_dataset("lextale/FirstAidInstructionsDataset")
        documents = []
        
        if 'Superdataset' not in dataset:
            print("[ERROR] Dataset structure unexpected! Check dataset keys:", dataset.keys())
            return []

        print("[INFO] Processing dataset into Document objects...")
        for i, example in enumerate(dataset['Superdataset']):  # Use enumerate to get the index
            if limit and i >= limit:
                break  # Stop processing once limit is reached

            user_input = example["question"]
            response = example["answer"]

            if not user_input or not response:
                print(f"[WARNING] Skipping incomplete entry at index {i}")
                continue
            
            text = f"User: {user_input}\nTherapist: {response}"
            doc = Document(page_content=text, metadata={"source": "dataset"})
            documents.append(doc)

            if i % 100 == 0:  # Print progress every 100 documents
                print(f"[INFO] Processed {i+1} documents...")

        print(f"[SUCCESS] Loaded {len(documents)} valid documents from dataset.")
        return documents