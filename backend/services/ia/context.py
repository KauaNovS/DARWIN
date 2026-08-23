# services/ia/context.py
from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from core.config import settings
from services.memory.live_memory import LiveMemory
from services.graph.query import GraphQuery

logger = logging.getLogger(__name__)

class ContextualAI:
    """IA contextual do Darwin - versão inicial"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.memory = LiveMemory(user_id)
        self.graph = GraphQuery(user_id)
    
    async def understand_context(self, input_text: str) -> Dict[str, Any]:
        """Compreende o contexto de uma entrada do usuário"""
        # Recupera contexto relevante
        context = await self.memory.get_relevant_context(input_text)
        patterns = await self.graph.get_patterns()
        
        prompt = self._build_context_prompt(input_text, context, patterns)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def generate_recommendation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gera recomendações baseadas no estado atual"""
        # TODO: Implementar recomendação contextual
        pass
    
    def _system_prompt(self) -> str:
        return """
        Você é Darwin, um sistema operacional de evolução humana.
        Sua função é compreender o contexto do usuário, identificar padrões,
        e ajudar na evolução pessoal.
        
        Você deve interpretar:
        - Intenção do usuário
        - Estado emocional
        - Padrões comportamentais
        - Oportunidades de evolução
        
        Responda sempre em formato JSON com os campos:
        - intent: string
        - emotion: string
        - context: object
        - suggested_actions: array
        - recommended_tasks: array
        """
    
    def _build_context_prompt(self, input_text: str, context: Dict, patterns: Dict) -> str:
        return f"""
        Entrada do usuário: {input_text}
        
        Contexto relevante:
        {json.dumps(context, indent=2)}
        
        Padrões identificados:
        {json.dumps(patterns, indent=2)}
        
        Interprete esta entrada no contexto do usuário.
        """
