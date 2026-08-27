import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions } from 'react-native'
import { router } from 'expo-router'

const PATHS = [
  { key: 'FOOL',      name: 'O Louco',      icon: '🌀', color: '#60A5FA' },
  { key: 'OBSERVER',  name: 'O Observador',  icon: '👁', color: '#A78BFA' },
  { key: 'ALCHEMIST', name: 'O Alquimista',  icon: '⚗',  color: '#34D399' },
  { key: 'GUARDIAN',  name: 'O Guardiao',    icon: '🛡', color: '#F87171' },
  { key: 'ARCHITECT', name: 'O Arquiteto',   icon: '🏛', color: '#FBBF24' },
]

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>DARWIN</Text>
          <Text style={styles.subtitle}>Sistema de Evolucao Humana</Text>
          <Text style={styles.quote}>
            "O misterio nao existe para ser resolvido.{'
'}Existe para ser habitado."
          </Text>
          <View style={styles.divider} />
        </View>

        {/* Caminhos */}
        <Text style={styles.sectionLabel}>Escolha seu Caminho</Text>
        <View style={styles.grid}>
          {PATHS.map((p) => (
            <TouchableOpacity key={p.key} style={styles.card}
              onPress={() => router.push(`/path/${p.key.toLowerCase()}`)}>
              <Text style={styles.cardIcon}>{p.icon}</Text>
              <Text style={[styles.cardName, { color: p.color }]}>{p.name}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Acoes */}
        <TouchableOpacity style={styles.primaryBtn}
          onPress={() => router.push('/auth/login')}>
          <Text style={styles.primaryBtnText}>Iniciar Jornada</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.secondaryBtn}
          onPress={() => router.push('/dashboard')}>
          <Text style={styles.secondaryBtnText}>Ja sou Beyonder</Text>
        </TouchableOpacity>

      </ScrollView>
    </View>
  )
}

const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: '#080822' },
  scroll:       { padding: 24, paddingBottom: 48 },
  header:       { alignItems: 'center', marginBottom: 40, marginTop: 40 },
  title:        { fontSize: 48, color: '#D8D8E8', letterSpacing: 12, fontWeight: '300' },
  subtitle:     { fontSize: 11, color: '#606088', letterSpacing: 4, marginTop: 8, textTransform: 'uppercase' },
  quote:        { fontSize: 12, color: '#383866', fontStyle: 'italic', textAlign: 'center', marginTop: 16, lineHeight: 20 },
  divider:      { width: 60, height: 1, backgroundColor: '#E8A820', opacity: 0.5, marginTop: 20 },
  sectionLabel: { fontSize: 11, color: '#606088', letterSpacing: 3, textTransform: 'uppercase', marginBottom: 16 },
  grid:         { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 32 },
  card: {
    width: (Dimensions.get('window').width - 60) / 2,
    backgroundColor: '#111133',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#282855',
    padding: 20,
    alignItems: 'center',
    gap: 10,
  },
  cardIcon:     { fontSize: 32 },
  cardName:     { fontSize: 14, fontWeight: '500', textAlign: 'center' },
  primaryBtn: {
    backgroundColor: '#F9C44A',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 12,
  },
  primaryBtnText: { color: '#080822', fontSize: 15, fontWeight: '600' },
  secondaryBtn: {
    borderWidth: 1,
    borderColor: '#282855',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
  },
  secondaryBtnText: { color: '#606088', fontSize: 14 },
})
