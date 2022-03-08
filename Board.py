import pygame
from pygame.locals import *
import sys

from Balloon import Balloon
from Seesaw import Seesaw
from JumpBoard import JumpBoard
from Performer import Performer

from const import *
# 効果音

pygame.mixer.init(frequency = 44100)
pon=pygame.mixer.Sound("pon.wav")
bonus=pygame.mixer.Sound("bonus.wav")
jump=pygame.mixer.Sound("jump.wav")
fail=pygame.mixer.Sound("fail.wav")

class Board():
    def __init__(self, width, height, num_jumper):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width, self.height = (width, height)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsansms', FONT_SIZE)
        self.score = 0
        self.balloon_tilt = 0
        self.num_jumper_org = self.num_jumper = num_jumper

    def setup_yellows(self):
        image1 = pygame.image.load(YELLOW_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(YELLOW_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP + 2*(BALLOON_DIAM + BALLOON_GAP_Y)
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.yellows.add(Balloon(x, y, BALLOON_DIAM, -BALLOON_VX,
                                     YELLOW_SCORE, image1, image2))

    def setup_greens(self):
        image1 = pygame.image.load(GREEN_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(GREEN_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP + BALLOON_DIAM + BALLOON_GAP_Y
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.greens.add(Balloon(x, y, BALLOON_DIAM, BALLOON_VX,
                                    GREEN_SCORE, image1, image2))

    def setup_blues(self):
        image1 = pygame.image.load(BLUE_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(BLUE_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.blues.add(Balloon(x, y, BALLOON_DIAM, -BALLOON_VX,
                                   BLUE_SCORE, image1, image2))

    def setup_jumpboards(self):
        y = JUMP_BOARD_HIGH
        self.jumpboards.add(JumpBoard(0, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        self.jumpboards.add(JumpBoard(EAST-JUMP_BOARD_WIDTH, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        y = JUMP_BOARD_LOW
        self.jumpboards.add(JumpBoard(0, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        self.jumpboards.add(JumpBoard(EAST-JUMP_BOARD_WIDTH, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))

    def setup(self):
        self.stage = STAGE_START
        # Groupを準備する
        self.yellows = pygame.sprite.Group()    # 一番下の列
        self.greens = pygame.sprite.Group()     # 真ん中の列
        self.blues = pygame.sprite.Group()      # 一番上の列
        seesaws = pygame.sprite.Group()    # シーソー
        self.performers = pygame.sprite.Group() # 二人のパフォーマー
        self.jumpboards = pygame.sprite.Group() # 四つのジャンプ台

        self.setup_blues()          # 青のバルーンを準備
        self.setup_greens()         # 緑のバルーンを準備
        self.setup_yellows()        # 黄色のバルーンを準備

        self.setup_jumpboards()     # ジャンプボードを準備

        # シーソーを準備する
        self.seesaw = Seesaw(SEESAW_X, SEESAW_Y, SEESAW_W, SEESAW_H,
                             SEESAW_VX, SEESAW1_IMAGE, SEESAW2_IMAGE)
        seesaws.add(self.seesaw)    # Eventを受ける為、Group以外を持つ

        # パフォーマを準備する(一人目はジャンプ中)
        self.performers.add(Performer(1, WEST, PERFORMER_Y,
                                      PERFORMER_W, PERFORMER_H,
                                      STATE_JUMPING, PERFORMER1_IMAGE))
        # 二人目はシーソーの右端に立つ
        performer = Performer(2, SEESAW_X + SEESAW_W - PERFORMER_W,
                              SEESAW_Y + SEESAW_H - PERFORMER_H,
                              PERFORMER_W, PERFORMER_H,
                              STATE_STANDING, PERFORMER2_IMAGE)
        self.performers.add(performer)
        # 二人目は、シーソーに乗っている事を伝える
        self.seesaw.ride(performer)

        # Groupの一括管理
        self.objects = [self.yellows, self.greens, self.blues, seesaws,
                        self.performers, self.jumpboards]
        self.balloons = [self.yellows, self.greens, self.blues]
        self.screen.fill(BLACK)
        self.frame()
        self.show_score()

    def show_score(self):
        text = self.font.render( ("SCORE : %d" % self.score), True, WHITE )
        self.screen.blit(text, (SCORE_X, SCORE_Y))
        text = self.font.render( ("PLAYER : %d" % self.num_jumper), True, WHITE )
        position = text.get_rect()
        position.y = SCORE_Y
        position.right = EAST
        self.screen.blit(text, position)

    def frame(self):
        pygame.draw.rect(self.screen, WHITE,
                         pygame.Rect(WEST, NORTH, EAST-WEST, SOUTH-NORTH), 1)

    def run(self):
        while (self.stage != STAGE_QUIT):
            if self.stage == STAGE_START:
                self.intro()
            self.animate()
            self.num_jumper -= 1
            if self.stage == STAGE_DOWN and self.num_jumper > 0:
                self.stage = STAGE_NEXT
                self.next()
            if self.stage != STAGE_QUIT:
                if self.num_jumper == 0:
                    self.stage = STAGE_OVER
                    self.game_over()
                else:       # 再開する
                    self.stage = STAGE_RUN

    def show_center_message(self, message, y):
        text = self.font.render(message, True, WHITE)
        position = text.get_rect()
        position.center = (X_CENTER, y)
        self.screen.blit(text, position)

    def intro_message(self):
        y = MESSAGE_TOP
        self.show_center_message("INSERT COIN", y)
        y += MESSAGE_GAP
        self.show_center_message("OR", y)
        y += MESSAGE_GAP
        self.show_center_message("PRESS 'SPACE' BAR", y)
        y += MESSAGE_GAP
        self.show_center_message("TO START", y)

    def intro(self):
        self.balloon_tilt = 0
        self.stage = STAGE_INTRO
        self.num_jumper = self.num_jumper_org
        self.score = 0
        while (self.stage == STAGE_INTRO):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.intro_message()

            # バルーンのアニメ
            self.balloon_anime() # 傾きを切り替える
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
        self.seesaw.back_origin()
        for performer in self.performers:
            performer.back_origin(self.seesaw)
        # self.seesaw.back_origin()

    def next_message(self):
        y = MESSAGE_TOP + MESSAGE_GAP
        self.show_center_message("JUMPER 1 DOWN", y)
        message = str(self.num_jumper) + "  JUMPER"
        if self.num_jumper > 1:
            message +="S"
        message += "  LEFT";
        y += MESSAGE_GAP
        self.show_center_message(message, y)

    def next(self):
        self.balloon_tilt = 0
        count = FPS * 2
        while (count > 0 and self.stage != STAGE_QUIT):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.next_message()

            # バルーンのアニメ
            self.balloon_anime()
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
            count -= 1
        self.seesaw.back_origin()
        for performer in self.performers:
            performer.back_origin(self.seesaw)

    def game_over_message(self):
        y = MESSAGE_TOP + MESSAGE_GAP
        self.show_center_message("GAME OVER!", y)
        y += MESSAGE_GAP*2
        self.show_center_message("PRESS 'SPACE' BAR", y)
        y += MESSAGE_GAP
        self.show_center_message("TO REPLAY", y)

    def game_over(self):
        self.balloon_tilt = 0
        count = FPS * 5
        while (count > 0 and self.stage != STAGE_RUN):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.game_over_message()

            # バルーンのアニメ
            self.balloon_anime()
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
            count -= 1
        if self.stage == STAGE_RUN:
            self.seesaw.back_origin()
            for performer in self.performers:
                performer.back_origin(self.seesaw)
            self.stage = STAGE_START
        else:
            self.stage = STAGE_QUIT

    def balloon_anime(self):
        self.balloon_tilt += 1
        if self.balloon_tilt >= FPS:
            self.balloon_tilt = 0
        # バルーンのアニメ
        for color_groups in self.balloons:
            for balloon in color_groups:
                balloon.set_balloon_tilt( self.balloon_tilt)

    def animate(self):
        while (self.stage == STAGE_RUN):
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    # 「左」キーを処理する
                    if event.key == pygame.K_LEFT:
                        self.seesaw.move_left()
                    # 「右」キーを処理する
                    if event.key == pygame.K_RIGHT:
                        self.seesaw.move_right()
                if event.type == pygame.KEYUP:
                    # 「左」キーを処理する
                    if event.key == pygame.K_LEFT:
                        self.seesaw.stop()
                    # 「右」キーを処理する
                    if event.key == pygame.K_RIGHT:
                        self.seesaw.stop()
            self.clock.tick(FPS)
            # バルーンのアニメ
            self.balloon_anime()
            # オブジェクトの描画
            for obj in self.objects:
                obj.update()
                obj.draw(self.screen)
            # パフォーマの墜落を確認
            for performer in self.performers.sprites():
                if performer.down:
                    fail.play() # 墜落音を再生
                    self.stage = STAGE_DOWN
            # パフォーマとジャンプ台の接触をチェック
            collided = pygame.sprite.groupcollide(self.jumpboards,
                                                  self.performers, False, False)
            if len(collided)>0:
                for jumpboard in collided:
                    performer = collided.get(jumpboard).pop()
                    jump.play()
                    jumpboard.bump(performer)

            # シーソーとパフォーマの接触をチェック
            collided = pygame.sprite.spritecollide(self.seesaw,
                                                   self.performers, False )
            if len(collided) > 1:  # 必ず1人は接触しているので
                for person in self.performers.sprites():
                    if person.status == STATE_JUMPING:  #personが今飛んでいるなら
                        jumper = person #jumperに割り当てる
                    else: #personが今飛んでいないなら
                        stand_by_player = person #stand_by_playerに割り当てる
                if jumper.inactive_y == 0: # ジャンパーが着地
                    x_offset, y_rate = jumper.check(self.seesaw)
                    #rateがゼロなら墜落
                    if y_rate==0:
                        fail.play() # 墜落音を再生
                        self.stage = STAGE_DOWN
                    else:
                        jump.play() # ジャンプ音を再生
                    # 着地したジャンパーの情報を、立っているパフォーマにひき継ぐ
                    vx, vy = jumper.landed(self.seesaw)
                    vx = max(min((self.seesaw.vx + vx)/2 + x_offset, MAX_VX),
                             -MAX_VX)
                    vy = min(vy * y_rate, MAX_VY)
                    stand_by_player.jump(vx, -vy, self.seesaw)
                else:  # 今、飛びたてのjumperが一 ( 着地じゃない )
                    jumper.inactive_y += jumper.vy
                    if jumper.inactive_y <= 0:
                        jumper.inactive_y = 0 # シーソーを離れた
            # パフォーマと風船の接触をチェック
            for balloons in self.balloons:
                collided = pygame.sprite.groupcollide(
                    balloons, self.performers, False, False
                    )
                if len(collided)>0:
                    for balloon in collided:
                        performer = collided.get(balloon).pop()
                        self.score += balloon.bump(performer)
                        pon.play() # 破裂音を再生
                        balloons.remove(balloon)
                    if len(balloons) == 0:
                        if balloons == self.yellows:
                            bonus.play() # ボーナス音を再生
                            self.score += YELLOW_BONUS
                            self.setup_yellows()
                        elif balloons == self.greens:
                            bonus.play() # ボーナス音を再生
                            self.score += GREEN_BONUS
                            self.setup_greens()
                        else:
                            bonus.play() # ボーナス音を再生
                            self.score += BLUE_BONUS
                            self.setup_blues()

            # 表示の更新
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()