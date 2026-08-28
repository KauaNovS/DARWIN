import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

const PATHS = [
  {
    slug: "estrategista",
    name: "Caminho do Estrategista",
    archetype: "Observador → Arquiteto Contextual",
    philosophy:
      "Observe antes de agir. Escute antes de concluir. Leia padrões antes de interpretar. Toda interação contém informação oculta.",
    description:
      "Desenvolve percepção, leitura de contexto, análise e tomada de decisão sob pressão. Para quem quer operar com inteligência e precisão.",
    color: "#3B82F6",
    icon: "Eye",
    sequences: [
      { number: 9, name: "Observador", identity: "Alguém que percebe antes de agir", purpose: "Transformar reatividade em percepção consciente", actionMethod: "Observe antes de agir. Escute antes de concluir. Leia padrões antes de interpretar.", potionName: "Poção do Observador", potionPurpose: "Transformar reatividade em percepção consciente", ingredients: [
        { name: "Observação diária", type: "PRACTICE", description: "Registrar observações de comportamentos e padrões no dia", weight: 0.20, difficulty: 3 },
        { name: "Silêncio estratégico", type: "EMOTIONAL", description: "Ouvir antes de reagir em conversas importantes", weight: 0.15, difficulty: 4 },
        { name: "Leitura de padrões", type: "INTELLECTUAL", description: "Identificar padrões em pessoas e ambientes", weight: 0.20, difficulty: 5 },
        { name: "Registro de conversas", type: "RECORD", description: "Analisar conversas importantes após ocorrerem", weight: 0.15, difficulty: 3 },
        { name: "Estudo de comportamento humano", type: "INTELLECTUAL", description: "Ler e aplicar conceitos de psicologia comportamental", weight: 0.15, difficulty: 4 },
        { name: "Prova em ambiente real", type: "APPLICATION", description: "Observar e mapear dinâmica social em ambiente desconhecido", weight: 0.15, difficulty: 6 },
      ]},
      { number: 8, name: "Analista", identity: "Alguém que conecta padrões e extrai estrutura", purpose: "Transformar observação em análise estruturada", actionMethod: "Não apenas observe. Conecte. Encontre a estrutura por trás do comportamento.", potionName: "Poção do Analista", potionPurpose: "Desenvolver raciocínio estrutural e conexão de padrões", ingredients: [
        { name: "Análise de decisões passadas", type: "RECORD", description: "Revisar e analisar decisões importantes da semana", weight: 0.25, difficulty: 5 },
        { name: "Mapeamento de sistemas", type: "INTELLECTUAL", description: "Identificar como sistemas ao redor funcionam", weight: 0.25, difficulty: 6 },
        { name: "Previsão de comportamento", type: "APPLICATION", description: "Prever como pessoas ou sistemas vão se comportar e validar", weight: 0.30, difficulty: 7 },
        { name: "Raciocínio contrafactual", type: "INTELLECTUAL", description: "Analisar o que teria acontecido se a decisão fosse diferente", weight: 0.20, difficulty: 6 },
      ]},
      { number: 7, name: "Tático", identity: "Alguém que transforma análise em ação precisa", purpose: "Transformar raciocínio em execução estratégica", actionMethod: "Analise, decida e execute com precisão. Evite análise sem ação.", potionName: "Poção do Tático", potionPurpose: "Desenvolver execução estratégica baseada em análise", ingredients: [
        { name: "Decisão sob pressão", type: "DIFFICULTY", description: "Tomar decisões importantes em contextos de pressão real", weight: 0.30, difficulty: 7 },
        { name: "Planejamento reverso", type: "INTELLECTUAL", description: "Partir do objetivo final e planejar os passos para trás", weight: 0.25, difficulty: 6 },
        { name: "Execução com dados limitados", type: "APPLICATION", description: "Agir decisivamente com informação incompleta", weight: 0.25, difficulty: 8 },
        { name: "Revisão de resultados", type: "RECORD", description: "Analisar resultados de decisões e extrair aprendizados", weight: 0.20, difficulty: 5 },
      ]},
    ],
  },
  {
    slug: "executor",
    name: "Caminho do Executor",
    archetype: "Iniciante → Operador Absoluto",
    philosophy:
      "Aja antes de negociar com a inércia. Movimento gera clareza. Conclusão vale mais que intenção. Não espere motivação para executar.",
    description:
      "Desenvolve capacidade de ação, consistência, resistência e finalização. Para quem quer transformar intenção em execução real.",
    color: "#EF4444",
    icon: "Zap",
    sequences: [
      { number: 9, name: "Iniciante Consciente", identity: "Alguém que age antes de se sentir pronto", purpose: "Transformar inércia em movimento consciente", actionMethod: "Execute uma ação real por dia. Registre tudo. Não permita que intenção substitua execução.", potionName: "Poção do Movimento", potionPurpose: "Transformar inércia em execução consistente", ingredients: [
        { name: "Uma tarefa principal por dia", type: "PRACTICE", description: "Executar a tarefa mais importante do dia sem negociar com a inércia", weight: 0.30, difficulty: 4 },
        { name: "Registro diário de execução", type: "RECORD", description: "Registrar o que foi feito e o que foi evitado", weight: 0.20, difficulty: 2 },
        { name: "Resistência ao conforto", type: "DIFFICULTY", description: "Executar algo desconfortável antes do lazer", weight: 0.25, difficulty: 5 },
        { name: "Finalização completa", type: "DOMAIN", description: "Terminar o que começar — sem tarefas pela metade", weight: 0.25, difficulty: 5 },
      ]},
      { number: 8, name: "Consistente", identity: "Alguém que executa independente do estado emocional", purpose: "Transformar execução episódica em consistência real", actionMethod: "Execute mesmo quando não está motivado. Especialmente quando não está motivado.", potionName: "Poção da Consistência", potionPurpose: "Desenvolver execução independente de motivação", ingredients: [
        { name: "Sequência sem interrupção", type: "REPETITION", description: "Manter a rotina de execução por 14 dias sem quebrar", weight: 0.35, difficulty: 6 },
        { name: "Execução em dias ruins", type: "DIFFICULTY", description: "Executar a tarefa principal mesmo em dias de baixa energia", weight: 0.35, difficulty: 7 },
        { name: "Revisão de inconsistências", type: "CORRECTION", description: "Identificar e corrigir padrões de evitação", weight: 0.30, difficulty: 5 },
      ]},
    ],
  },
  {
    slug: "inteligencia",
    name: "Caminho da Inteligência",
    archetype: "Aprendiz → Mestre Cognitivo",
    philosophy:
      "Observe padrões antes de agir. Entenda sistemas antes de expandir. Transforme conhecimento em processo. Transforme processo em estrutura.",
    description:
      "Desenvolve aprendizado profundo, síntese, conexão de padrões e raciocínio sistêmico. Para quem quer expandir capacidade cognitiva real.",
    color: "#8B5CF6",
    icon: "Brain",
    sequences: [
      { number: 9, name: "Aprendiz", identity: "Alguém que absorve com intenção", purpose: "Transformar consumo passivo em aprendizado ativo", actionMethod: "Leia para aplicar. Estude para transformar. Conhecimento sem uso é ilusão.", potionName: "Poção do Aprendizado", potionPurpose: "Transformar consumo passivo em assimilação real", ingredients: [
        { name: "Leitura ativa diária", type: "INTELLECTUAL", description: "Ler com caneta na mão — sublinhar, questionar, conectar", weight: 0.25, difficulty: 4 },
        { name: "Registro de aprendizados", type: "RECORD", description: "Registrar o que foi aprendido em linguagem própria", weight: 0.25, difficulty: 3 },
        { name: "Aplicação prática", type: "APPLICATION", description: "Usar o que foi aprendido em uma situação real da semana", weight: 0.30, difficulty: 5 },
        { name: "Revisão espaçada", type: "REPETITION", description: "Revisar aprendizados de dias anteriores", weight: 0.20, difficulty: 4 },
      ]},
    ],
  },
  {
    slug: "comunicacao",
    name: "Caminho da Comunicação",
    archetype: "Ouvinte → Influenciador Estratégico",
    philosophy:
      "Fale para transformar. Escreva para clarificar. Escute para compreender. Toda comunicação é uma oportunidade de gerar impacto.",
    description:
      "Desenvolve expressão, persuasão, escuta ativa e influência. Para quem quer transformar pensamento em impacto real.",
    color: "#F59E0B",
    icon: "MessageCircle",
    sequences: [
      { number: 9, name: "Ouvinte", identity: "Alguém que escuta antes de responder", purpose: "Transformar comunicação reativa em comunicação consciente", actionMethod: "Escute completamente antes de responder. Faça perguntas antes de concluir.", potionName: "Poção da Escuta", potionPurpose: "Desenvolver escuta real e comunicação consciente", ingredients: [
        { name: "Escuta ativa em conversas", type: "PRACTICE", description: "Praticar escuta sem interromper e sem preparar resposta enquanto ouve", weight: 0.30, difficulty: 4 },
        { name: "Registro de conversas importantes", type: "RECORD", description: "Anotar o que foi comunicado e o que ficou subentendido", weight: 0.25, difficulty: 3 },
        { name: "Reformulação", type: "APPLICATION", description: "Reformular o que o outro disse antes de responder", weight: 0.25, difficulty: 5 },
        { name: "Silêncio consciente", type: "EMOTIONAL", description: "Sustentar silêncio em momentos de tensão sem reagir impulsivamente", weight: 0.20, difficulty: 6 },
      ]},
    ],
  },
  {
    slug: "disciplina",
    name: "Caminho da Disciplina",
    archetype: "Desordenado → Arquiteto de Hábitos",
    philosophy:
      "Disciplina não é punição. É a estrutura que liberta. Rotina sólida gera liberdade real.",
    description:
      "Desenvolve autocontrole, consistência de hábitos e resistência à inércia. Para quem quer construir estrutura operacional real.",
    color: "#10B981",
    icon: "Target",
    sequences: [
      { number: 9, name: "Iniciante Estruturado", identity: "Alguém que segue uma rotina básica", purpose: "Criar estrutura mínima sustentável", actionMethod: "Defina 3 hábitos inegociáveis. Execute todos os dias. Não negocie com exceções.", potionName: "Poção da Estrutura", potionPurpose: "Criar base de rotina sustentável", ingredients: [
        { name: "3 hábitos diários inegociáveis", type: "REPETITION", description: "Definir e executar 3 hábitos todos os dias sem exceção", weight: 0.40, difficulty: 5 },
        { name: "Horário fixo de início", type: "PRACTICE", description: "Começar o dia no mesmo horário por 21 dias", weight: 0.30, difficulty: 5 },
        { name: "Registro de consistência", type: "RECORD", description: "Marcar todos os dias se os hábitos foram cumpridos", weight: 0.30, difficulty: 2 },
      ]},
    ],
  },
  {
    slug: "emocional",
    name: "Caminho Emocional",
    archetype: "Reativo → Operador Integrado",
    philosophy:
      "Emoções não são fraquezas. São sistemas de sinalização profunda. O objetivo não é suprimir — é compreender e integrar.",
    description:
      "Desenvolve regulação emocional, estabilidade e inteligência interna. Para quem quer parar de ser controlado por estados internos.",
    color: "#EC4899",
    icon: "Heart",
    sequences: [
      { number: 9, name: "Observador Emocional", identity: "Alguém que percebe emoções antes de ser controlado por elas", purpose: "Transformar reatividade emocional em consciência interna", actionMethod: "Identifique a emoção antes de agir. Nomeie. Localize no corpo. Decida com clareza.", potionName: "Poção da Consciência Emocional", potionPurpose: "Desenvolver percepção e regulação emocional básica", ingredients: [
        { name: "Diário emocional diário", type: "RECORD", description: "Registrar emoções predominantes do dia e seus gatilhos", weight: 0.30, difficulty: 3 },
        { name: "Pausa antes de reagir", type: "EMOTIONAL", description: "Criar um intervalo consciente antes de responder emocionalmente", weight: 0.30, difficulty: 6 },
        { name: "Mapeamento de gatilhos", type: "INTELLECTUAL", description: "Identificar o que ativa estados emocionais intensos", weight: 0.20, difficulty: 5 },
        { name: "Regulação física", type: "PHYSICAL", description: "Usar respiração ou movimento para regular emoções intensas", weight: 0.20, difficulty: 4 },
      ]},
    ],
  },
  {
    slug: "fisico",
    name: "Caminho Físico",
    archetype: "Sedentário → Operador de Elite",
    philosophy:
      "O corpo é a infraestrutura da mente. Sem corpo estável, não existe mente estável. Sem mente estável, não existe evolução.",
    description:
      "Desenvolve energia, resistência física e capacidade operacional biológica. Para quem quer o corpo como aliado da evolução.",
    color: "#F97316",
    icon: "Activity",
    sequences: [
      { number: 9, name: "Ativo Básico", identity: "Alguém que respeita o corpo como infraestrutura", purpose: "Criar base física mínima sustentável", actionMethod: "Mova-se todos os dias. Durma o suficiente. Hidrate-se. Sem isso, tudo perde eficiência.", potionName: "Poção da Base Física", potionPurpose: "Criar estabilidade biológica básica", ingredients: [
        { name: "Movimento diário", type: "PHYSICAL", description: "Fazer pelo menos 30 minutos de atividade física por dia", weight: 0.30, difficulty: 4 },
        { name: "Sono regulado", type: "PRACTICE", description: "Dormir e acordar no mesmo horário por 14 dias", weight: 0.30, difficulty: 5 },
        { name: "Hidratação consciente", type: "REPETITION", description: "Beber 2L de água por dia e registrar", weight: 0.20, difficulty: 2 },
        { name: "Registro de energia", type: "RECORD", description: "Avaliar nível de energia ao acordar e à tarde", weight: 0.20, difficulty: 2 },
      ]},
    ],
  },
  {
    slug: "financeiro",
    name: "Caminho Financeiro",
    archetype: "Desordenado → Arquiteto Econômico",
    philosophy:
      "Dinheiro não deve controlar o usuário. Mas também não deve ser ignorado. Ele deve ser compreendido, organizado e usado como ferramenta de evolução.",
    description:
      "Desenvolve controle financeiro, consciência econômica e estabilidade. Para quem quer transformar a relação com dinheiro.",
    color: "#059669",
    icon: "DollarSign",
    sequences: [
      { number: 9, name: "Consciente Financeiro", identity: "Alguém que sabe para onde vai o dinheiro", purpose: "Criar consciência financeira básica", actionMethod: "Registre todo gasto. Sem exceção. Consciência antes de controle.", potionName: "Poção da Consciência Financeira", potionPurpose: "Desenvolver rastreamento e consciência de padrões financeiros", ingredients: [
        { name: "Registro de todos os gastos", type: "RECORD", description: "Registrar cada gasto do dia, por menor que seja", weight: 0.40, difficulty: 4 },
        { name: "Análise semanal", type: "INTELLECTUAL", description: "Revisar os gastos da semana e identificar padrões", weight: 0.30, difficulty: 4 },
        { name: "Identificação de gastos emocionais", type: "EMOTIONAL", description: "Identificar compras motivadas por emoção e não por necessidade", weight: 0.30, difficulty: 5 },
      ]},
    ],
  },
];

async function main() {
  console.log("🌱 Seeding Darwin database...");

  // Admin user
  const hashedPassword = await bcrypt.hash("darwin@2026", 12);
  await prisma.user.upsert({
    where: { email: "admin@darwin.app" },
    update: {},
    create: {
      email: "admin@darwin.app",
      name: "Darwin Admin",
      password: hashedPassword,
      role: "ADMIN",
      metaFinal: "Construir o Darwin como sistema operacional de evolução humana",
      identityNow: "Arquiteto em formação",
      identityGoal: "Operador de elite — alguém que torna a evolução inevitável",
    },
  });

  // Seed Paths, Sequences, Potions, Ingredients
  for (const pathData of PATHS) {
    const { sequences, ...pathFields } = pathData;

    const path = await prisma.path.upsert({
      where: { slug: pathFields.slug },
      update: pathFields,
      create: pathFields,
    });

    for (const seqData of sequences) {
      const { ingredients, potionName, potionPurpose, ...seqFields } = seqData;

      const sequence = await prisma.sequence.upsert({
        where: { pathId_number: { pathId: path.id, number: seqFields.number } },
        update: { ...seqFields, pathId: path.id },
        create: { ...seqFields, pathId: path.id },
      });

      if (potionName) {
        const potion = await prisma.potion.upsert({
          where: { sequenceId: sequence.id },
          update: { name: potionName, purpose: potionPurpose, actingMethod: seqFields.actionMethod },
          create: { sequenceId: sequence.id, name: potionName, purpose: potionPurpose, actingMethod: seqFields.actionMethod },
        });

        for (const ing of ingredients) {
          const existing = await prisma.ingredient.findFirst({
            where: { potionId: potion.id, name: ing.name },
          });
          if (!existing) {
            await prisma.ingredient.create({ data: { ...ing, potionId: potion.id } });
          }
        }
      }
    }

    console.log(`  ✓ ${pathFields.name}`);
  }

  console.log("\n✅ Darwin seeded successfully!");
  console.log("   Admin: admin@darwin.app / darwin@2026");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
