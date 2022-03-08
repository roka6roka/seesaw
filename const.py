WHITE, RED, GREEN = ((255, 255, 255), (255, 0, 0),(0, 255, 0))
BLUE, YELLOW, BLACK = ((0, 0, 255), (255, 255, 0), (0, 0, 0))
FPS = 40        # 描画更新速度(flame per second)

WIDTH = 800     # 画面全体幅
HEIGHT = 700    # 画面全体高さ
NORTH = 80      # 盤面トップ
WEST = 0        # 盤面左端
EAST = 800      # 盤面右端
SOUTH = 680     # 盤面ボトム
X_CENTER = (WEST + EAST)/2  # 画面Xの中心

BALLOON_TOP = 18 + NORTH  # バルーンのトップの高さ => 98
BALLOON_GAP = 35  # バルーンの列の間隔
BALLOON_GAP_Y = 20
BALLOON_DIAM = 45 # バルーンの直径
BALLOON_VX = 2    # バルーンの移動する速度
BALLOON_JUMP = WIDTH + BALLOON_DIAM + BALLOON_GAP
BALLOON_LAST_X = BALLOON_JUMP + 1          # 初期設定
BALLOON_STEP = BALLOON_DIAM + BALLOON_GAP  # バルーンのY加算

YELLOW_IMAGE1 = 'yellow1.png'
YELLOW_IMAGE2 = 'yellow2.png'
GREEN_IMAGE1 = 'green1.png'
GREEN_IMAGE2 = 'green2.png'
BLUE_IMAGE1 = 'blue1.png'
BLUE_IMAGE2 = 'blue2.png'

YELLOW_SCORE = 10
GREEN_SCORE = 20
BLUE_SCORE = 30
YELLOW_BONUS = 100
GREEN_BONUS = 200
BLUE_BONUS = 300

SEESAW_H = 20    # シーソーの高さ
SEESAW_W = 140   # シーソーの横幅
SEESAW_X = (EAST-SEESAW_W)/2 + WEST
SEESAW_Y = SOUTH - SEESAW_H - 15
SEESAW_VX = 8    # シーソーの移動スピード
SEESAW1_IMAGE = "seesaw1.png"
SEESAW2_IMAGE = "seesaw2.png"

FONT_SIZE = 24

SCORE_X = 0      # スコア表示位置
SCORE_Y = 0

MESSAGE_TOP = BALLOON_TOP + 3*BALLOON_DIAM + 2*BALLOON_GAP_Y + 50
MESSAGE_GAP = 40   # タイトルメッセージの表示位置

PERFORMER_H = 40 # 棒人間の高さ
PERFORMER_W = 20 # 棒人間の幅
PERFORMER1_IMAGE = "performer1.png"
PERFORMER2_IMAGE = "performer2.png"

# 落ちる人の初期位置
PERFORMER_X = (EAST-PERFORMER_W)/2 + WEST
PERFORMER_Y = BALLOON_TOP + 3*BALLOON_DIAM + 2*BALLOON_GAP_Y + 50
JUMP_CENTER = (SEESAW_W-PERFORMER_W)/2  # ジャンプ速度の計算に使用
STATE_JUMPING = 1
STATE_STANDING = 2
GRAVITY = 0.3
MAX_VX = SEESAW_VX/1.2
MAX_VY = SEESAW_H - 2

# ジャンプボード
JUMP_BOARD_HIGH = MESSAGE_TOP + 100
JUMP_BOARD_LOW = SEESAW_Y - 100
JUMP_BOARD_WIDTH = 50
JUMP_BOARD_HEIGHT = 5
LEFT_BOARD = 1
RIGHT_BOARD = 2

NUM_JUMPER = 5

# 状態遷移
STAGE_START = 1
STAGE_INTRO = 2
STAGE_RUN = 3
STAGE_DOWN = 4
STAGE_NEXT = 5
STAGE_OVER = 6
STAGE_QUIT = 7
