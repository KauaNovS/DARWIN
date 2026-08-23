# api/routes/voice.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from services.voice.processor import VoiceProcessor
from services.ia.context import ContextualAI
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/voice/process")
async def process_voice(
    audio: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Processa um comando de voz"""
    processor = VoiceProcessor()
    ai = ContextualAI(current_user.id)
    
    # Transcreve áudio
    text = await processor.transcribe(audio)
    
    # Compreende contexto
    context = await ai.understand_context(text)
    
    # Executa ação correspondente
    action = await processor.execute_command(text, context, current_user.id)
    
    return {
        "transcription": text,
        "context": context,
        "action": action
    }

@router.post("/voice/register")
async def register_voice_command(
    command: dict,
    current_user = Depends(get_current_user)
):
    """Registra um comando de voz manualmente"""
    from services.voice.command_handler import VoiceCommandHandler
    
    handler = VoiceCommandHandler(current_user.id)
    result = await handler.process_command(command["text"], command.get("context", {}))
    
    return result
