"""Cenário de fundo: os três biomas do jogo - Selva (dia), Selva (noite) e Neve.

O bioma é escolhido com base na posição x do centro da câmera no nível,
com interpolação de cores (lerp) nas zonas de transição para um efeito
suave em vez de um corte brusco.
"""
import pygame

from src import config
from src import cores


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_cor(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def obter_cores_bioma(x):
    """Retorna (cor_ceu_topo, cor_ceu_base, cor_chao, tipo_decoracao) para a posição x do mundo."""
    if x < config.SELVA_FIM:
        return cores.VERDE_CEU_CLARO, cores.VERDE_CEU, cores.MARROM_CHAO, "selva"
    elif x < config.TRANSICAO_NOITE_FIM:
        t = (x - config.SELVA_FIM) / (config.TRANSICAO_NOITE_FIM - config.SELVA_FIM)
        topo = lerp_cor(cores.VERDE_CEU_CLARO, cores.NOITE_CEU_TOPO, t)
        base = lerp_cor(cores.VERDE_CEU, cores.NOITE_CEU_BASE, t)
        chao = lerp_cor(cores.MARROM_CHAO, cores.MARROM_CHAO_NOITE, t)
        return topo, base, chao, ("selva_noite" if t > 0.5 else "selva")
    elif x < config.NOITE_FIM:
        return cores.NOITE_CEU_TOPO, cores.NOITE_CEU_BASE, cores.MARROM_CHAO_NOITE, "selva_noite"
    elif x < config.TRANSICAO_NEVE_FIM:
        t = (x - config.NOITE_FIM) / (config.TRANSICAO_NEVE_FIM - config.NOITE_FIM)
        topo = lerp_cor(cores.NOITE_CEU_TOPO, cores.NEVE_CEU_TOPO, t)
        base = lerp_cor(cores.NOITE_CEU_BASE, cores.NEVE_CEU_BASE, t)
        chao = lerp_cor(cores.MARROM_CHAO_NOITE, cores.BRANCO_NEVE, t)
        return topo, base, chao, ("neve" if t > 0.5 else "selva_noite")
    else:
        return cores.NEVE_CEU_TOPO, cores.NEVE_CEU_BASE, cores.BRANCO_NEVE, "neve"


def desenhar_fundo(tela, camera_x):
    centro_mundo = camera_x + config.LARGURA // 2
    ceu_topo, ceu_base, chao_cor, tipo = obter_cores_bioma(centro_mundo)

    tela.fill(ceu_base)
    pygame.draw.rect(tela, ceu_topo, (0, 0, config.LARGURA, config.CHAO_Y - 100))

    if tipo == "selva":
        _desenhar_arvores(tela, camera_x, tronco_cor=cores.MARROM_TRONCO, folha_cor=cores.VERDE_FOLHA)
    elif tipo == "selva_noite":
        _desenhar_ceu_noturno(tela, camera_x)
        _desenhar_arvores(tela, camera_x, tronco_cor=(40, 30, 25), folha_cor=cores.VERDE_ESCURO)
    else:
        _desenhar_montanhas(tela, camera_x)
        _desenhar_pinheiros(tela, camera_x)

    pygame.draw.rect(tela, chao_cor, (0, config.CHAO_Y, config.LARGURA, config.ALTURA - config.CHAO_Y))
    return tipo


def _desenhar_arvores(tela, camera_x, tronco_cor, folha_cor):
    for i in range(10):
        arv_x = (i * 250 - camera_x // 2) % (config.LARGURA + 200) - 100
        pygame.draw.rect(tela, tronco_cor, (arv_x, config.CHAO_Y - 160, 15, 100))
        pygame.draw.circle(tela, folha_cor, (arv_x + 7, config.CHAO_Y - 170), 45)


def _desenhar_ceu_noturno(tela, camera_x):
    lua_x = int(config.LARGURA * 0.85)
    lua_y = int(config.ALTURA * 0.17)
    pygame.draw.circle(tela, (240, 240, 220), (lua_x, lua_y), 35)  # lua
    for i in range(25):
        ex = (i * 97 - camera_x // 3) % config.LARGURA
        ey = (i * 53) % (config.CHAO_Y - 120)
        pygame.draw.circle(tela, cores.BRANCO, (ex, ey), 1)


def _desenhar_montanhas(tela, camera_x):
    for i in range(6):
        mx = (i * 220 - camera_x // 3) % (config.LARGURA + 300) - 150
        pygame.draw.polygon(tela, (176, 190, 197),
                             [(mx, config.CHAO_Y - 100), (mx + 90, config.CHAO_Y - 250), (mx + 180, config.CHAO_Y - 100)])
        pygame.draw.polygon(tela, cores.BRANCO,
                             [(mx + 55, config.CHAO_Y - 210), (mx + 90, config.CHAO_Y - 250), (mx + 125, config.CHAO_Y - 210)])


def _desenhar_pinheiros(tela, camera_x):
    for i in range(8):
        arv_x = (i * 220 - camera_x // 2) % (config.LARGURA + 200) - 100
        pygame.draw.polygon(tela, (20, 70, 50),
                             [(arv_x, config.CHAO_Y - 40), (arv_x + 20, config.CHAO_Y - 110), (arv_x + 40, config.CHAO_Y - 40)])
