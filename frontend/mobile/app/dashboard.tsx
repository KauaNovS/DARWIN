import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native'
import { useEffect, useState } from 'react'
import { router } from 'expo-router'

const API = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchAPI(path: string) {
  const res = await fetch(`${API}${path}`, {
    headers: { Authorization: `Bearer ${global.darwin_token || ''}` }
  })
  return res.json()
}

export default function DashboardScreen() {
  const [seq, setSeq] = useState<any>(null)
  const [potion, setPotion] = useState<any>(null)

  useEffect(() => {
    Promise.all([
      fetchAPI('/api/sequences/my-sequence'),
      fetchAPI('/api/potions/current'),
    ]).then(([s, p]) => { setSeq(s); setPotion(p) })
  }, [])

  const digPct = potion?.progress_pct ?? 0

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>

        <Text style={styles.heading}>Sua Jornada</Text>
        {seq && (
          <Text style={styles.subheading}>
            {seq.path_name} -- Nivel {seq.level}: {seq.title}
          </Text>
        )}

        {/* XP */}
        <View style={styles.xpBadge}>
          <Text style={styles.xpLabel}>Total XP</Text>
          <Text style={styles.xpValue}>{seq?.total_xp?.toFixed(0) ?? 0}</Text>
        </View>

        {/* Pocao */}
        {potion && (
          <View style={styles.card}>
            <Text style={styles.cardLabel}>Pocao Atual</Text>
            <Text style={styles.cardTitle}>{potion.potion_name}</Text>
            <View style={styles.progressBg}>
              <View style={[styles.progressFill, { width: `${Math.min(digPct, 100)}%` }]} />
            </View>
            <Text style={styles.progressText}>
              Digestao: {potion.digestion_score?.toFixed(1)}% / {potion.digestion_threshold}%
            </Text>
            <View style={styles.tags}>
              {(potion.ingredients ?? []).slice(0, 4).map((i: string) => (
                <Text key={i} style={styles.tag}>{i.replace(/_/g,' ')}</Text>
              ))}
            </View>
          </View>
        )}

        {/* Acoes rapidas */}
        <View style={styles.actions}>
          {[
            { label: 'Ritual Diario', icon: '🌙', route: '/ritual' },
            { label: 'O Oraculo', icon: '🔮', route: '/oracle' },
            { label: 'Sequencia', icon: '📜', route: '/sequence' },
            { label: 'Arquivo', icon: '📁', route: '/memory' },
          ].map(a => (
            <TouchableOpacity key={a.route} style={styles.actionBtn}
              onPress={() => router.push(a.route as any)}>
              <Text style={{ fontSize: 24 }}>{a.icon}</Text>
              <Text style={styles.actionLabel}>{a.label}</Text>
            </TouchableOpacity>
          ))}
        </View>

      </ScrollView>
    </View>
  )
}

const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: '#080822' },
  scroll:       { padding: 24, paddingBottom: 48, paddingTop: 56 },
  heading:      { fontSize: 26, color: '#D8D8E8', fontWeight: '300' },
  subheading:   { fontSize: 13, color: '#606088', marginTop: 4, marginBottom: 20 },
  xpBadge:     { alignSelf: 'flex-end', alignItems: 'flex-end', marginBottom: 16 },
  xpLabel:     { fontSize: 10, color: '#606088', textTransform: 'uppercase', letterSpacing: 2 },
  xpValue:     { fontSize: 28, color: '#F9C44A', fontVariant: ['tabular-nums'] },
  card: {
    backgroundColor: '#111133',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#282855',
    padding: 20,
    marginBottom: 20,
    gap: 10,
  },
  cardLabel:   { fontSize: 10, color: '#606088', textTransform: 'uppercase', letterSpacing: 2 },
  cardTitle:   { fontSize: 18, color: '#D8D8E8' },
  progressBg:  { height: 4, backgroundColor: '#1C1C44', borderRadius: 2, overflow: 'hidden' },
  progressFill:{ height: '100%', backgroundColor: '#F9C44A', borderRadius: 2 },
  progressText:{ fontSize: 11, color: '#606088' },
  tags:        { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tag: {
    paddingHorizontal: 10, paddingVertical: 4,
    borderRadius: 20, borderWidth: 1, borderColor: '#282855',
    fontSize: 10, color: '#B0B0CC',
  },
  actions:     { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  actionBtn: {
    width: '45%',
    backgroundColor: '#111133',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#282855',
    padding: 20,
    alignItems: 'center',
    gap: 8,
  },
  actionLabel: { fontSize: 12, color: '#8888AA', textAlign: 'center' },
})
