# services/automation/engine.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from services.agents.orchestrator import AgentOrchestrator
from services.memory.live_memory import LiveMemory
from services.ia.patterns import PatternDetector

class AutomationEngine:
    """Motor de automações do Darwin"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pattern_detector = PatternDetector(user_id)
        self.memory = LiveMemory(user_id)
        self.orchestrator = AgentOrchestrator(user_id)
        self.automations = {}
        self.is_running = False
    
    async def create_automation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova automação"""
        automation_id = str(uuid.uuid4())
        
        self.automations[automation_id] = {
            "id": automation_id,
            "name": config.get("name", "Untitled Automation"),
            "trigger": config.get("trigger", {}),
            "actions": config.get("actions", []),
            "conditions": config.get("conditions", []),
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "last_triggered": None,
            "execution_count": 0
        }
        
        return self.automations[automation_id]
    
    async def start(self) -> None:
        """Inicia o motor de automações"""
        self.is_running = True
        asyncio.create_task(self._run_loop())
    
    async def stop(self) -> None:
        """Para o motor de automações"""
        self.is_running = False
    
    async def _run_loop(self) -> None:
        """Loop principal de execução"""
        while self.is_running:
            try:
                # Verifica padrões
                patterns = await self.pattern_detector.detect_patterns()
                
                # Executa automações
                for automation_id, automation in self.automations.items():
                    if automation["status"] == "active":
                        if await self._should_trigger(automation, patterns):
                            await self._execute_automation(automation)
                
                # Espera
                await asyncio.sleep(60)  # Verifica a cada minuto
                
            except Exception as e:
                print(f"Error in automation loop: {e}")
                await asyncio.sleep(60)
    
    async def _should_trigger(self, automation: Dict[str, Any], patterns: List[Dict[str, Any]]) -> bool:
        """Verifica se a automação deve ser acionada"""
        trigger = automation.get("trigger", {})
        
        if trigger.get("type") == "pattern":
            pattern_type = trigger.get("pattern_type")
            for pattern in patterns:
                if pattern.get("type") == pattern_type:
                    return True
        
        elif trigger.get("type") == "schedule":
            # Verifica agendamento
            schedule = trigger.get("schedule", {})
            now = datetime.now()
            
            if schedule.get("time") == now.strftime("%H:%M"):
                return True
        
        elif trigger.get("type") == "threshold":
            # Verifica limite
            metric = trigger.get("metric")
            threshold = trigger.get("threshold")
            # TODO: Implementar verificação de métricas
            
        return False
    
    async def _execute_automation(self, automation: Dict[str, Any]) -> None:
        """Executa uma automação"""
        actions = automation.get("actions", [])
        
        for action in actions:
            if action.get("type") == "agent":
                # Executa agente
                result = await self.orchestrator.execute_agent(
                    action["agent_name"],
                    action.get("input", {})
                )
                
                # Registra resultado
                await self.memory.store({
                    "type": "automation_execution",
                    "data": {
                        "automation_id": automation["id"],
                        "action": action,
                        "result": result,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
            
            elif action.get("type") == "task":
                # Cria tarefa
                await self.memory.store({
                    "type": "task",
                    "data": {
                        "title": action.get("title"),
                        "description": action.get("description"),
                        "priority": action.get("priority", 3),
                        "context": action.get("context", {})
                    }
                })
            
            elif action.get("type") == "notification":
                # Envia notificação
                # TODO: Implementar envio de notificação
                pass
        
        # Atualiza automação
        automation["last_triggered"] = datetime.utcnow().isoformat()
        automation["execution_count"] += 1
