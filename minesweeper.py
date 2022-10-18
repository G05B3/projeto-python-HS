import random as r
from colorama import Fore, Back, Style

CHANCE = 10

# Definir que cores usar para os vários nºs de adjacências

def color(val):
    if val == 2:  # 0
        return Fore.WHITE
    elif val == 3:  # 1
        return Fore.BLUE
    elif val == 4:  # 2
        return Fore.GREEN
    elif val == 5:  # 3
        return Fore.RED
    elif val == 6:  # 4
        return Fore.CYAN
    elif val == 7:  # 5
        return Fore.MAGENTA
    elif val == 8:  # 6
        return Fore.LIGHTCYAN_EX
    elif val == 9:  # 7
        return Fore.LIGHTRED_EX
    elif val == 10:  # 8
        return Fore.YELLOW

def print_field():
    for i in range(M_WIDTH):
        for j in range(M_HEIGHT):
            if field.m[i][j] == 0 or field.m[i][j] == 1:
                print('x ', end=" ")
            elif field.m[i][j] == "Bomb":
                print('B  ', end="")
            elif field.m[i][j] >= 2:
                print(color(field.m[i][j])+str(field.m[i]
                      [j]-2) + " "+Style.RESET_ALL, end=" ")
        print()


class Field():
    def __init__(self, width, height, chance):
        self.m = []
        self.countdown = width * height #se chegar a 0 o jogador ganha
        # Generate Minesweeper Field (0 = safe, 1 = mine)
        for i in range(width):
            field_line = []
            for j in range(height):
                if chance == -1:
                    f_val = 0
                else:
                    f_val = r.randint(0, chance)
                    if f_val == chance:
                        f_val = 1
                        self.countdown-=1 #retirar do countdown o número de células correspondente às bombas
                    else:
                        f_val = 0
                field_line.append(f_val)
            self.m.append(field_line)

print("Choose the mine field's size (L x C):")
print("L = ", end = "")
M_WIDTH = int(input())
print("W = ", end = "")
M_HEIGHT = int(input())
field = Field(M_WIDTH, M_HEIGHT, CHANCE)
adjm = Field(M_WIDTH, M_HEIGHT, -1)

# Cria Matriz de Adjacências (nº de adjacências a bombas)
for i in range(M_WIDTH):
    for j in range(M_HEIGHT):
        if field.m[i][j] == 1:
            adjm.m[i][j] = "Bomb"
        else:
            adj_counter = 2  # offset of 2 to differentiate from 0 and 1
            # Procura bombas num espaço 3x3 centrado na célula em estudo
            for k in range(max(0, i-1), min(M_HEIGHT, i+2)):
                for l in range(max(0, j-1), min(M_WIDTH, j+2)):
                    if field.m[k][l] == 1:
                        adj_counter += 1
            adjm.m[i][j] = adj_counter


def print_adjm():
    for i in range(M_WIDTH):
        for j in range(M_HEIGHT):
            if adjm.m[i][j] == "Bomb":
                print('B  ', end="")
            elif adjm.m[i][j] >= 2:
                print(color(adjm.m[i][j])+str(adjm.m[i]
                      [j]-2) + " "+Style.RESET_ALL, end=" ")
        print()

# Running the Game-----------------------------
isRunning = True
while (isRunning == True):
    print_field()
    print("Select Coordinates to check (between 1 and Width/Height of the field):")
    print("line: ", end="")
    line = int(input()) - 1
    print("column: ", end="")
    column = int(input()) - 1

    # Coordenadas Inválidas
    if line < 0 or column < 0 or line >= M_HEIGHT or column >= M_WIDTH:
        isRunning = False
    # Avaliar coordenada
    else:
        if field.m[line][column] == 1:
            field.m[line][column] = "Bomb"
            print_adjm()
            print("Oh no! You stepped on a mine! GAME OVER")
            isRunning = False
        elif field.m[line][column] == 0:
            field.m[line][column] = adjm.m[line][column]
            field.countdown-=1
            if field.m[line][column] == 2:
                # Aplicar DFS para mostrar todas as células não adjacentes a bombas
                stack = [(line, column)]
                y = line
                x = column
                while (stack != []):
                    if (field.m[max(0, y-1)][x] == 0 and adjm.m[max(0, y-1)][x] == 2):  # célula acima
                        y = max(0, y-1)
                        field.m[y][x] = adjm.m[y][x]
                        field.countdown-=1
                        stack.append((y, x))
                    # célula à direita
                    elif (field.m[y][min(M_WIDTH-1, x+1)] == 0 and adjm.m[y][min(M_WIDTH-1, x+1)] == 2):
                        x = min(M_WIDTH-1, x+1)
                        field.m[y][x] = adjm.m[y][x]
                        field.countdown-=1
                        stack.append((y, x))
                    # célula abaixo
                    elif (field.m[min(M_HEIGHT-1, y+1)][x] == 0 and adjm.m[min(M_HEIGHT-1, y+1)][x] == 2):
                        y = min(M_HEIGHT-1, y+1)
                        field.m[y][x] = adjm.m[y][x]
                        field.countdown-=1
                        stack.append((y, x))
                    # célula à esquerda
                    elif (field.m[y][max(0, x-1)] == 0 and adjm.m[y][max(0, x-1)] == 2):
                        x = max(0, x-1)
                        field.m[y][x] = adjm.m[y][x]
                        field.countdown-=1
                        stack.append((y, x))
                    else:
                        # Pintar Bordas dos 0s
                        if (field.m[max(0, y-1)][x] == 0 and adjm.m[max(0, y-1)][x] != 2):  # cima
                            field.m[max(0, y-1)][x] = adjm.m[max(0, y-1)][x]
                            field.countdown-=1
                        # direita
                        if (field.m[y][min(M_WIDTH-1, x+1)] == 0 and adjm.m[y][min(M_WIDTH-1, x+1)] != 2):
                            field.m[y][min(M_WIDTH-1, x+1)
                                       ] = adjm.m[y][min(M_WIDTH-1, x+1)]
                            field.countdown-=1
                        if (field.m[min(M_HEIGHT-1, y+1)][x] == 0 and adjm.m[min(M_HEIGHT-1, y+1)][x] != 2):  # baixo
                            field.m[min(M_HEIGHT-1, y+1)
                                    ][x] = adjm.m[min(M_HEIGHT-1, y+1)][x]
                            field.countdown-=1
                        if (field.m[y][max(0, x-1)] == 0 and adjm.m[y][max(0, x-1)] != 2):  # esquerda
                            field.m[y][max(0, x-1)] = adjm.m[y][max(0, x-1)]
                            field.countdown-=1

                        # Pintar Bordas dos 0s (Cantos)
                        if (field.m[max(0, y-1)][max(0, x-1)] == 0 and adjm.m[max(0, y-1)][max(0, x-1)] != 2):
                            field.m[max(0, y-1)][max(0, x-1)
                                                 ] = adjm.m[max(0, y-1)][max(0, x-1)]
                            field.countdown-=1
                        if (field.m[max(0, y-1)][min(M_WIDTH-1, x+1)] == 0 and adjm.m[max(0, y-1)][min(M_WIDTH-1, x+1)] != 2):
                            field.m[max(0, y-1)][min(M_WIDTH-1, x+1)
                                                 ] = adjm.m[max(0, y-1)][min(M_WIDTH-1, x+1)]
                            field.countdown-=1
                        if (field.m[min(M_HEIGHT-1, y+1)][max(0, x-1)] == 0 and adjm.m[min(M_HEIGHT-1, y+1)][max(0, x-1)] != 2):
                            field.m[min(M_HEIGHT-1, y+1)][max(0, x-1)
                                                          ] = adjm.m[min(M_HEIGHT-1, y+1)][max(0, x-1)]
                            field.countdown-=1
                        if (field.m[min(M_HEIGHT-1, y+1)][min(M_WIDTH-1, x+1)] == 0 and adjm.m[min(M_HEIGHT-1, y+1)][min(M_WIDTH-1, x+1)] != 2):
                            field.m[min(M_HEIGHT-1, y+1)][min(M_WIDTH-1, x+1)
                                                          ] = adjm.m[min(M_HEIGHT-1, y+1)][min(M_WIDTH-1, x+1)]
                            field.countdown-=1
                        # Pop
                        (y, x) = stack.pop()

    if field.countdown <= 0:
        print_field()
        print("Player Wins!")
        isRunning = False
# --------------------------------------------
