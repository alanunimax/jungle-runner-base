"""Áudio do jogo - versão simplificada, com apenas o som de pulo.

Isolar o áudio em seu próprio módulo significa que o resto do código
(Jogador, Jogo) só chama audio.tocar_pulo() e não precisa saber onde o
arquivo está nem como o pygame.mixer funciona.

Se o dispositivo de áudio não estiver disponível (ex.: computador sem
placa de som), o jogo continua funcionando normalmente, apenas sem som.
"""
import os
import pygame

_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PASTA_SONS = os.path.join(_RAIZ_PROJETO, "assets", "sounds")

_som_pulo = None
_ativo = False


def iniciar():
    """Inicializa o mixer e carrega o som. Chamar depois de pygame.init()."""
    global _ativo, _som_pulo
    try:
        pygame.mixer.init()
        caminho = os.path.join(_PASTA_SONS, "pulo.ogg")
        if os.path.exists(caminho):
            _som_pulo = pygame.mixer.Sound(caminho)
        _ativo = True
    except pygame.error:
        # Sem dispositivo de áudio disponível - o jogo segue sem som.
        _ativo = False


def tocar_pulo():
    if _ativo and _som_pulo is not None:
        _som_pulo.play()
