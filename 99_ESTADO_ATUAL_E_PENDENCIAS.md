# DARWIN GENESIS — ESTADO ATUAL E PENDÊNCIAS

> CHECKPOINT operacional para continuar o projeto entre conversas.
> Formato definido em `00_MASTER.md` (seção "Regra de continuidade" e "Regra de documentação").

## IMPORTANTE

Este checkpoint não inventa percentual de conclusão. O estado real de cada módulo deve ser validado
contra o código existente antes de marcar algo como implementado. Ver `README.md` para o relato
detalhado, testado, do que sobe e do que ainda é placeholder.

## SESSÃO — Integração da camada instintiva (Darwin 2.0) ao backend

### Objetivo atual
Corrigir os bugs da camada instintiva ("Darwin 2.0" — Sentinel, Eco Listener, Halter Guardian, Wave
Index, Genetic Memory, Trust Boundary) e integrá-la de fato ao `backend/`, que já sobe e funciona.

### Módulos envolvidos
Onboarding (04_MEMORIA / 05_CONTEXTO_PADROES_APRENDIZADO), Eco (escuta comportamental implícita),
Halter (proteção contra sobrecarga), Wave Index / 08_XP_METRICAS_DOMINIO_ASCENSAO (matemática de
domínio), Memória Genética / 04_MEMORIA (compressão de 30 dias), Trust Boundary / 11_AUTOMACAO
(autonomia delegada), 09_IA_E_INTELIGENCIA (insights).

### Arquivos envolvidos
- Removido: `app/` (scaffold antigo, desconectado do backend, com imports quebrados)
- Criados: `backend/models/genome.py`, `backend/models/stress.py`,
  `backend/services/instinct/{__init__,wave_index,trust_boundary,eco_listener,halter_guardian,sentinel,genetic_memory,ai_service}.py`,
  `backend/api/routes/instinct.py`
- Modificados: `backend/main.py` (registra o router `/api/instinct`), `backend/requirements.txt`
  (adiciona `httpx`), `README.md`

### Implementado nesta sessão
- `GET /api/instinct/onboarding/questions` — perguntas diárias da fase atual
- `POST /api/instinct/onboarding/answer` — registra resposta e tenta avançar de fase
- `GET /api/instinct/onboarding/phase` — fase atual + dias ativos
- `POST /api/instinct/process` — processa Eco + Halter + Wave Index + Genoma + Trust Boundary + insight de IA
- `POST /api/instinct/feedback` — ajusta a confiança do Trust Boundary

### Alterado nesta sessão
Todos os serviços da camada instintiva foram reescritos para importar de `core.database` /
`core.dependencies` deste backend (assíncronos e já testados) em vez do módulo `app.core.database`, que
nunca existiu no repositório e vinha de um material de referência externo (documento colado numa
conversa com outra IA).

### Testado
- `python3 -m py_compile` em todos os `.py` do `backend/` — sem erro de sintaxe.
- App real importado via `from main import app` — sem `ImportError` (prova de que os imports resolvem
  em runtime, não só sintaticamente).
- `TestClient(app).get("/openapi.json")` confirma as 5 rotas `/api/instinct/*` registradas.
- NÃO testado contra Postgres/Neo4j/Redis reais rodando — precisa de um ambiente com esses serviços de
  pé (Docker Compose local ou Render + Neo4j Aura, como descrito no `README.md`).

### Erros corrigidos (bugs reais que impediam a execução)
1. Imports para `app.core.database` / `app.models.genome` / `app.models.stress` — módulos que nunca
   existiram neste repositório.
2. `GeneticMemory.distill()` chamava `await result.fetch()` — esse método não existe na API assíncrona
   do driver oficial do Neo4j (`neo4j` >= 5); corrigido para `[record async for record in result]`.
3. `OnboardingSentinel.get_days_active()` contava uma chave Redis por *resposta* como se fosse um dia
   inteiro — um único dia com 3 respostas virava "3 dias ativos", inflando artificialmente o avanço de
   fase (FETUS → INFANT em ~3 dias reais em vez de 7). Corrigido: cada dia grava uma única chave
   carimbada com a data (`YYYY-MM-DD`).

### Decisões
- Não duplicar uma segunda stack de conexões (Postgres/Neo4j/Redis) só para a camada instintiva — ela
  reaproveita `core.database` do backend, testado e funcional, em vez do `docker-compose.yml` e
  `config.py` paralelos que vinham junto com o código colado.
- `EvolutionOrchestrator` do material original não foi trazido como classe separada: sua função
  (avançar sequência por domínio) já existe em `services/evolution/sequence.py` (`SequenceManager`).
  Conectar os dois é a próxima tarefa, não uma duplicação de lógica.

### Pendências
- Testar `/api/instinct/*` contra Postgres/Neo4j/Redis reais rodando.
- `SequenceManager.advance_sequence` ainda não usa `WaveIndex` para decidir se o usuário avança de nível
  (hoje `services/evolution/sequence.py` não recebe dado de domínio nenhum).
- Frontend (web/mobile) não tem telas para a camada instintiva ainda — pela "Regra de UI" do
  `00_MASTER.md`, a funcionalidade não é considerada completa sem isso.
- Agentes Atlas/Orion continuam stubs (pendência herdada de sessões anteriores, documentada no README).
- Recomendação, notificações, ingredientes de poções, busca de nós/relações e transcrição de voz
  seguem como TODO (idem, herdado, ver README).

### Próxima tarefa
Conectar `SequenceManager` ao `WaveIndex` para o avanço de sequência usar domínio real (variância sob
pressão) em vez de critério manual, e desenhar as telas de onboarding/insight no frontend web.
