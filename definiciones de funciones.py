# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 20:38:25 2020

@author: anapl
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
        self.cuadricula = [[cuadricula(self.tablero[i][j], i, j, ancho, alto) for j in range(columnas)]for i in range(filas)]
        self.ancho = ancho
        self.alto = alto
        self.model = None
        self.update_model()
        self.selected = None
        self.ganar = ganar

    def update_model(self):
        self.model = [[self.cuadricula[i][j].value for j in range(self.columnas)] for i in range(self.filas)]

    def lugar(self, val):
        fila, columna = self.selected
        if self.cuadricula[fila][columna].value == 0:
            self.cuadricula[fila][columna].set(val)
            self.update_model()

            if val(self.model, val, (fila,columna)) and self.solve():
                return True
            else:
                self.cuadricula[fila][columna].set(0)
                self.cuadriculas[fila][columna].set_temp(0)
                self.update_model()
                return False

    def bosquejo(self, val):
        fila, columna = self.selected
        self.cuadricula[fila][columna].set_temp(val)
        
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
                self.cuadriculas[i][j].dibujo(self.ganar)

    def selecccion(self, fila, columna):
        
        for i in range(self.filas):
            for j in range(self.columnas):
                self.cuadriculas[i][j].selected = False

        self.cuadriculas.selected = True
        self.selected = (fila, columna)

    def limpiar(self):
        fila, columna = self.selected
        if self.cuadriculas[fila][columna].value == 0:
            self.cuadriculas[fila][columna].set_temp(0)

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
                if self.cuadriculas[i][j].value == 0:
                    return False
        return True
