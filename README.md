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

O `backend/` **já sobe de verdade**: `uvicorn main:app` inicia sem erro e todas as 9 rotas
(`/api/auth`, `/api/users`, `/api/tasks`, `/api/agents`, `/api/memory`, `/api/graph`, `/api/evolution`,
`/api/health`, `/api/instinct`) respondem em `/docs`. Isso foi testado rodando o servidor de verdade
(via `TestClient`, checando o `openapi.json`), não só checando a sintaxe.

### Camada instintiva ("Darwin 2.0") — agora integrada, não mais separada

A versão anterior deste README descrevia `app/` como um scaffold separado e desconectado do `backend/`
(sem `main.py` próprio, importando de um módulo `app.core.database` que nunca existiu). Esse scaffold
tinha bugs reais que impediam qualquer execução:

- Importava `app.core.database.get_redis()` / `get_neo4j_driver()` — módulo inexistente no repositório.
- Importava `app.models.genome.Genome` / `app.models.stress.StressIndex` — módulos inexistentes.
- `GeneticMemory.distill()` chamava `await result.fetch()` num `AsyncResult` do driver Neo4j — esse
  método não existe na API assíncrona (`neo4j` >= 5); precisa iterar com `async for`.
- `OnboardingSentinel.get_days_active()` contava uma chave por *resposta* como se fosse um dia — 1 dia
  com 3 respostas virava "3 dias ativos", inflando artificialmente o avanço de fase.

Esses módulos foram corrigidos e movidos para `backend/services/instinct/` (`wave_index.py`,
`trust_boundary.py`, `eco_listener.py`, `halter_guardian.py`, `sentinel.py`, `genetic_memory.py`), agora
reaproveitando `core.database` e `core.dependencies` já testados deste backend, em vez de duplicar uma
stack de conexões separada. Um `ai_service.py` novo gera insights curtos (OpenAI se `OPENAI_API_KEY`
estiver configurada, com fallback local baseado em regras caso contrário). Tudo isso é exposto em
`backend/api/routes/instinct.py`, prefixo `/api/instinct`:

- `GET /api/instinct/onboarding/questions` — perguntas diárias da fase atual
- `POST /api/instinct/onboarding/answer` — registra resposta e tenta avançar de fase
- `GET /api/instinct/onboarding/phase` — fase atual + dias ativos
- `POST /api/instinct/process` — processa Eco + Halter + Wave Index + Genoma + Trust Boundary de uma vez
- `POST /api/instinct/feedback` — feedback de aprovação/rejeição para ajustar o Trust Boundary

Para chegar até aí, além do que já estava no plano, foi necessário escrever peças que **não existiam
no documento original** (main.py importava/chamava tudo isso, mas nunca foi escrito):

- `backend/core/config.py`, `core/database.py`, `core/dependencies.py`, `core/security.py` — settings,
  conexão com Postgres/Neo4j/Redis, autenticação JWT (login/registro reais com hash de senha).
- As 7 rotas que faltavam: `api/routes/{auth,users,tasks,agents,memory,graph,evolution,health}.py`
  (só `voice.py` existia no plano).
- `services/voice/processor.py`, `services/graph/query.py`, `services/graph/propagation.py` — eram
  importados por outros arquivos mas nunca definidos.
- `services/agents/atlas.py` e `orion.py` — importados por `factory.py` mas nunca definidos (ainda são
  stubs: só devolvem `"status": "not_implemented"`, a lógica real de cada agente falta escrever).
- Também corrigi alguns bugs que já estavam no texto do plano e que quebrariam em runtime: `import json`
  faltando em `node_manager.py`, `_record_to_dict` chamado mas nunca definido em `relation_manager.py`,
  `LiveMemory.search()` chamado por `sequence.py` mas nunca definido, e um `sequence["id"]` que deveria
  ser `sequence["node"]["id"]`.

O que **ainda é TODO** (igual já estava marcado no plano original, não mudei a lógica de negócio):
recomendação, notificações, lógica real de ingredientes de poções, busca flexível de nós/relações
(`NodeManager.search`/`RelationManager.search` retornam lista vazia), transcrição de voz de verdade
(hoje é só um placeholder), e a lógica real dos agentes Atlas/Orion.

Todos os arquivos `.py` passam em `python3 -m py_compile` e os dois `docker-compose.yml` são YAML válido.

## Como rodar (quando as peças faltantes estiverem prontas)

```bash
pip install -r backend/requirements.txt
cp .env.example .env   # preencha OPENAI_API_KEY etc.
docker-compose up --build
```

## Deploy grátis na nuvem (Render)

Inclui um `render.yaml` (Blueprint) na raiz para automatizar a criação do backend + Postgres + Redis no
Render. O Neo4j **não é hospedado pelo Render** — use o [Neo4j Aura Free](https://neo4j.com/cloud/aura-free/)
(grátis) e cole a URI/usuário/senha na dashboard do Render depois.

1. Crie a instância grátis no Neo4j Aura e guarde a URI, usuário e senha.
2. No Render: **New > Blueprint**, conecte este repositório GitHub.
3. O Render vai propor criar: o Web Service (`darwin-genesis-api`), o Postgres (`darwin-genesis-db`) e o
   Key Value/Redis (`darwin-genesis-redis`) — confirme.
4. Depois de criado, abra o Web Service > Environment e preencha `NEO4J_URI`, `NEO4J_USER`,
   `NEO4J_PASSWORD` (do Aura) e `OPENAI_API_KEY` (se for usar IA).
5. O serviço vai buildar e subir sozinho. A URL pública fica em algo como
   `https://darwin-genesis-api.onrender.com/docs`.

**Limitações do plano grátis do Render:** o Web Service "dorme" depois de 15 minutos sem tráfego (o
primeiro acesso depois disso demora ~1 minuto pra acordar), e o Postgres grátis expira em 30 dias (precisa
recriar ou migrar pro pago). Serve bem para testar e mostrar o projeto, não para uso contínuo 24/7.

Se o Blueprint der erro de validação na dashboard, os mesmos serviços podem ser criados manualmente:
Web Service (Root Directory `backend`, Build Command `pip install -r requirements.txt`, Start Command
`uvicorn main:app --host 0.0.0.0 --port $PORT`), um Postgres grátis, e um Key Value grátis — depois só
copiar as URLs geradas para as variáveis de ambiente do Web Service.

## Estrutura

```
darwin-genesis/
├── backend/          # API, modelos, serviços — inclui services/instinct/ (Darwin 2.0, já integrado)
├── frontend/
│   ├── web/
│   └── mobile/
├── infrastructure/
│   └── docker/
├── docker-compose.yml
└── README.md
```
