# services/voice/processor.py
#
# NOTE: Referenced by api/routes/voice.py but never implemented in the
# original plan document. Minimal stub — plug in a real speech-to-text
# provider (Whisper API, etc) inside process().
from typing import Any, Dict
from fastapi import UploadFile


class VoiceProcessor:
    """Processa áudio de voz (stub — implementar transcrição real)"""

    async def process(self, audio: UploadFile) -> Dict[str, Any]:
        # TODO: Implementar transcrição real (ex: Whisper API)
        return {
            "status": "not_implemented",
            "filename": audio.filename,
            "transcript": None,
        }
