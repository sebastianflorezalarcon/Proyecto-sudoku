# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 15:37:08 2020

@author: USER
"""

import pygame
import time
pygame.font.init()

class cuadricula:
    tablero = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
               [6, 0, 0, 0, 7, 5, 0, 0, 9],
               [0, 0, 0, 6, 0, 1, 0, 7, 8],
               [0, 0, 7, 0, 4, 0, 2, 6, 0],
               [0, 0, 1, 0, 5, 0, 9, 3, 0],
               [9, 0, 4, 0, 6, 0, 0, 0, 5],
               [0, 7, 0, 3, 0, 0, 0, 1, 2],
               [1, 2, 0, 0, 0, 7, 4, 0, 0],
               [0, 4, 9, 2, 0, 6, 0, 0, 7]]
    
    def __init__(self, filas, columnas, ancho, alto, ganar):
        self.filas = filas
        self.columnas = columnas
        self.cubos = [[cubo(self.tablero[i][j], i, j, ancho, alto) for j in range(columnas)]for i in range(filas)]
        self.ancho = ancho
        self.alto = alto
        self.model = None
        self.update_model()
        self.selected = None
        self.ganar = ganar

    def update_model(self):
        self.model = [[self.cubos[i][j].value for j in range(self.columnas)] for i in range(self.filas)]

    def lugar(self, val):
        fila, columna = self.selected
        if self.cubos[fila][columna].value == 0:
            self.cubos[fila][columna].set(val)
            self.update_model()

            if valid(self.model, val, (fila,columna)) and self.solve():
                return True
            else:
                self.cubos[fila][columna].set(0)
                self.cubos[fila][columna].set_temp(0)
                self.update_model()
                return False

    def bosquejo(self, val):
        fila, columna = self.selected
        self.cubos[fila][columna].set_temp(val)
        
    def dibujo(self):
        
        brocha = self.ancho / 9
        for i in range(self.filas+1):
            if i % 3 == 0 and i != 0:
                espesor = 4
            else:
                espesor = 1
            pygame.dibujo.line(self.ganar, (0,0,0), (0, i*brocha), (self.ancho, i*brocha), espesor)
            pygame.dibujo.line(self.ganar, (0, 0, 0), (i * brocha, 0), (i * brocha, self.alto), espesor)

       
        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].dibujo(self.ganar)

    def selecccion(self, fila, columna):
        
        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].selected = False

        self.cubos.selected = True
        self.selected = (fila, columna)

    def limpiar(self):
        fila, columna = self.selected
        if self.cubos[fila][columna].value == 0:
            self.cubos[fila][columna].set_temp(0)

    def click(self, posicion):
        """
        :param: posicion
        :return: (fila, columna)
        """
        if posicion[0] < self.ancho and posicion[1] < self.alto:
            brocha = self.ancho / 9
            x = posicion[0] // brocha
            y = posicion[1] // brocha
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.cubos[i][j].value == 0:
                    return False
        return True

    def resolver(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            fila, columna = find

        for i in range(1, 10):
            if valid(self.model, i, (fila, columna)):
                self.model[fila][columna] = i

                if self.solve():
                    return True

                self.model[fila][columna] = 0

        return False

    def resolver_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            fila, columna = find

        for i in range(1, 10):
            if valid(self.model, i, (fila, columna)):
                self.model[fila][columna] = i
                self.cubos[fila][columna].set(i)
                self.cubos[fila][columna].draw_change(self.ganar, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.resolver_gui():
                    return True

                self.model[fila][columna] = 0
                self.cubos[fila][columna].set(0)
                self.update_model()
                self.cubos[fila][columna].draw_change(self.ganar, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class cubo:
    filas = 9
    columnas = 9

    def __init__(self, value, fila, columna, ancho, alto):
        self.value = value
        self.temp = 0
        self.fila = fila
        self.columna = columna
        self.ancho = ancho
        self.alto = alto
        self.selected = False
        

    def dibujo(self, ganar):
        fnt = pygame.font.SysFont("comicsans", 40)

        brocha = self.ancho / 9
        x = self.columna * brocha
        y = self.fila * brocha

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            ganar.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            ganar.blit(text, (x + (brocha/2 - text.get_ancho()/2), y + (brocha/2 - text.get_alto()/2)))

        if self.selected:
            pygame.dibujo.rect(ganar, (255,0,0), (x,y, brocha ,brocha), 3)

    def dibujo_cambio(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        brocha = self.ancho / 9
        x = self.col * brocha
        y = self.row * brocha

        pygame.dibujo.rect(win, (255, 255, 255), (x, y, brocha, brocha), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (brocha / 2 - text.get_ancho() / 2), y + (brocha / 2 - text.get_alto() / 2)))
        if g:
            pygame.dibujo.rect(win, (0, 255, 0), (x, y, brocha, brocha), 3)
        else:
            pygame.dibujo.rect(win, (255, 0, 0), (x, y, brocha, brocha), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) 

    return None


def valid(bo, num, posicion):

    #verifica filas
    for i in range(len(bo[0])):
        if bo[posicion[0]][i] == num and posicion[1] != i:
            return False

    #verifica columnas
    for i in range(len(bo)):
        if bo[i][posicion[1]] == num and posicion[0] != i:
            return False

    # casilla verificacion 
    box_x = posicion[1] // 3
    box_y = posicion[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != posicion:
                return False

    return True
