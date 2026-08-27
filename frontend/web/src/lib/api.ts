const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

function getToken() {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('darwin_token')
}

async function request(path: string, opts: RequestInit = {}) {
  const token = getToken()
  const res = await fetch(`${API}${path}`, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(opts.headers || {}),
    },
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }))
    throw new Error(err.detail || 'Erro na requisicao')
  }
  return res.json()
}

export const api = {
  auth: {
    login: (email: string, password: string) =>
      request('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
    register: (name: string, email: string, password: string) =>
      request('/api/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
    me: () => request('/api/auth/me'),
  },
  sequences: {
    paths: () => request('/api/sequences/paths'),
    mySequence: () => request('/api/sequences/my-sequence'),
  },
  potions: {
    current: () => request('/api/potions/current'),
    allForPath: (path: string) => request(`/api/potions/all-potions/${path}`),
  },
  rituals: {
    register: (data: object) =>
      request('/api/rituals/', { method: 'POST', body: JSON.stringify(data) }),
    list: () => request('/api/rituals/'),
    today: () => request('/api/rituals/today'),
  },
  oracle: {
    consult: (text: string) =>
      request('/api/oracle/consult', { method: 'POST', body: JSON.stringify({ text }) }),
    status: () => request('/api/oracle/status'),
  },
  memory: {
    summary: () => request('/api/memory/summary'),
  },
}
