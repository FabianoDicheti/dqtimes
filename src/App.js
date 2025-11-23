import React from 'react';
import './App.css';
import Historico from './components/Historico/Historico';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>DQTimes</h1>
        <p>Sistema de Previsão de Séries Temporais</p>
      </header>
      <main className="App-main">
        <Historico />
      </main>
    </div>
  );
}

export default App;

