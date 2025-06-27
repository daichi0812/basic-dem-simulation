import taichi as ti

# Taichiを初期化する（計算バックエンドを選択）
ti.init(arch=ti.gpu)

# パラメータ
n_particles = 1
particle_pos = ti.Vector.field(2, dtype=ti.f32, shape=n_particles) # 2次元ベクトル(x,y)を、n_particles個格納できるフィールド
win_x, win_y = 800, 800 # ウィンドウサイズを変数で持っておくと便利
r_pixels = 15   # 半径をピクセル単位で定義
# 半径をピクセルから正規化座標に変換
r_normalized = r_pixels / win_x

# 初期化
particle_pos[0] = ti.Vector([0.5, 0.5])

# GUIセットアップ
window = ti.ui.Window("One Particle", (win_x, win_y))
canvas = window.get_canvas()

# メインループ
while window.running:
    canvas.circles(particle_pos, radius=r_normalized, color=(1, 1, 1))
    window.show()

