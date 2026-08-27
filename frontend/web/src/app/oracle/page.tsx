"use client"
import { useState } from 'react'
import { api } from '@/lib/api'

export default function OraclePage() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const ask = async () => {
    if (!question.trim()) return
    setLoading(true)
    setResponse('')
    try {
      const res = await api.oracle.consult(question)
      setResponse(res.response)
    } catch (e: any) {
      setResponse('O Oraculo permanece em silencio. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>
      <div className="max-w-xl w-full space-y-6">

        {/* Header */}
        <div className="text-center space-y-2">
          <div className="text-5xl">🔮</div>
          <h1 className="text-2xl font-serif text-fog-100">O Oraculo</h1>
          <p className="text-fog-500 text-xs italic">
            Agente Safira -- Psicologia, Neurociencia e Lord of Mysteries
          </p>
        </div>

        {/* Input */}
        <div className="space-y-3">
          <textarea
            rows={4}
            placeholder="O que voce quer compreender sobre sua jornada?"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            className="w-full bg-fog-900/80 border border-fog-700 rounded-2xl px-5 py-4 text-fog-200 text-sm placeholder-fog-600 focus:outline-none focus:border-gold-500/50 resize-none"
          />
          <button onClick={ask} disabled={loading || !question.trim()}
            className="w-full py-3 rounded-xl bg-gold-500 text-fog-900 font-medium text-sm hover:bg-gold-400 transition disabled:opacity-50">
            {loading ? 'O Oraculo consulta a nevoa...' : 'Consultar o Oraculo'}
          </button>
        </div>

        {/* Resposta */}
        {response && (
          <div className="rounded-2xl border border-gold-500/30 bg-fog-900/60 p-6">
            <p className="text-fog-400 text-xs mb-3 uppercase tracking-widest">Resposta do Oraculo</p>
            <p className="text-fog-200 text-sm leading-relaxed italic">{response}</p>
          </div>
        )}

        <a href="/dashboard" className="block text-center text-fog-600 text-xs hover:text-fog-400 transition">
          Voltar ao painel
        </a>
      </div>
    </main>
  )
}
