import pygame
import math
import os
from random import randint


# Inicialização do pygame
pygame.init()
FPS = 120
CLOCK = pygame.time.Clock()

# Criar a tela
TELA = pygame.display.set_mode((800, 600))

# FUNDO
FUNDO = pygame.image.load(os.path.join("assets", "background.png"))

# Título e Ícone
pygame.display.set_caption("Invasores do Espaço")
ICONE = pygame.image.load(os.path.join("assets", "ufo.png"))
pygame.display.set_icon(ICONE)

# Pontuação
valor_pontuacao = 0
boss = 5
FONTE = pygame.font.Font("freesansbold.ttf", 32)
POS_X_PONTUACAO = 10
POS_Y_PONTUACAO = 10

def mostrar_pontuacao(x, y):
    pontuacao = FONTE.render("Pontuação: " + str(valor_pontuacao), True, (255, 255, 255))
    TELA.blit(pontuacao, (x, y))

# Fim do jogo
FONTE_GAME_OVER = pygame.font.Font("freesansbold.ttf", 64)

def texto_fim_do_jogo():
    fim_do_jogo = FONTE_GAME_OVER.render("FIM DO JOGO", True, (255, 255, 255))

    TELA.blit(fim_do_jogo, (200, 250))

# vitória do game
FONTE_VICTORY = pygame.font.Font("freesansbold.ttf", 64)

def text_victory():
    victory = FONTE_VICTORY.render('VITÓRIA', True, (255, 255, 255))
    TELA.blit(victory, (255, 250))

# Jogador
imagem_jogador = pygame.image.load(os.path.join("assets", "spaceship.png"))
jogadorX = 370
jogadorY = 480
alteracao_jogadorX = 0

def jogador(x, y):
    TELA.blit(imagem_jogador, (x, y))

# Alienígenas
imagem_alienigena = []
alienigenaX = []
alienigenaY = []
alteracao_alienigenaX = []
alteracao_alienigenaY = []
abaixar_alienigena = []
num_alienigenas = 6



for i in range(num_alienigenas):
    imagem_alienigena.append(pygame.image.load("assets\\alien.png"))
    alienigenaX.append(randint(0, 735))
    alienigenaY.append(randint(50, 150))
    alteracao_alienigenaX.append(1)
    alteracao_alienigenaY.append(40)
    abaixar_alienigena.append(False)

def alienigena(x, y):
    TELA.blit(imagem_alienigena[i], (x, y))

# Tiro
imagem_tiro = pygame.image.load("assets\\bullet.png")
tiroX = 0
tiroY = 480
alteracao_tiroX = 0
alteracao_tiroY = 5
estado_tiro = "pronto"

def atirar(x, y):

    global estado_tiro
    estado_tiro = "atirar"
    TELA.blit(imagem_tiro, (x + 16, y + 10))

def colisao(alienigenaX, alienigenaY, tiroX, tiroY):

    distancia = math.sqrt(
        (math.pow(alienigenaX - tiroX, 2)) + (math.pow(alienigenaY - tiroY, 2))
    )
    if distancia < 27:
        return True
    return False


# BOSS:
alien_especial_img = pygame.image.load("assets\\alien.png")
alien_especial_X = randint(0, 735)
alien_especial_Y = randint(50, 150)
alien_especial_X_change = 3
alien_especial_Y_change = 50
alien_especial_dead = False
alien_especial_vidas = 3  # Número de vidas do alienígena especial
chefe_final_vivo = True
alien_especial_invocado = "no"

# O programa
executando = True
tela_inicio = True
tela_replay = False

while tela_inicio:
    TELA.fill((0, 0, 0))
    TELA.blit(FUNDO, (0, 0))
    texto_inicio = FONTE.render("Pressione CAPS LOCK para começar", True, (255, 255, 255))
    TELA.blit(texto_inicio, (110, 275))
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_CAPSLOCK:
            tela_inicio = False

while executando:

    while tela_replay:
        TELA.fill((0, 0, 0))
        TELA.blit(FUNDO, (0, 0))
        texto_replay = FONTE.render("Você Perdeu. Tente novamente em CAPS LOCK", True, (255, 255, 255))
        TELA.blit(texto_replay, (10, 275))
        alien_especial_vidas = 3
        valor_pontuacao = 0
        num_alienigenas = 6
        FPS = 120
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_CAPSLOCK:
                tela_replay = False

    # Relógio
    CLOCK.tick(FPS)

    # RGB
    TELA.fill((0, 0, 0))

    # FUNDO
    TELA.blit(FUNDO, (0, 0))

    # Verificar se não saiu
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # invocando BOSS
    if valor_pontuacao >= 2:
        alien_especial_invocado = "yes"
        num_alienigenas = 0  # Remover os inimigos normais
    else:
        alien_especial_invocado = "no"


    # invocar BOSS:
    if chefe_final_vivo == True:
        if not alien_especial_dead and alien_especial_invocado == "yes":
            alien_especial_X += alien_especial_X_change

            if alien_especial_Y > 430: # jm: verifica se o BOSS ja atingiu a altura max.
                alien_especial_Y = 0
                tela_replay = True
            
            if alien_especial_X > 736:
                alien_especial_X_change *= -1
                alien_especial_X = 736
                alien_especial_Y += alien_especial_Y_change
            elif alien_especial_X < 0:
                alien_especial_X_change *= -1
                alien_especial_X = 0
                alien_especial_Y += alien_especial_Y_change

            # Colisão com o tiro
            colisao_alien_especial = colisao(alien_especial_X, alien_especial_Y, tiroX, tiroY)
            if colisao_alien_especial:
                tiroY = 480
                estado_tiro = "pronto"
                alien_especial_vidas -= 1
                alien_especial_Y -= 30

                if alien_especial_vidas == 0:
                    alien_especial_dead = True
                    chefe_final_vivo = False
                    valor_pontuacao += 5  # Ajuste a pontuação conforme desejado
                    # Defina a posição fora da tela para remover o alienígena especial
                    alien_especial_X = -100
                    alien_especial_Y = -100
            alienigena(alien_especial_X, alien_especial_Y)

    if alien_especial_dead:
        text_victory()

    # Gerar inimigos
    if num_alienigenas != 0:
        for i in range(num_alienigenas):
            # Fim do Jogo
            if alienigenaY[i] > 430: #jm: verifica se um alien ja atingiu a altura max.
                for j in range(num_alienigenas): #jm: joga os inimigos pra fora do mapa já que o game acabou.
                    alienigenaY[j] = 9999
                texto_fim_do_jogo()
                break

            # jm: soma a posição horizontal a cada atualização
            alienigenaX[i] += alteracao_alienigenaX[i]

            # jm: essa função e a debaixo apenas verificam se chegou ao limite da tela e retorna o boneco de posição
            if alienigenaX[i] > 736:
                alteracao_alienigenaX[i] *= -1
                alienigenaX[i] = 736
                alienigenaY[i] += alteracao_alienigenaY[i]
            elif alienigenaX[i] < 0:
                alteracao_alienigenaX[i] *= -1
                alienigenaX[i] = 0
                alienigenaY[i] += alteracao_alienigenaY[i]

            # Colisão
            colisao_alienigena = colisao(alienigenaX[i], alienigenaY[i], tiroX, tiroY)

            if colisao_alienigena:
                tiroY = 480
                estado_tiro = "pronto"
                alienigenaX[i] = randint(0, 735)
                alienigenaY[i] = randint(50, 150)
                valor_pontuacao += 1 


                # ONDE JM MODIFICOU: 
                if valor_pontuacao == 1:
                    num_alienigenas = 15  # Aumentar o número de inimigos
                    for j in range(num_alienigenas):
                        imagem_alienigena.append(pygame.image.load("assets\\alien.png"))
                        alienigenaX.append(randint(0, 735))
                        alienigenaY.append(randint(50, 150))
                        alteracao_alienigenaX.append(1)
                        alteracao_alienigenaY.append(40)
                        abaixar_alienigena.append(False)
                    FPS = 180
                elif valor_pontuacao == 0:
                    FPS = 120

            alienigena(alienigenaX[i], alienigenaY[i])

        
    # Jogador
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_LEFT:
            alteracao_jogadorX = -2
        if evento.key == pygame.K_RIGHT:
            alteracao_jogadorX = 2
        if evento.key == pygame.K_UP and estado_tiro == "pronto":
            tiroX = jogadorX
            atirar(tiroX, tiroY)

    if evento.type == pygame.K_UP:
        if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
            alteracao_jogadorX = 1
    jogadorX += alteracao_jogadorX

    if jogadorX <= 10 or jogadorX >= 726:
        alteracao_jogadorX *= -1

    # Movimento do Tiro
    if tiroY <= 0:
        tiroY = 480
        estado_tiro = "pronto"

    if estado_tiro == "atirar":
        atirar(tiroX, tiroY)
        tiroY -= alteracao_tiroY

    jogador(jogadorX, jogadorY)
    mostrar_pontuacao(POS_X_PONTUACAO, POS_Y_PONTUACAO)
    pygame.display.update()
