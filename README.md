# Darwin -- Sistema de Evolucao Humana

> *"O misterio nao existe para ser resolvido. Existe para ser habitado."*
> -- Klein, Sequencia do Louco, Nivel 1

Darwin e um sistema de desenvolvimento humano construido sobre a intersecao entre
psicologia clinica, neurociencia comportamental, nutricao funcional e filosofia estoica
-- apresentado atraves da linguagem e estetica de **Lord of Mysteries**.

A equipe por tras da logica: psicologos, terapeutas, psiquiatras, nutricionistas e
filosofos -- os melhores de suas areas, reunidos para criar o unico sistema que trata
o ser humano como um **Beyonder em ascensao**.

---

## O que e Darwin

Cada usuario e um **Beyonder** -- alguem que escolheu sair da mediocridade ordinaria
e caminhar por uma **Sequencia**. O progresso nao e gamificacao vazia. E estruturado
sobre principios reais:

- **Pocoes** = combinacoes de praticas diarias (sono, nutricao, movimento, cognicao, emocao)
- **Ingredientes** = acoes concretas registradas pelo usuario a cada dia
- **Digestao** = o sistema analisa padroes ao longo do tempo e determina se a pocao
  esta sendo absorvida
- **Sequencias** = trilhas de evolucao tematicas (9 niveis, do mais denso ao mais refinado)
- **Caminhos** = o arquetipo escolhido pelo usuario, que define quais Sequencias estao disponiveis

## Sequencias disponiveis

| Caminho        | Arquetipo                     | Nivel 9 (inicio)         | Nivel 1 (maestria)        |
|----------------|-------------------------------|--------------------------|---------------------------|
| O Louco        | Filosofo / Viajante           | Estudante do Caos        | Guardiao da Nevoa         |
| O Observador   | Psicologo / Analista          | Percebedor de Padroes    | Leitor de Almas           |
| O Alquimista   | Nutricionista / Curandeiro    | Preparador de Ervas      | Transmutador              |
| O Guardiao     | Terapeuta / Protetor          | Sentinela do Limiar      | Paladino da Psique        |
| O Arquiteto    | Estrategista / Construtor     | Tracador de Planos       | Deus dos Sistemas         |

## Como funciona a progressao

1. Usuario escolhe um **Caminho** e recebe sua **Sequencia de Nivel 9**
2. Todo dia, registra os **Ingredientes** do Ritual (sono, agua, leitura, emocao, etc.)
3. O sistema calcula o **Score da Pocao** e a **Digestao acumulada**
4. Quando a digestao atinge o limiar do nivel, o **Agente Safira** (coach de IA) avalia
   se o usuario esta pronto para subir
5. O Agente analisa: consistencia, padroes psicologicos, sombra, e gera um veredicto
6. Se aprovado: o usuario sobe para o Nivel 8 e recebe a proxima pocao

## Stack tecnica

- **Backend**: FastAPI + PostgreSQL + Neo4j + Redis
- **Frontend Web**: Next.js 14 + Tailwind CSS
- **Mobile**: React Native + Expo

## Rodar localmente

```bash
cp .env.example .env
docker-compose up --build
```
