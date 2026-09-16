# Selva Runner - Exemplo Simples

Versão enxuta do jogo, feita para apresentar em aula dois assuntos:
**arquitetura em arquivos separados** e **herança/polimorfismo em POO**.

## Como executar

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Controles:** ← → move o personagem · ESPAÇO (ou ↑) pula.

## O que tem neste exemplo

- 3 biomas (Selva de dia, Selva à noite, Neve) com transição suave de cores.
- 3 obstáculos - Tronco, Cobra, Fogo - todos filhos de uma classe `Obstaculo`.
- Um lago estilo Pitfall, atravessado por uma ponte com tábuas e vãos.
- Um único som: o pulo do personagem.

*(Não tem pontuação, coletáveis, macaco, vinha ou decorações extras -
foram removidos de propósito para deixar o código mais enxuto e fácil de
seguir em aula.)*

## Arquitetura do projeto

```
selva_runner_simples/
├── main.py                    # ponto de entrada - só cria e roda a Jogo
├── requirements.txt
├── assets/
│   └── sounds/
│       └── pulo.ogg            # único efeito sonoro do jogo
└── src/
    ├── config.py               # constantes: janela, física, biomas
    ├── cores.py                 # paleta de cores
    ├── jogo.py                  # classe Jogo: orquestra o loop principal
    ├── audio.py                 # carrega e toca o som de pulo
    ├── entidades/
    │   ├── jogador.py             # classe Jogador
    │   ├── obstaculos.py          # Obstaculo (base) + Tronco, Cobra, Fogo
    │   └── ponte.py                # Ponte + lago
    ├── mundo/
    │   └── cenario.py             # fundo e transição entre os 3 biomas
    └── ui/
        └── hud.py                  # vidas e nome do bioma na tela
```

### Como os arquivos se relacionam

`main.py` cria um objeto `Jogo` (definido em `src/jogo.py`) e chama
`executar()`. A classe `Jogo` é o "maestro": ela importa e guarda uma
instância de cada coisa que existe no jogo -

```python
from src.entidades.jogador import Jogador
from src.entidades.obstaculos import Tronco, Cobra, Fogo
from src.entidades.ponte import Ponte, desenhar_lago, chao_em
from src.mundo.cenario import desenhar_fundo
from src.ui.hud import desenhar_hud
```

- e a cada quadro (60 vezes por segundo) chama, na ordem certa:
  `_processar_eventos()` → `_atualizar()` → `_desenhar()`.

Nenhum desses módulos sabe da existência dos outros além do que precisa.
`obstaculos.py` não sabe que existe uma `Ponte`; `cenario.py` não sabe que
existe um `Jogador`. Quem conecta tudo é só o `jogo.py`.

## Herança e polimorfismo (o assunto principal)

Abra `src/entidades/obstaculos.py`. A estrutura é:

```
Obstaculo                <- classe base ("mãe")
    |
    +-- Tronco             <- bloqueia como parede
    +-- Cobra               <- perigosa, tira vida
    +-- Fogo                  <- perigosa, tira vida, tem animação própria
```

**Herança:** `Tronco`, `Cobra` e `Fogo` começam com
`class Tronco(Obstaculo):` - isso significa "todo Tronco também é um
Obstaculo". As três reaproveitam o `__init__` da classe base via
`super().__init__(...)`, então não precisam reescrever a lógica de criar
o `rect` nem guardar o atributo `perigoso`.

**Polimorfismo:** cada subclasse sobrescreve `desenhar()` com sua própria
aparência (um tronco marrom, uma cobra verde ondulada, uma fogueira
animada). O `Fogo` também sobrescreve `atualizar()`, porque precisa de um
contador de quadros para animar o flamejar - `Tronco` e `Cobra` não
precisam, então simplesmente herdam o `atualizar()` vazio da classe base.

A prova de que isso funciona está em `src/jogo.py`, no método
`_checar_colisoes`:

```python
for obs in self.obstaculos:
    obs.atualizar()
    ...
    if obs.perigoso:
        ...
    else:
        ...
```

Repare que esse laço passa por **todos** os obstáculos - trocos, cobras e
fogos misturados na mesma lista - e chama `obs.atualizar()` e depois
`obs.desenhar(...)` (lá no método `_desenhar`) sem nunca perguntar "que
tipo de obstáculo é esse?". Cada objeto já sabe se animar e se desenhar
sozinho, do jeito que sua própria classe definiu. Isso é o valor prático
do polimorfismo: o código que *usa* os obstáculos fica simples, mesmo
com vários tipos diferentes misturados.

**Pra exercitar em aula:** um bom desafio para os alunos é criar uma nova
subclasse de `Obstaculo` (por exemplo, uma `Pedra`) sem precisar tocar em
`jogo.py` - só criar a classe em `obstaculos.py` e adicionar uma instância
na lista `self.obstaculos`. Se funcionar sem mexer no resto, é a prova de
que a arquitetura está bem separada.
