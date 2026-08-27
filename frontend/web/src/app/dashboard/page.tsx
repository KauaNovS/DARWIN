"use client"
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function DashboardPage() {
  const [sequence, setSequence] = useState<any>(null)
  const [potion, setPotion] = useState<any>(null)
  const [memory, setMemory] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.sequences.mySequence(),
      api.potions.current(),
      api.memory.summary(),
    ]).then(([seq, pot, mem]) => {
      setSequence(seq)
      setPotion(pot)
      setMemory(mem)
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>
      <div className="text-fog-400 text-sm animate-pulse">A nevoa se disipa...</div>
    </div>
  )

  const digPct = potion?.progress_pct ?? 0

  return (
    <main className="min-h-screen p-6 md:p-10"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-serif text-fog-100">Sua Jornada</h1>
            <p className="text-fog-400 text-sm mt-1">
              {sequence?.path_name ?? ''} &mdash; Nivel {sequence?.level ?? '?'}: {sequence?.title ?? ''}
            </p>
          </div>
          <div className="text-right">
            <p className="text-gold-400 text-xl font-mono">{sequence?.total_xp?.toFixed(0) ?? 0} XP</p>
            <p className="text-fog-500 text-xs">total acumulado</p>
          </div>
        </div>

        {/* Pocao atual */}
        {potion && (
          <div className="rounded-2xl border border-fog-700 bg-fog-900/60 p-6 space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-fog-400 text-xs uppercase tracking-widest">Pocao Atual</p>
                <h2 className="text-fog-100 text-xl mt-1">{potion.potion_name}</h2>
              </div>
              <span className="text-gold-400 text-2xl font-mono">{digPct}%</span>
            </div>

            {/* Barra de digestao */}
            <div>
              <div className="flex justify-between text-xs text-fog-500 mb-2">
                <span>Digestao</span>
                <span>{potion.digestion_score?.toFixed(1)}% / {potion.digestion_threshold}%</span>
              </div>
              <div className="h-1.5 bg-fog-800 rounded-full overflow-hidden">
                <div className="h-full bg-gold-500 rounded-full transition-all duration-700"
                  style={{ width: `${Math.min(digPct, 100)}%` }} />
              </div>
            </div>

            {/* Ingredientes */}
            <div>
              <p className="text-fog-500 text-xs mb-2">Ingredientes da Pocao</p>
              <div className="flex flex-wrap gap-2">
                {(potion.ingredients ?? []).map((ing: string) => (
                  <span key={ing}
                    className="px-3 py-1 rounded-full text-xs border border-fog-700 text-fog-300">
                    {ing.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Grid de cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { label: 'Rituais (30d)', value: memory?.rituals_count ?? '--', unit: 'registros' },
            { label: 'Score medio', value: memory?.avg_potion_score?.toFixed(1) ?? '--', unit: '/ 100' },
            { label: 'Indice de Sombra', value: sequence?.shadow_index?.toFixed(0) ?? '--', unit: '%' },
          ].map((c) => (
            <div key={c.label} className="rounded-xl border border-fog-700 bg-fog-900/40 p-5 text-center">
              <p className="text-fog-400 text-xs">{c.label}</p>
              <p className="text-fog-100 text-3xl font-mono mt-2">{c.value}</p>
              <p className="text-fog-600 text-xs mt-1">{c.unit}</p>
            </div>
          ))}
        </div>

        {/* Navegacao rapida */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { href: '/ritual', label: 'Ritual Diario', icon: '🌙' },
            { href: '/oracle', label: 'O Oraculo', icon: '🔮' },
            { href: '/sequence', label: 'Minha Sequencia', icon: '📜' },
            { href: '/memory', label: 'Arquivo', icon: '📁' },
          ].map((item) => (
            <a key={item.href} href={item.href}
              className="flex flex-col items-center gap-2 p-4 rounded-xl border border-fog-700 bg-fog-900/40 hover:border-gold-500/40 transition text-center">
              <span className="text-2xl">{item.icon}</span>
              <span className="text-fog-300 text-xs">{item.label}</span>
            </a>
          ))}
        </div>

      </div>
    </main>
  )
}
