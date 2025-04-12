import threading
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from models.llm import LLMModel
from database.vector_db import VectorDatabase

class FirstAidService:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    @classmethod
    def get_instance(cls, config):
        """Singleton pattern with thread-safe initialization"""
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    cls._instance = cls._initialize_service(config)
                    cls._initialized = True
        return cls._instance
    
    @staticmethod
    def _initialize_service(config):
        """Initialize the QA service"""
        print("Initializing First Aid Service...")
        
        # Get LLM instance
        llm = LLMModel.get_instance(config)
        
        # Get Vector DB instance
        vector_db = VectorDatabase.get_instance(config)
        
        # Create QA chain
        qa_chain = FirstAidService._create_qa_chain(llm, vector_db)
        
        print("First Aid Service initialized successfully")
        return qa_chain
    
    @staticmethod
    def _create_qa_chain(llm, vector_db):
        """Create a QA chain for the first aid service"""
        # Create retriever
        retriever = vector_db.as_retriever()
        
        # Create prompt template
        prompt_template = """You are a knowledgeable and reliable First Aid Assistant.
        Your ONLY purpose is to provide clear and concise first aid recommendations based on the given information.
        
        IMPORTANT: You must ONLY respond to medical and first aid related questions. 
        If the query is not related to medical advice, first aid, health emergencies, or similar topics,
        you must politely decline to answer and remind the user about your specific purpose.
        
        Relevant First Aid Info:
        {context}
        
        User: {question}
        Assistant: """
        
        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=['context', 'question']
        )
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    
    @classmethod
    def get_recommendation(cls, query, config):
        """Get first aid recommendation for a query"""
        service = cls.get_instance(config)
        return service.run(query)