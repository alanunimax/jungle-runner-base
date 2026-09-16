"""HUD: vidas do jogador e nome do bioma atual.

A fonte é criada de forma preguiçosa (lazy) na primeira chamada, pois
pygame.font só pode ser inicializado depois de pygame.init().
"""
import pygame

from src import config
from src.cores import BRANCO

_fonte = None

NOMES_BIOMA = {
    "selva": "Selva (Dia)",
    "selva_noite": "Selva (Noite)",
    "neve": "Montanhas de Neve",
}


def _obter_fonte():
    global _fonte
    if _fonte is None:
        _fonte = pygame.font.SysFont("Arial", 22, bold=True)
    return _fonte


def desenhar_hud(tela, vidas, tipo_bioma):
    for i in range(3):
        cor = (220, 50, 50) if i < vidas else (80, 80, 80)
        pygame.draw.circle(tela, cor, (25 + i * 30, 25), 10)

    fonte = _obter_fonte()
    texto = fonte.render(NOMES_BIOMA.get(tipo_bioma, ""), True, BRANCO)
    tela.blit(texto, (config.LARGURA - texto.get_width() - 15, 15))
