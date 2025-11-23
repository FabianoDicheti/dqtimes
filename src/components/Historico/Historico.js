import React, { useState } from 'react';
import './Historico.css';
import { mockPrevisoes } from '../../data/mockData';

const Historico = () => {
  const [previsoes] = useState(mockPrevisoes);
  const [filtro, setFiltro] = useState('');
  const [ordenacao, setOrdenacao] = useState({ campo: 'dataCriacao', direcao: 'desc' });

  // Filtrar previsões baseado no termo de busca
  const previsoesFiltradas = previsoes.filter(previsao => {
    const termoBusca = filtro.toLowerCase();
    return (
      previsao.referencia.toLowerCase().includes(termoBusca) ||
      previsao.task.toLowerCase().includes(termoBusca) ||
      previsao.serie.toLowerCase().includes(termoBusca) ||
      previsao.previsao.toLowerCase().includes(termoBusca)
    );
  });

  // Ordenar previsões
  const previsoesOrdenadas = [...previsoesFiltradas].sort((a, b) => {
    let valorA = a[ordenacao.campo];
    let valorB = b[ordenacao.campo];

    if (ordenacao.campo === 'dataCriacao') {
      valorA = new Date(valorA);
      valorB = new Date(valorB);
    } else {
      valorA = String(valorA).toLowerCase();
      valorB = String(valorB).toLowerCase();
    }

    if (ordenacao.direcao === 'asc') {
      return valorA > valorB ? 1 : -1;
    } else {
      return valorA < valorB ? 1 : -1;
    }
  });

  const handleOrdenar = (campo) => {
    setOrdenacao(prev => ({
      campo,
      direcao: prev.campo === campo && prev.direcao === 'asc' ? 'desc' : 'asc'
    }));
  };

  const getIconeOrdenacao = (campo) => {
    if (ordenacao.campo !== campo) return '↕️';
    return ordenacao.direcao === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="historico-container">
      <div className="historico-header">
        <h2>Histórico de Previsões</h2>
        <div className="historico-filtro">
          <input
            type="text"
            placeholder="Buscar por referência, task, série temporal ou previsão..."
            value={filtro}
            onChange={(e) => setFiltro(e.target.value)}
            className="filtro-input"
          />
        </div>
      </div>

      <div className="historico-tabela-container">
        <table className="historico-tabela">
          <thead>
            <tr>
              <th 
                onClick={() => handleOrdenar('referencia')}
                className="coluna-ordenavel"
              >
                Referência {getIconeOrdenacao('referencia')}
              </th>
              <th 
                onClick={() => handleOrdenar('task')}
                className="coluna-ordenavel"
              >
                Task {getIconeOrdenacao('task')}
              </th>
              <th 
                onClick={() => handleOrdenar('serie')}
                className="coluna-ordenavel"
              >
                Série {getIconeOrdenacao('serie')}
              </th>
              <th 
                onClick={() => handleOrdenar('previsao')}
                className="coluna-ordenavel"
              >
                Previsão {getIconeOrdenacao('previsao')}
              </th>
              <th 
                onClick={() => handleOrdenar('dataCriacao')}
                className="coluna-ordenavel"
              >
                Data de Criação {getIconeOrdenacao('dataCriacao')}
              </th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {previsoesOrdenadas.length > 0 ? (
              previsoesOrdenadas.map((previsao) => (
                <tr key={previsao.id}>
                  <td className="coluna-referencia">{previsao.referencia}</td>
                  <td className="coluna-task">{previsao.task}</td>
                  <td className="coluna-serie">{previsao.serie}</td>
                  <td className="coluna-previsao">{previsao.previsao}</td>
                  <td className="coluna-data">{previsao.dataCriacao}</td>
                  <td>
                    <span className={`status-badge status-${previsao.status.toLowerCase()}`}>
                      {previsao.status}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="sem-resultados">
                  Nenhuma previsão encontrada
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="historico-footer">
        <p className="total-registros">
          Total: {previsoesOrdenadas.length} {previsoesOrdenadas.length === 1 ? 'previsão' : 'previsões'}
        </p>
      </div>
    </div>
  );
};

export default Historico;

