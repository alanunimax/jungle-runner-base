"""Classe Jogador: personagem controlado pelo usuário."""
import pygame

from src import config
from src.cores import DOURADO, PELE


class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.velocidade_y = 0
        self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = config.FORCA_PULO
            self.no_chao = False

    def mover(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, config.LARGURA_NIVEL - self.rect.width))

    def atualizar(self, chao_y):
        """Aplica gravidade. Retorna True se o jogador caiu na água (chao_y is None)."""
        self.velocidade_y += config.GRAVIDADE
        self.rect.y += int(self.velocidade_y)

        if chao_y is not None:
            if self.rect.bottom >= chao_y:
                self.rect.bottom = chao_y
                self.velocidade_y = 0
                self.no_chao = True
            else:
                self.no_chao = False
            return False

        # Não há chão sob o jogador (vão da ponte / água do lago)
        self.no_chao = False
        return self.rect.bottom >= config.ALTURA

    def desenhar(self, tela, camera_x):
        x = self.rect.x - camera_x
        pygame.draw.rect(tela, DOURADO, (x, self.rect.y, self.rect.width, self.rect.height), border_radius=8)
        pygame.draw.circle(tela, PELE, (x + self.rect.width // 2, self.rect.y - 5), 14)
