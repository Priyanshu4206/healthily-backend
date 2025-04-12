from langchain_groq import ChatGroq

class LLMModel:
    _instance = None
    
    @classmethod
    def get_instance(cls, config):
        """Singleton pattern to ensure model is only created once"""
        if cls._instance is None:
            cls._instance = cls._create_model(config)
        return cls._instance
    
    @staticmethod
    def _create_model(config):
        """Create and return the LLM model"""
        print(f"Initializing LLM model: {config['model_name']}")
        return ChatGroq(
            temperature=config['temperature'],
            groq_api_key=config['groq_api_key'],
            model_name=config['model_name']
        )