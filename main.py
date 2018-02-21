# Gnome Launch main file
from subroutines import *
import pygame

pygame.init()
font = pygame.font.SysFont("roboto", 25, True, False) # Default font

def main():
    startMenu(font)

if __name__ == '__main__':
    main()