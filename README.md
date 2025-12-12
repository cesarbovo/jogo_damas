# 🏆 Damas com IA Avançada em Python

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-concluido-success)

Uma implementação profissional do jogo de Damas (Regras Brasileiras/Internacionais em tabuleiro 8x8) desenvolvida inteiramente em Python. O projeto conta com uma Engine de validação rigorosa de regras, uma Interface Gráfica (GUI) nativa e uma Inteligência Artificial competitiva baseada em algoritmos de busca.

---

## ✨ Funcionalidades Principais

### 🧠 Inteligência Artificial (Minimax)
* **Algoritmo Minimax:** Otimizado com **Poda Alpha-Beta** para máxima eficiência na tomada de decisão.
* **Busca de Quiescência (Quiescence Search):** Resolve o "Efeito Horizonte", permitindo que a IA continue calculando trocas de capturas além da profundidade limite para evitar jogadas suicidas.
* **Heurística Posicional:** Utiliza "mapas de calor" (Heatmaps) para valorizar o controle do centro do tabuleiro e a segurança das bordas.
* **Avaliação Dinâmica:** Pesos diferenciados para Pedras, Damas, Mobilidade e proteção da primeira linha (Defesa de Base).

### 📜 Motor de Regras (Rigorous Engine)
* **Lei da Maioria:** Implementação estrita da regra oficial que **obriga** o jogador a escolher a jogada que captura o maior número de peças disponível.
* **Captura Obrigatória:** O sistema valida e força a captura sempre que possível.
* **Dama Voadora:** Suporte completo para movimentos de damas a longa distância e pouso em qualquer casa livre após a peça capturada.
* **Captura Bidirecional:** Pedras andam apenas para frente, mas podem capturar tanto para frente quanto para trás.

### 🖥️ Interface Gráfica (GUI)
* Desenvolvida com **Tkinter** (Biblioteca nativa do Python, sem dependências pesadas).
* Visualização clara de movimentos válidos (destaque em verde).
* Menu de opções (Jogar Novamente, Sair).
* Feedback de status em tempo real (Turno do Jogador vs IA Pensando).

---

## 📷 Screenshots

| Tabuleiro Inicial | Destaque de Movimento |
|:---:|:---:|
| <img width="518" height="616" alt="image" src="https://github.com/user-attachments/assets/19150d21-9a34-42d2-a5f3-3f381dec57eb" /> | <img width="518" height="616" alt="image" src="https://github.com/user-attachments/assets/306b2169-d5cd-4f80-8b9f-bae3aafa0000" /> |

---

## 🚀 Instalação e Execução

Este projeto foi desenhado para ser leve e portátil. Ele utiliza **apenas a Biblioteca Padrão do Python**. Não é necessário instalar pacotes externos via `pip` (como numpy ou pygame).

### Pré-requisitos
* Python 3.8 ou superior instalado.
* **(Apenas Linux):** Em algumas distros, o Tkinter deve ser instalado separadamente:
    ```bash
    sudo apt-get install python3-tk
    ```

### Como Rodar
1.  Clone o repositório:
    ```bash
    git clone [https://github.com/cesarbovo/damas-python-ai.git](https://github.com/cesarbovo/damas-python-ai.git)
    cd damas-python-ai
    ```

2.  Execute o jogo:
    ```bash
    python app.py
    ```

---

## 📂 Estrutura do Projeto

O código segue princípios de *Clean Code* e separação de responsabilidades (MVC - Model View Controller adaptado):

```text
.
├── app.py           # Entry Point & Interface Gráfica (View/Controller)
├── regras.py        # Motor de Regras e Lógica do Tabuleiro (Model/Truth Source)
├── ia.py            # Lógica da Inteligência Artificial (AI Service)
├── requirements.txt # Documentação de dependências (Vazio/Informativo)
└── README.md        # Documentação do projeto

---

## 🎓 Visualizador Educativo (Minimax Debugger)

Localizado em visualizador_educativo.py, este módulo atua como uma ferramenta pedagógica interativa para desmistificar o funcionamento da Inteligência Artificial. Ao contrário do jogo principal, esta interface oferece um "Raio-X" do processo de decisão do algoritmo:

* **Acompanhamento de Código em Tempo Real:** Exibe o pseudocódigo do algoritmo Minimax e destaca visualmente a linha exata que está sendo executada a cada passo.

* **Monitoramento de Variáveis:** Um painel lateral exibe os valores dinâmicos de Alpha, Beta, Profundidade e a Avaliação atual da árvore de busca.

* **Tabuleiro Fantasma (Ghost Board):** Renderiza graficamente as simulações hipotéticas e movimentos futuros que a IA está calculando antes de tomar a decisão final.

* **Controle de Execução:** Permite ao usuário ajustar a velocidade do raciocínio e a profundidade da IA dinamicamente através de sliders.

---

## 🎓 Sobre o Projeto

Este projeto foi desenvolvido como **Trabalho Final da disciplina de Introdução à Inteligência Artificial**.

**👥 Autores (2º Ciclo):**
* César Augusto Oliveira Bovo
* Elisa Almeida Alcântara
* Guilherme Peres Romanzotti