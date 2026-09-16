"""Configurações gerais do jogo: janela, física, nível e biomas.

Manter essas constantes centralizadas facilita ajustar o jogo (tamanho da
janela, gravidade, onde cada bioma começa/termina) sem precisar caçar
números espalhados pelo código.
"""

# Janela
LARGURA = 1000
ALTURA = 500
FPS = 60
TITULO = "Selva Runner - Exemplo Simples (UniFAJ/UniMAX)"

# Chão e física
CHAO_Y = 400  # 80% da altura da janela
GRAVIDADE = 0.8
VELOCIDADE_JOGADOR = 5
FORCA_PULO = -15

# Tamanho total do nível (o jogador percorre da esquerda para a direita)
LARGURA_NIVEL = 4200

# Lago / ponte suspensa (estilo Pitfall)
LAGO_INICIO = 600
LAGO_FIM = 950

# Limites (em x do mundo) de cada bioma. Entre um bioma "puro" e o próximo
# existe uma faixa de transição onde as cores se misturam gradualmente.
SELVA_FIM = 1700            # 0 .. SELVA_FIM             = selva de dia
TRANSICAO_NOITE_FIM = 2000  # .. aqui                    = transição p/ noite
NOITE_FIM = 2900            # .. aqui                    = selva à noite
TRANSICAO_NEVE_FIM = 3200   # .. aqui                    = transição p/ neve
# daqui até LARGURA_NIVEL                                = neve/montanhas
