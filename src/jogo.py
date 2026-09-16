"""Classe Jogo: orquestra o loop principal, entidades, câmera e regras.

Este módulo é o "maestro" da arquitetura - ele não desenha nem calcula
física por conta própria, apenas chama os métodos das entidades e módulos
certos, na ordem certa. Cada responsabilidade (jogador, obstáculos,
cenário, HUD, áudio) fica isolada em seu próprio arquivo.

Repare que este arquivo trata todo obstáculo da lista `self.obstaculos` de
forma genérica (`obs.atualizar()`, `obs.desenhar(...)`, `obs.perigoso`) -
sem nunca perguntar "isso é um Tronco ou uma Cobra?". Cada objeto sabe se
comportar sozinho. Isso só é possível porque Tronco, Cobra e Fogo herdam
de Obstaculo (ver src/entidades/obstaculos.py).
"""
import sys
import pygame

from src import config
from src import audio
from src.entidades.jogador import Jogador
from src.entidades.obstaculos import Tronco, Cobra, Fogo
from src.entidades.ponte import Ponte, desenhar_lago, chao_em
from src.mundo.cenario import desenhar_fundo
from src.ui.hud import desenhar_hud


class Jogo:
    def __init__(self):
        
        pygame.init()
        
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption(config.TITULO)
        self.relogio = pygame.time.Clock()
        
        audio.iniciar()

        self.jogador = Jogador(100, config.CHAO_Y - 50)
        self.ponte = Ponte(config.LAGO_INICIO, config.LAGO_FIM)

        # Um Tronco, uma Cobra e um Fogo em cada bioma - mesmas classes,
        # contextos diferentes.
        self.obstaculos = [
            
            # Selva (dia)
            Tronco(300),
            Cobra(1150),
            Fogo(1450),
            
            # Selva (noite)
            Tronco(2200),
            Cobra(2500),
            Fogo(2750),
            
            # Neve/montanhas
            Tronco(3400),
            Cobra(3700),
            Fogo(3950),
        ]

        self.vidas = 3
        self.checkpoint_x = 100
        self.camera_x = 0

    def executar(self):
        rodando = True
        while rodando:
            rodando = self._processar_eventos()
            self._atualizar()
            self._desenhar()
            self.relogio.tick(config.FPS)

        pygame.quit()
        sys.exit()

    # -- Entrada -------------------------------------------------------------
    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP):
                if self.jogador.no_chao:
                    audio.tocar_pulo()
                self.jogador.pular()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.jogador.mover(-config.VELOCIDADE_JOGADOR)
        if teclas[pygame.K_RIGHT]:
            self.jogador.mover(config.VELOCIDADE_JOGADOR)
        return True

    # -- Lógica ----------------------------------------------------------------
    def _atualizar(self):
        chao_atual = chao_em(self.jogador.rect.centerx, self.ponte)
        caiu_na_agua = self.jogador.atualizar(chao_atual)

        if caiu_na_agua:
            self._perder_vida()

        # checkpoint: só atualiza em chão firme, fora do lago
        dentro_do_lago = config.LAGO_INICIO <= self.jogador.rect.centerx <= config.LAGO_FIM
        if chao_atual == config.CHAO_Y and not dentro_do_lago:
            self.checkpoint_x = self.jogador.rect.x

        self._checar_colisoes()

        if self.vidas <= 0:
            self._reiniciar()

        self.camera_x = max(0, min(self.jogador.rect.x - config.LARGURA // 3, config.LARGURA_NIVEL - config.LARGURA))

    def _checar_colisoes(self):
        for obs in self.obstaculos:
            obs.atualizar()  # Fogo anima; Tronco/Cobra não fazem nada (herdado da base)
            if not self.jogador.rect.colliderect(obs.rect):
                continue

            if obs.perigoso:
                self._perder_vida(empurrar=True)
            else:
                # Tronco: bloqueia como parede, o jogador precisa pular por cima
                if self.jogador.rect.centerx < obs.rect.centerx:
                    self.jogador.rect.right = obs.rect.left
                else:
                    self.jogador.rect.left = obs.rect.right

    def _perder_vida(self, empurrar=False):
        self.vidas -= 1
        if empurrar:
            self.jogador.rect.x = max(self.checkpoint_x, self.jogador.rect.x - 80)
        else:
            self.jogador.rect.x = self.checkpoint_x
            self.jogador.rect.bottom = config.CHAO_Y
            self.jogador.velocidade_y = 0

    def _reiniciar(self):
        self.vidas = 3
        self.jogador.rect.x = 100
        self.jogador.rect.bottom = config.CHAO_Y
        self.checkpoint_x = 100

    # -- Desenho -------------------------------------------------------------
    def _desenhar(self):
        camera_x = self.camera_x

        tipo_bioma = desenhar_fundo(self.tela, camera_x)
        desenhar_lago(self.tela, camera_x, config.LAGO_INICIO, config.LAGO_FIM)
        self.ponte.desenhar(self.tela, camera_x)

        for obs in self.obstaculos:
            obs.desenhar(self.tela, camera_x)

        self.jogador.desenhar(self.tela, camera_x)
        desenhar_hud(self.tela, self.vidas, tipo_bioma)
        pygame.display.flip()
