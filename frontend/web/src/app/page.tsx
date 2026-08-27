"use client"
import Link from 'next/link'

const PATHS = [
  { key: 'FOOL',      name: 'O Louco',      icon: '🌀', archetype: 'Filosofo / Viajante',       start: 'Estudante do Caos' },
  { key: 'OBSERVER',  name: 'O Observador',  icon: '👁', archetype: 'Psicologo / Analista',       start: 'Percebedor de Padroes' },
  { key: 'ALCHEMIST', name: 'O Alquimista',  icon: '⚗',  archetype: 'Nutricionista / Curandeiro', start: 'Preparador de Ervas' },
  { key: 'GUARDIAN',  name: 'O Guardiao',    icon: '🛡', archetype: 'Terapeuta / Protetor',       start: 'Sentinela do Limiar' },
  { key: 'ARCHITECT', name: 'O Arquiteto',   icon: '🏛', archetype: 'Estrategista / Construtor',  start: 'Tracador de Planos' },
]

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16"
      style={{ background: 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 80%)' }}>

      {/* Nevoa decorativa */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="fog-pulse absolute top-0 left-1/4 w-96 h-96 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(56,56,102,0.4) 0%, transparent 70%)' }} />
        <div className="fog-pulse absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(249,196,74,0.08) 0%, transparent 70%)', animationDelay: '2s' }} />
      </div>

      <div className="relative z-10 max-w-4xl w-full text-center space-y-12">
        {/* Logo / Titulo */}
        <div className="space-y-4">
          <div className="text-6xl font-serif text-fog-100 tracking-widest">
            DARWIN
          </div>
          <p className="text-fog-300 text-sm tracking-widest uppercase">
            Sistema de Evolucao Humana
          </p>
          <p className="text-fog-400 text-xs italic max-w-md mx-auto">
            "O misterio nao existe para ser resolvido. Existe para ser habitado."
          </p>
          <div className="w-24 h-px bg-gold-500 mx-auto opacity-60" />
        </div>

        {/* Caminhos */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {PATHS.map((p) => (
            <Link key={p.key} href={`/path/${p.key.toLowerCase()}`}
              className="group relative p-5 rounded-2xl border border-fog-700 bg-fog-900/60 hover:border-gold-500/50 transition-all duration-300 text-left">
              <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"
                style={{ background: 'radial-gradient(circle at top left, rgba(249,196,74,0.05) 0%, transparent 60%)' }} />
              <div className="relative">
                <span className="text-3xl">{p.icon}</span>
                <h3 className="mt-3 text-fog-100 font-medium text-lg">{p.name}</h3>
                <p className="text-fog-400 text-xs mt-1">{p.archetype}</p>
                <p className="text-fog-500 text-xs mt-3 font-mono">Nivel 9 -- {p.start}</p>
              </div>
            </Link>
          ))}
        </div>

        {/* Acoes */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/login"
            className="px-8 py-3 rounded-xl bg-gold-500 text-fog-900 font-medium text-sm hover:bg-gold-400 transition gold-glow">
            Iniciar Jornada
          </Link>
          <Link href="/login"
            className="px-8 py-3 rounded-xl border border-fog-600 text-fog-300 text-sm hover:border-fog-400 hover:text-fog-100 transition">
            Ja sou Beyonder
          </Link>
        </div>

        {/* Rodape */}
        <p className="text-fog-600 text-xs">
          Desenvolvido por psicologos, terapeutas, psiquiatras, nutricionistas e filosofos.
          <br />Baseado nos principios narrativos de Lord of Mysteries.
        </p>
      </div>
    </main>
  )
}
