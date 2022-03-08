import pygame
from pygame.locals import *
import sys
from Balloon import Balloon
from Seesaw import Seesaw
from JumpBoard import JumpBoard
from Performer import Performer
from Board import Board

from const import *

def main():
    pygame.mixer.init(frequency = 44100)
    pygame.mixer.music.load("bgm.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    board = Board(WIDTH, HEIGHT, NUM_JUMPER)
    board.setup()
    board.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()