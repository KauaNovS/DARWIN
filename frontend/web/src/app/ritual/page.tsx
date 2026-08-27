"use client"
import { useState } from 'react'
import { api } from '@/lib/api'

const today = new Date().toISOString().split('T')[0]

function Slider({ label, name, max = 10, value, onChange }: any) {
  return (
    <div>
      <div className="flex justify-between text-xs text-fog-400 mb-1">
        <span>{label}</span>
        <span className="text-gold-400 font-mono">{value ?? '--'}</span>
      </div>
      <input type="range" min={1} max={max} value={value ?? 5}
        onChange={e => onChange(name, Number(e.target.value))}
        className="w-full accent-gold-500 cursor-pointer" />
    </div>
  )
}

export default function RitualPage() {
  const [form, setForm] = useState<Record<string, any>>({ date: today })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const set = (k: string, v: any) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    setLoading(true)
    try {
      const res = await api.rituals.register(form)
      setResult(res)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setLoading(false)
    }
  }

  if (result) return (
    <main className="min-h-screen flex items-center justify-center p-6"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>
      <div className="max-w-md w-full rounded-2xl border border-fog-700 bg-fog-900/80 p-8 space-y-4 text-center">
        <div className="text-4xl">
          {result.potion_score >= 70 ? '✨' : result.potion_score >= 40 ? '🌒' : '🌑'}
        </div>
        <h2 className="text-fog-100 text-xl">{result.message}</h2>
        <div className="text-gold-400 text-3xl font-mono">{result.potion_score?.toFixed(1)}</div>
        <p className="text-fog-400 text-xs">score da pocao</p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-xl border border-fog-700 p-3">
            <p className="text-fog-500 text-xs">XP ganho</p>
            <p className="text-gold-400 font-mono">+{result.xp_gained?.toFixed(1)}</p>
          </div>
          <div className="rounded-xl border border-fog-700 p-3">
            <p className="text-fog-500 text-xs">Digestao</p>
            <p className="text-fog-200 font-mono">{result.new_digestion?.toFixed(1)}%</p>
          </div>
        </div>
        {result.shadow_analysis?.notes && (
          <p className="text-fog-500 text-xs italic border-t border-fog-800 pt-4">
            {result.shadow_analysis.notes}
          </p>
        )}
        <a href="/dashboard" className="block mt-4 text-fog-400 text-xs hover:text-fog-200 transition">
          Voltar ao painel
        </a>
      </div>
    </main>
  )

  return (
    <main className="min-h-screen p-6"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-serif text-fog-100">Ritual Diario</h1>
          <p className="text-fog-400 text-sm mt-1">{today} -- Registre os ingredientes de hoje</p>
        </div>

        <div className="rounded-2xl border border-fog-700 bg-fog-900/60 p-6 space-y-6">

          <div>
            <p className="text-fog-300 text-sm font-medium mb-4">Corpo</p>
            <div className="space-y-4">
              <Slider label="Horas de sono" name="sleep_hours" max={10}
                value={form.sleep_hours} onChange={set} />
              <Slider label="Qualidade do sono" name="sleep_quality" max={10}
                value={form.sleep_quality} onChange={set} />
              <Slider label="Hidratacao (x300ml)" name="water_ml" max={10}
                value={form.water_ml ? Math.round(form.water_ml/300) : undefined}
                onChange={(k: string, v: number) => set('water_ml', v * 300)} />
              <Slider label="Nutricao (1-10)" name="nutrition_score" max={10}
                value={form.nutrition_score} onChange={set} />
              <Slider label="Movimento (min)" name="movement_minutes" max={12}
                value={form.movement_minutes ? Math.round(form.movement_minutes/10) : undefined}
                onChange={(k: string, v: number) => set('movement_minutes', v * 10)} />
            </div>
          </div>

          <div>
            <p className="text-fog-300 text-sm font-medium mb-4">Mente</p>
            <div className="space-y-4">
              <Slider label="Leitura (min)" name="reading_minutes" max={10}
                value={form.reading_minutes ? Math.round(form.reading_minutes/10) : undefined}
                onChange={(k: string, v: number) => set('reading_minutes', v * 10)} />
              <Slider label="Meditacao (min)" name="meditation_minutes" max={9}
                value={form.meditation_minutes ? Math.round(form.meditation_minutes/5) : undefined}
                onChange={(k: string, v: number) => set('meditation_minutes', v * 5)} />
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" checked={!!form.journaling}
                  onChange={e => set('journaling', e.target.checked)}
                  className="w-4 h-4 accent-gold-500" />
                <span className="text-fog-300 text-sm">Journaling realizado hoje</span>
              </label>
            </div>
          </div>

          <div>
            <p className="text-fog-300 text-sm font-medium mb-4">Emocao</p>
            <div className="space-y-4">
              <Slider label="Estado emocional" name="emotional_state" max={10}
                value={form.emotional_state} onChange={set} />
              <Slider label="Nivel de ansiedade" name="anxiety_level" max={10}
                value={form.anxiety_level} onChange={set} />
              <Slider label="Conexao social" name="social_connection" max={10}
                value={form.social_connection} onChange={set} />
            </div>
          </div>

          <div>
            <p className="text-fog-300 text-sm font-medium mb-3">Anotacoes</p>
            <div className="space-y-3">
              {[
                { k: 'insights', label: 'Insights do dia' },
                { k: 'gratitude', label: 'Gratidao' },
                { k: 'notes', label: 'Notas livres' },
              ].map(f => (
                <textarea key={f.k} rows={2} placeholder={f.label}
                  value={form[f.k] || ''}
                  onChange={e => set(f.k, e.target.value)}
                  className="w-full bg-fog-800/50 border border-fog-700 rounded-xl px-4 py-3 text-fog-200 text-sm placeholder-fog-600 focus:outline-none focus:border-gold-500/50 resize-none" />
              ))}
            </div>
          </div>

          <button onClick={submit} disabled={loading}
            className="w-full py-3 rounded-xl bg-gold-500 text-fog-900 font-medium text-sm hover:bg-gold-400 transition disabled:opacity-50">
            {loading ? 'Calculando pocao...' : 'Registrar Ritual'}
          </button>
        </div>
      </div>
    </main>
  )
}
