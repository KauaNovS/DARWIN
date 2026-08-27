import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Paleta Darwin -- nevoa, misterio, profundidade
        fog: {
          50:  '#f0f0f5',
          100: '#d8d8e8',
          200: '#b0b0cc',
          300: '#8888aa',
          400: '#606088',
          500: '#383866',
          600: '#282855',
          700: '#1c1c44',
          800: '#111133',
          900: '#080822',
          950: '#040411',
        },
        gold: {
          300: '#fcd47a',
          400: '#f9c44a',
          500: '#e8a820',
          600: '#b88010',
        },
        crimson: {
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
        },
        teal: {
          400: '#2dd4bf',
          500: '#14b8a6',
        }
      },
      fontFamily: {
        serif: ['Georgia', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'fog-gradient': 'radial-gradient(ellipse at top, #1c1c44 0%, #080822 70%)',
      }
    },
  },
  plugins: [],
}
export default config
