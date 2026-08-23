// frontend/web/src/components/GrafoVisualization.tsx
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface Node {
  id: string;
  name: string;
  type: string;
  intensity: number;
}

interface Relation {
  source: string;
  target: string;
  type: string;
  intensity: number;
}

interface GraphData {
  nodes: Node[];
  relations: Relation[];
}

export const GrafoVisualization: React.FC<{ data: GraphData }> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !data) return;

    const width = 800;
    const height = 600;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Limpa SVG
    svg.selectAll('*').remove();

    // Cria simulação de força
    const simulation = d3.forceSimulation()
      .force('link', d3.forceLink().id((d: any) => d.id))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Cria links
    const link = svg.append('g')
      .selectAll('line')
      .data(data.relations)
      .enter()
      .append('line')
      .attr('stroke', '#999')
      .attr('stroke-width', (d: any) => d.intensity * 2)
      .attr('stroke-opacity', 0.6);

    // Cria nós
    const node = svg.append('g')
      .selectAll('circle')
      .data(data.nodes)
      .enter()
      .append('circle')
      .attr('r', (d: any) => 10 + d.intensity * 5)
      .attr('fill', (d: any) => getColorByType(d.type))
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended))
      .on('click', (event, d) => {
        // TODO: Abrir detalhes do nó
        console.log('Node clicked:', d);
      });

    // Adiciona labels
    const label = svg.append('g')
      .selectAll('text')
      .data(data.nodes)
      .enter()
      .append('text')
      .text((d: any) => d.name)
      .attr('font-size', '10px')
      .attr('dx', 12)
      .attr('dy', 4);

    // Atualiza posições
    simulation.nodes(data.nodes).on('tick', ticked);
    simulation.force('link').links(data.relations);

    function ticked() {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      label
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    }

    function dragstarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    function getColorByType(type: string): string {
      const colors: Record<string, string> = {
        'person': '#4CAF50',
        'emotion': '#FF5722',
        'task': '#2196F3',
        'habit': '#9C27B0',
        'event': '#FF9800',
        'idea': '#00BCD4',
        'company': '#8BC34A',
        'agent': '#E91E63'
      };
      return colors[type] || '#607D8B';
    }

    return () => {
      simulation.stop();
    };
  }, [data]);

  return <svg ref={svgRef} className="grafo-visualization" />;
};
