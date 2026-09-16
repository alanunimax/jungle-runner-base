"""Obstáculos do jogo: aqui mora a herança e o polimorfismo.

    Obstaculo                <- classe base (mãe)
        |
        +-- Tronco            <- bloqueia como parede, o jogador precisa pular
        +-- Cobra             <- perigosa, tira vida se tocar
        +-- Fogo               <- perigosa, tira vida e tem animação própria

As três subclasses HERDAM de Obstaculo (reaproveitam __init__ e o atributo
`perigoso`) e cada uma sobrescreve desenhar() com seu próprio visual -
isso é POLIMORFISMO: o resto do jogo (veja Jogo._checar_colisoes em
jogo.py) chama `obstaculo.desenhar(...)` sem precisar saber qual subclasse
é cada obstáculo da lista; cada um desenha a si mesmo do seu jeito.
"""
import pygame

from src import config
from src.cores import MARROM_TRONCO, VERDE_ESCURO


class Obstaculo:
    """Classe base (mãe) para todos os obstáculos do jogo."""

    def __init__(self, x, largura, altura, perigoso):
        self.rect = pygame.Rect(x, config.CHAO_Y - altura, largura, altura)
        # perigoso=True  -> tira vida do jogador (Cobra, Fogo)
        # perigoso=False -> bloqueia como parede, só precisa pular (Tronco)
        self.perigoso = perigoso

    def atualizar(self):
        """Não faz nada por padrão - Fogo sobrescreve isso para animar."""
        pass

    def desenhar(self, tela, camera_x):
        raise NotImplementedError("Cada subclasse deve implementar seu próprio desenho")


class Tronco(Obstaculo):
    """Obstáculo parado, não-perigoso: funciona como uma parede a ser pulada."""

    def __init__(self, x):
        super().__init__(x, largura=30, altura=35, perigoso=False)

    def desenhar(self, tela, camera_x):
        x = self.rect.x - camera_x
        pygame.draw.rect(tela, MARROM_TRONCO, (x, self.rect.y, self.rect.width, self.rect.height))
        pygame.draw.ellipse(tela, VERDE_ESCURO, (x - 10, self.rect.y - 15, 50, 20))


class Cobra(Obstaculo):
    """Obstáculo baixo e perigoso: tira vida do jogador ao tocar."""

    def __init__(self, x):
        super().__init__(x, largura=45, altura=18, perigoso=True)

    def desenhar(self, tela, camera_x):
        x = self.rect.x - camera_x
        y = self.rect.y
        pygame.draw.ellipse(tela, (60, 140, 60), (x, y, self.rect.width, self.rect.height))
        for i in range(3):
            cy = y + (3 if i % 2 == 0 else 11)
            pygame.draw.circle(tela, (30, 90, 30), (x + 8 + i * 14, cy), 5)
        pygame.draw.circle(tela, (0, 0, 0), (x + self.rect.width - 6, y + 5), 2)


class Fogo(Obstaculo):
    """Obstáculo perigoso com animação própria - por isso sobrescreve atualizar()."""

    def __init__(self, x):
        super().__init__(x, largura=26, altura=40, perigoso=True)
        self.contador = 0

    def atualizar(self):
        self.contador += 1  # anima o flamejar

    def desenhar(self, tela, camera_x):
        x = self.rect.x - camera_x
        oscilacao = 5 if (self.contador // 8) % 2 == 0 else 0
        pygame.draw.ellipse(tela, (80, 40, 20), (x, self.rect.bottom - 10, self.rect.width, 10))
        pygame.draw.polygon(tela, (255, 100, 0), [
            (x, self.rect.bottom),
            (x + self.rect.width // 2, self.rect.top - oscilacao),
            (x + self.rect.width, self.rect.bottom),
        ])
        pygame.draw.polygon(tela, (255, 200, 0), [
            (x + 6, self.rect.bottom),
            (x + self.rect.width // 2, self.rect.top + 10 - oscilacao),
            (x + self.rect.width - 6, self.rect.bottom),
        ])
