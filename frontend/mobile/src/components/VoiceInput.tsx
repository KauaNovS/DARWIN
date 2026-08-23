// frontend/mobile/src/components/VoiceInput.tsx
import React, { useState } from 'react';
import { 
  View, 
  TouchableOpacity, 
  Text, 
  StyleSheet,
  ActivityIndicator 
} from 'react-native';
import Voice from '@react-native-voice/voice';
import { useDarwin } from '../hooks/useDarwin';

export const VoiceInput: React.FC<{ onResult?: (text: string) => void }> = ({ onResult }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const { processVoiceCommand } = useDarwin();

  const startRecording = async () => {
    try {
      setIsRecording(true);
      await Voice.start('pt-BR');
    } catch (error) {
      console.error('Error starting voice recording:', error);
      setIsRecording(false);
    }
  };

  const stopRecording = async () => {
    try {
      setIsRecording(false);
      await Voice.stop();
    } catch (error) {
      console.error('Error stopping voice recording:', error);
    }
  };

  const handleVoiceResults = async (event: any) => {
    const text = event.value?.[0];
    if (text) {
      setTranscript(text);
      setIsProcessing(true);
      
      try {
        // Processa comando no backend
        const result = await processVoiceCommand(text);
        if (onResult) onResult(text);
        setTranscript('');
      } catch (error) {
        console.error('Error processing voice command:', error);
      } finally {
        setIsProcessing(false);
      }
    }
  };

  useEffect(() => {
    Voice.onSpeechResults = handleVoiceResults;
    Voice.onSpeechError = (error) => {
      console.error('Voice error:', error);
      setIsRecording(false);
    };

    return () => {
      Voice.destroy().then(Voice.removeAllListeners);
    };
  }, []);

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.button, isRecording && styles.recording]}
        onPressIn={startRecording}
        onPressOut={stopRecording}
        disabled={isProcessing}
      >
        {isProcessing ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>
            {isRecording ? '🎤 Gravando...' : '🎤 Pressione e fale'}
          </Text>
        )}
      </TouchableOpacity>
      
      {transcript && (
        <Text style={styles.transcript}>"{transcript}"</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 12,
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
  },
  recording: {
    backgroundColor: '#FF5722',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  transcript: {
    marginTop: 8,
    color: '#555',
    fontStyle: 'italic',
  },
});
