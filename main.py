"""
Selva Runner Base - Exemplo Simples
UniFAJ/UniMAX - Projeto Prático Integrado (POO + Desenvolvimento de Aplicativos)

Versão enxuta, feita para explicar em aula:
- Herança e polimorfismo (Obstaculo -> Tronco, Cobra, Fogo)
- Arquitetura separada em arquivos (cada um com uma responsabilidade)

Para executar:
    python main.py

Controles: SETAS ESQUERDA/DIREITA move, ESPAÇO (ou seta CIMA) pula.
"""
from src.jogo import Jogo

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
