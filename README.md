# Jogo de Hex com Q-Learning AI

Este é um jogo de Hex implementado em Python, onde você pode jogar contra uma inteligência artificial (AI) treinada com Q-Learning.

## Sobre o Jogo de Hex

O Hex é um jogo de tabuleiro estratégico para dois jogadores que foi inventado pelos matemáticos dinamarqueses Piet Hein e John Nash independentemente em 1942. O jogo é jogado em um tabuleiro hexagonal, onde cada jogador tem peças de sua cor e o objetivo é conectar as extremidades opostas do tabuleiro com uma cor contínua.

## Visão Geral do Código

- O código implementa o jogo de Hex e uma AI baseada em Q-Learning para jogar contra o jogador humano.
- A classe `HexBoard` representa o tabuleiro do jogo e contém métodos para imprimir o tabuleiro, verificar movimentos válidos e determinar o vencedor.
- A classe `Player` representa os jogadores do jogo.
- A classe `HexQLearningAI` implementa a AI baseada em Q-Learning, com métodos para tomar decisões de movimento, atualizar a tabela Q e calcular as recompensas.
- A função `jogar_hex()` é a função principal que inicia o jogo, permite que o jogador humano faça movimentos e controla a jogada da AI.

## Como Jogar

1. Clone ou faça o download do repositório.
2. Certifique-se de ter o Python instalado em seu sistema.
3. Execute o script Python `hex_game.py`.
4. Siga as instruções no terminal para jogar contra a AI.

## Requisitos

- Python 3.x
- Biblioteca NumPy

## Autor

Este jogo foi criado por Lucas. Sinta-se à vontade para fazer sugestões ou contribuir para o projeto.

Divirta-se jogando Hex!
