"""Lago e ponte suspensa estilo Pitfall."""
import pygame

from src import config
from src.cores import AZUL_LAGO, AZUL_LAGO_CLARO, MARROM_TABUA, CORDA


class Ponte:
    """Ponte com tábuas separadas por vãos - o jogador precisa pular os vãos."""

    def __init__(self, inicio, fim, largura_tabua=50, largura_vao=50):
        self.tabuas = []
        x = inicio
        while x < fim:
            self.tabuas.append((x, x + largura_tabua))
            x += largura_tabua + largura_vao

    def esta_sobre_tabua(self, x):
        return any(ini <= x <= fim for ini, fim in self.tabuas)

    def desenhar(self, tela, camera_x):
        for ini, fim in self.tabuas:
            x = ini - camera_x
            largura = fim - ini
            pygame.draw.line(tela, CORDA, (x, config.CHAO_Y - 8), (x, config.CHAO_Y - 25), 2)
            pygame.draw.line(tela, CORDA, (x + largura, config.CHAO_Y - 8), (x + largura, config.CHAO_Y - 25), 2)
            pygame.draw.rect(tela, MARROM_TABUA, (x, config.CHAO_Y - 8, largura, 12))


def desenhar_lago(tela, camera_x, inicio, fim):
    x0 = inicio - camera_x
    x1 = fim - camera_x
    pygame.draw.rect(tela, AZUL_LAGO, (x0, config.CHAO_Y, x1 - x0, config.ALTURA - config.CHAO_Y))
    for i in range(int(x0), int(x1), 20):
        pygame.draw.line(tela, AZUL_LAGO_CLARO, (i, config.CHAO_Y + 12), (i + 10, config.CHAO_Y + 12), 2)


def chao_em(x, ponte):
    """Retorna a altura do chão na posição x, ou None se for água (sem chão)."""
    if config.LAGO_INICIO <= x <= config.LAGO_FIM:
        return config.CHAO_Y if ponte.esta_sobre_tabua(x) else None
    return config.CHAO_Y
