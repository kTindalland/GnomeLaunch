# Gnome Launch main file
from subroutines import *
import pygame

pygame.init()
font = pygame.font.SysFont("roboto", 20, True, False) # Default font
font = pygame.font.SysFont("NasalizationRg-Regular", 20, False, False)

def main():
    startMenu(font)

if __name__ == '__main__':
    main()