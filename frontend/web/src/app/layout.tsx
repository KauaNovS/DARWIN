import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Darwin -- Sistema de Evolucao Humana',
  description: 'O caminho se abre para quem ousa caminhar.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-fog-gradient">
        {children}
      </body>
    </html>
  )
}
