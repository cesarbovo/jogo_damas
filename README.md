# 🏆 Damas com IA Avançada em Python

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-concluido-success)

Uma implementação profissional do jogo de Damas (Regras Brasileiras/Internacionais 64 casas) desenvolvida em Python puro. O projeto conta com uma Engine de regras rigorosa, uma Interface Gráfica (GUI) responsiva e uma Inteligência Artificial baseada em algoritmos de busca competitiva.

---

## ✨ Funcionalidades Principais

### 🧠 Inteligência Artificial (Minimax)
- **Algoritmo Minimax:** Implementado com **Poda Alpha-Beta** para otimização de performance.
- **Busca de Quiescência (Quiescence Search):** Evita o "Efeito Horizonte" em trocas complexas de peças, permitindo que a IA continue calculando capturas além da profundidade limite.
- **Heurística Posicional:** Utiliza "mapas de calor" (Heatmaps) para valorizar o domínio do centro e proteção da base.
- **Avaliação Dinâmica:** Diferencia pesos para Pedras, Damas, Mobilidade e Defesa.

### 📜 Motor de Regras (Rigorous Engine)
- **Lei da Maioria:** Implementação estrita da regra que obriga o jogador a escolher o movimento que captura o maior número de peças.
- **Captura Obrigatória:** O sistema valida e força capturas quando disponíveis.
- **Dama Voadora:** Suporte completo para movimentos de damas a longa distância e pouso em qualquer casa livre subsequente.
- **Captura para Trás:** Pedras andam para frente, mas capturam em ambas as direções.

### 🖥️ Interface Gráfica (GUI)
- Desenvolvida com **Tkinter** (Nativo do Python).
- Destaque visual para movimentos possíveis e últimas jogadas.
- Sistema de menus (Novo Jogo, Sair).
- Feedback de status em tempo real.

---

## 📷 Screenshots

| Tabuleiro Inicial | Sugestão de Movimento |
|:---:|:---:|
| *(Insira uma imagem do tabuleiro aqui)* | *(Insira uma imagem de uma jogada aqui)* |

---

## 🚀 Instalação e Execução

Este projeto utiliza apenas a **Biblioteca Padrão do Python**. Não é necessário instalar dependências externas (como numpy ou pygame).

### Pré-requisitos
- Python 3.x instalado.
- (Apenas Linux) Certifique-se de ter o `tkinter` instalado: `sudo apt-get install python3-tk`

### Passos
1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/damas-python-ai.git](https://github.com/seu-usuario/damas-python-ai.git)
   cd damas-python-ai
