import tkinter as tk
import random
import time

# パラメータ設定
WIN_X, WIN_Y = 800, 800
DT = 1e-4
UPDATES_PER_FRAME = 10  # 1フレームあたりに実行する計算ステップ数
PARTICLE_RADIUS_PX = 10    # 粒子の半径（ピクセル単位）
# 半径を正規化座標(0.0 ~ 1.0)に変換
PARTICLE_RADIUS_NORM = PARTICLE_RADIUS_PX / WIN_X
NUM_PARTICLES = 300 # 粒子の数

# 物理状態変数
# 重力ベクトル
gravity = [0.0, -9.8]   # 重力ベクトル
restitution = 0.8   # 反発係数

# グローバル変数
particles = []  # すべての粒子オブジェクトを格納するリスト
# FPS計算用の変数を追加
last_time = 0
frame_count = 0
fps = 0

# 粒子のクラス
class Particle:
    def __init__(self, x, y, vx, vy, radius_norm, color, canvas):
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.radius = radius_norm
        self.color = color
        self.canvas = canvas

        # 描画用のID、最初はNoneにしておき、draw関数で作成する
        self.id = None

    def update_physics(self):
        # 粒子の物理状態を1ステップ更新する
        # 速度の更新（重力の影響）
        self.vel[0] += DT * gravity[0]
        self.vel[1] += DT * gravity[1]

        # 位置の更新
        self.pos[0] += DT * self.vel[0]
        self.pos[1] += DT * self.vel[1]

        # 壁との衝突判定と処理
        # 右壁
        if self.pos[0] + self.radius > 1.0:
            self.pos[0] = 1 - self.radius
            self.vel[0] *= -restitution
        # 左壁
        if self.pos[0] - self.radius < 0.0:
            self.pos[0] = self.radius
            self.vel[0] *= -restitution
        # 天井
        if self.pos[1] + self.radius > 1.0:
            self.pos[1] = 1 - self.radius
            self.vel[1] *= -restitution
        # 床
        if self.pos[1] - self.radius < 0.0:
            self.pos[1] = self.radius
            self.vel[1] *= -restitution

    def draw(self):
        # 現在の粒子の位置をキャンバスに描画する
        px = self.pos[0] * WIN_X
        py = (1.0 - self.pos[1]) * WIN_Y

        x0 = px - PARTICLE_RADIUS_PX
        y0 = py - PARTICLE_RADIUS_PX
        x1 = px + PARTICLE_RADIUS_PX
        y1 = py + PARTICLE_RADIUS_PX

        # もし初回描画なら図形を生成、そうでなければ移動
        if self.id is None:
            self.id = self.canvas.create_oval(x0, y0, x1, y1, fill=self.color, outline="")
        else:
            self.canvas.coords(self.id, x0, y0, x1, y1)

# 関数定義
def initialize_particles():
    # 指定された数の粒子をランダムな位置、速度で生成する
    global particles
    particles = []

    # 色の候補リスト
    color_palette = [
        "#FF6B6B", "#FFD166", "#06D6A0", "#118AB2", "#073B4C",
        "#F7B267", "#F79D65", "#F4845F", "#F27059", "#F25C54"
    ]

    for _ in range(NUM_PARTICLES):
        # ランダムな初期位置と初期速度
        x = random.uniform(0.1, 0.9)
        y = random.uniform(0.1, 0.9)
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-0.5, 0.5)

        # カラーをランダムに選択
        color = random.choice(color_palette)

        p = Particle(x, y, vx, vy, PARTICLE_RADIUS_NORM, color, canvas)
        particles.append(p)

def main_loop():
    global last_time, frame_count, fps

    # FPS計算ロジック
    current_time = time.time()
    frame_count += 1
    # 1秒以上経過したらFPSを計算して表示を更新
    if current_time - last_time > 1.0:
        fps = frame_count / (current_time - last_time)
        window.title(f"Basic DEM Simulator - FPS: {fps:.1f}")
        frame_count = 0
        last_time = current_time

    # 物理計算
    for _ in range(UPDATES_PER_FRAME):
        for p in particles:
            p.update_physics()

    # 描画
    for p in particles:
        p.draw()

    # 1ミリ秒に再度この関数を呼び出し、可能な限り高速にループさせる
    window.after(1, main_loop)

# GUIセットアップと実行
window = tk.Tk()
window.title("Basic DEM Simulator")
window.geometry(f"{WIN_X}x{WIN_Y}")
window.resizable(False, False)  # ウィンドウサイズを固定

# キャンバスの作成
canvas = tk.Canvas(window, width=WIN_X, height=WIN_Y, bg="#4D4D4D", highlightthickness=0)
canvas.pack()

# 初期化
initialize_particles()

# メインループを開始
main_loop()

# ウィンドウイベントループを開始
window.mainloop()