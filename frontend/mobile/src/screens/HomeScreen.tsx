// frontend/mobile/src/screens/HomeScreen.tsx
import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity,
  RefreshControl 
} from 'react-native';
import { useDarwin } from '../hooks/useDarwin';
import { EnergyIndicator } from '../components/EnergyIndicator';
import { TaskCard } from '../components/TaskCard';
import { QuickActions } from '../components/QuickActions';
import { VoiceInput } from '../components/VoiceInput';

export const HomeScreen: React.FC = () => {
  const [refreshing, setRefreshing] = useState(false);
  const { 
    tasks, 
    energy, 
    metrics, 
    patterns,
    loadData 
  } = useDarwin();

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Darwin</Text>
        <EnergyIndicator value={energy.current} max={10} />
      </View>

      {/* Métricas rápidas */}
      <View style={styles.metricsRow}>
        <MetricCard label="XP" value={metrics.xp.total} />
        <MetricCard label="Tarefas" value={tasks.today.total} />
        <MetricCard label="Sequência" value={metrics.sequence.level} />
      </View>

      {/* Entrada de voz */}
      <VoiceInput onResult={handleVoiceResult} />

      {/* Tarefas do dia */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Tarefas Hoje</Text>
        {tasks.today.list.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </View>

      {/* Padrões detectados */}
      {patterns.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Padrões Detectados</Text>
          {patterns.map((pattern, index) => (
            <PatternCard key={index} pattern={pattern} />
          ))}
        </View>
      )}

      {/* Ações rápidas */}
      <QuickActions />

      {/* Botões de navegação */}
      <View style={styles.navButtons}>
        <TouchableOpacity style={styles.navButton} onPress={() => navigateTo('Dashboard')}>
          <Text>Dashboard</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigateTo('Agents')}>
          <Text>Agentes</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigateTo('Evolution')}>
          <Text>Evolução</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a2e',
  },
  metricsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 12,
  },
  section: {
    marginVertical: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#333',
  },
  navButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 20,
    borderTopWidth: 1,
    borderTopColor: '#ddd',
    marginTop: 20,
  },
  navButton: {
    padding: 12,
    backgroundColor: '#fff',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
});
