# Darwin Genesis

Scaffold de código extraído do documento `Darwin_Genesis_Code_Plan.txt` — um roadmap técnico para um
"Sistema Operacional de Evolução Humana" (memória contextual, grafo relacional, agentes de IA, automações).

## O que tem aqui

O plano original continha código já escrito, mas em formato de texto corrido, sem arquivos reais.
Este repositório organiza esse código na estrutura de pastas que o próprio plano descreve, em duas gerações:

- **`backend/`** — Fases 1–3 do plano: API FastAPI, modelos SQLAlchemy, memória viva, grafo relacional
  (Neo4j), agentes (`BaseAgent`, `SafiraAgent`, orquestrador), detecção de padrões, recomendação, automação.
- **`app/`** — a segunda geração descrita no fim do plano ("Darwin 2.0" / camada instintiva): `WaveIndex`
  (matemática de domínio), `EcoListener` (escuta implícita), `HalterGuardian` (anti-corrupção),
  `GeneticMemory` (compressão de memória), `OnboardingSentinel`, `TrustBoundary` e o endpoint único
  `POST /api/v1/instinct/process` que costura tudo isso.
- **`frontend/`** — componentes React (`Dashboard.tsx`, `GrafoVisualization.tsx`) e React Native
  (`HomeScreen.tsx`, `VoiceInput.tsx`) de exemplo.
- **`infrastructure/docker/docker-compose.yml`** e **`docker-compose.yml`** (raiz) — dois compose files
  do plano (um mais simples, outro completo com Neo4j + Redis + Postgres + backend).

## Importante — status real do código

Isto é o scaffold do **plano**, não um produto testado. Ao extrair fielmente o que estava no documento,
mantive tudo como estava, incluindo:

- Vários `# TODO: Implementar ...` deixados no próprio plano (recomendação, notificações, ingredientes
  de poções, análise de conteúdo dos agentes, etc.).
- `AtlasAgent` e `OrionAgent` eram **importados** por `services/agents/factory.py` mas nunca definidos
  no plano — adicionei stubs mínimos (`backend/services/agents/atlas.py` e `orion.py`) só para os imports
  não quebrarem. A lógica real deles precisa ser escrita.
- `core/config.py` e `core/database.py` (dentro de `backend/`) **não existiam no plano** — `main.py` e os
  models fazem `from core.config import settings` / `from core.database import Base`, então adicionei o
  mínimo de "cola" (Pydantic Settings + SQLAlchemy async engine) para o pacote ser importável. Ajuste como
  quiser.
- Não existe autenticação real (`get_current_user`, `core/security.py`), processamento de voz
  (`services/voice/processor.py`), nem `services/graph/query.py` / `services/graph/propagation.py` —
  esses módulos são referenciados em imports mas não estavam no plano. Vão precisar ser escritos antes do
  backend rodar de ponta a ponta.
- O `app/` (camada instintiva) depende de `get_redis()` e `get_neo4j_driver()` que também não têm
  implementação no plano — só as chamadas.

Ou seja: você tem a **arquitetura e uma fatia significativa da lógica** já escrita, mas para rodar de
verdade (`docker-compose up`) ainda falta preencher essas peças de infraestrutura/autenticação.

Todos os arquivos `.py` deste repositório passam em `python3 -m py_compile` (sintaxe válida) e os dois
`docker-compose.yml` são YAML válido.

## Como rodar (quando as peças faltantes estiverem prontas)

```bash
pip install -r backend/requirements.txt
cp .env.example .env   # preencha OPENAI_API_KEY etc.
docker-compose up --build
```

## Estrutura

```
darwin-genesis/
├── backend/          # Fases 1–3 do plano (API, modelos, serviços)
├── app/              # "Darwin 2.0" — camada instintiva
├── frontend/
│   ├── web/
│   └── mobile/
├── infrastructure/
│   └── docker/
├── docker-compose.yml
└── README.md
```
