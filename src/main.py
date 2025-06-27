import taichi as ti

# Taichiを初期化する（計算バックエンドを選択）
ti.init(arch=ti.gpu)

# パラメータ
win_x, win_y = 800, 800 # ウィンドウサイズを変数で持っておくと便利
dt = 1e-4
n_particles = 1
r_pixels = 15   # 半径をピクセル単位で定義
r_normalized = r_pixels / win_x # 半径をピクセルから正規化座標に変換

# フィールド定義
particle_pos = ti.Vector.field(2, dtype=ti.f32, shape=n_particles) # 位置
particle_vel = ti.Vector.field(2, dtype=ti.f32, shape=n_particles)  # 速度
gravity = ti.Vector([0.0, -9.8])

# カーネル定義
@ti.kernel
def initialize():
    particle_pos[0] = [0.5, 0.5]
    particle_vel[0] = [0.0, 0.0]

@ti.kernel
def update():

    particle_vel[0] += dt * gravity
    particle_pos[0] += dt * particle_vel[0]

    if particle_pos[0][0] + r_normalized >= 1 or particle_pos[0][0] - r_normalized <= 0:
        particle_vel[0][0] *= -0.9

    if particle_pos[0][1] + r_normalized >= 1 or particle_pos[0][1] - r_normalized <= 0:
        particle_vel[0][1] *= -0.9


# GUIセットアップ
window = ti.ui.Window("One Particle", (win_x, win_y), vsync=True)
canvas = window.get_canvas()

# 初期化カーネルを呼び出す
initialize()

# メインループ
while window.running:
    for _ in range(10):
        update()

    canvas.set_background_color((0.3, 0.3, 0.3))    # 背景色: 暗めの灰色
    canvas.circles(particle_pos, radius=r_normalized, color=(0.2, 0.7, 0.7))
    window.show()

