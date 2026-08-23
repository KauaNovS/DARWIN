// frontend/web/src/pages/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { useDarwin } from '../hooks/useDarwin';
import { MetricCard } from '../components/MetricCard';
import { TaskList } from '../components/TaskList';
import { Timeline } from '../components/Timeline';
import { EnergyChart } from '../components/EnergyChart';

export const Dashboard: React.FC = () => {
  const { 
    tasks, 
    metrics, 
    energy, 
    timeline,
    sequences,
    loading 
  } = useDarwin();

  if (loading) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Darwin Genesis</h1>
        <div className="user-status">
          <EnergyIndicator value={energy.current} />
          <span className="date">{new Date().toLocaleDateString()}</span>
        </div>
      </header>

      <section className="metrics-grid">
        <MetricCard 
          label="Energia" 
          value={energy.current} 
          max={10}
          trend={energy.trend}
        />
        <MetricCard 
          label="Tarefas Hoje" 
          value={tasks.today.total} 
          description={`${tasks.today.done} concluídas`}
        />
        <MetricCard 
          label="XP" 
          value={metrics.xp.total} 
          description={`+${metrics.xp.today} hoje`}
        />
        <MetricCard 
          label="Sequência" 
          value={sequences.current.name} 
          description={`Nível ${sequences.current.level}`}
        />
      </section>

      <section className="main-grid">
        <div className="left-column">
          <TaskList tasks={tasks.pending} />
          <EnergyChart data={energy.history} />
        </div>
        <div className="right-column">
          <Timeline events={timeline.recent} />
          <QuickActions />
        </div>
      </section>

      <section className="patterns-section">
        <PatternsList patterns={metrics.patterns} />
      </section>
    </div>
  );
};
