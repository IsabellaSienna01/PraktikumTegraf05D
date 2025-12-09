import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Init board
board = [[0]*8 for _ in range(8)]

# Gerak Kuda
gerak = [
    [-2,1], [-1,2], [1,2], [2,1],
    [2,-1], [1,-2], [-1,-2], [-2,-1]
]

# Konversi Notasi Catur ke Koordinat
def chess_to_xy(notation):
    notation = notation.strip().upper()
    # Error jika format ga panjang 2 (A3/Lainnya)
    if len(notation) != 2:
        raise ValueError("Format harus seperti A1..H8")
    file = notation[0]            # A–H
    rank = int(notation[1])       # 1–8
    # Error jika Notasi bukan A-H dan 1-8
    if file < 'A' or file > 'H' or rank < 1 or rank > 8:
        raise ValueError("Notasi di luar A1..H8")
    x = ord(file) - ord('A')      # A=0, B=1
    y = rank-1                    # 1 -> 7, 8 -> 0
    return x, y

# Cek apakah koordinat legal
def islegal(x, y):
    return (0 <= x < 8 and 0 <= y < 8) # Jika diluar board maka balikin 0

# Fungsi mengecek derajat
def degree(x, y):
    deg = 0
    for i in range(8):
        nx = x + gerak[i][0] # koordinat awal + Gerak kuda
        ny = y + gerak[i][1] 
        if islegal(nx, ny) and board[nx][ny] == 0: # Selama masih legal dan belum dikunjungi
            deg += 1
    return deg

# Cek apakah (x,y) menyerang (sx,sy)
def attacks(x, y, sx, sy):
    for i in range(8):
        if x + gerak[i][0] == sx and y + gerak[i][1] == sy: # Cek apakah udah closed tour apa engga
            return True
    return False

# Init board
def init():
    for i in range(8):
        for j in range(8):
            board[i][j] = 0

# RANDOMIZED WARNSDORFF
def next_square(xy):
    x, y = xy
    best = 9 # Derajat minimum
    candidates = []
    count = 0

    for i in range(8):
        nx = x + gerak[i][0]
        ny = y + gerak[i][1]

        if islegal(nx, ny) and board[nx][ny] == 0: # Selama legal dan masih belum dikunjungi
            deg = degree(nx, ny) # derajat lama = derajat baru

            if deg < best: # Kalo lebih minimal
                best = deg
                candidates = [(nx, ny)] # reset kandidat dan pilih jadi kandidat next step
                count = 1
            elif deg == best: # Kalo sama
                candidates.append((nx, ny)) # tambahkan ke calon kandidat (ada lebih dari 1 cabang)
                count += 1

    if count == 0: # Kalo ga gerak = dead end
        return (-1, -1)

    return random.choice(candidates) # pilih salah satu kandidat secara random

# Ngebuat jalannya knight
def generate_tour(sx, sy):
    init()
    x, y = sx, sy
    board[x][y] = 1

    for step in range(2, 65):
        x, y = next_square((x, y))
        if x == -1:
            return False   # gagal, dead-end
        board[x][y] = step

    return True

# Cetak papan dengan rank 8 di atas sehingga mudah dibaca:
def print_board():
    for rank in range(7, -1, -1):
        for file in range(8):
            print(f"{board[file][rank]:3d}", end="")
        print()


# Fungsi untuk menggambar rute dalam png
def plot_chess_knight_path(save_png=False, png_name="knight_tour.png"):
    fig, ax = plt.subplots(figsize=(6,6))

    # gambar kotak catur 8x8 — mulai dari (0,0) di kiri bawah
    for x in range(8):      # file A..H -> x
        for y in range(8):  # rank 1..8 -> y
            # warna papan (classic light/dark)
            color = '#EEEED2' if (x + y) % 2 == 0 else '#769656'
            rect = patches.Rectangle((x, y), 1, 1, facecolor=color)
            ax.add_patch(rect)

    # ambil path langkah dari board[x][y]
    path = [(0,0)] * 64
    for x in range(8):
        for y in range(8):
            step = board[x][y]
            if step != 0:
                # mapping langsung: board[x][y] -> (x, y)
                path[step-1] = (x, y)

    xs = [p[0] + 0.5 for p in path]  # tengah kotak
    ys = [p[1] + 0.5 for p in path]

    # gambar garis & nomor langkah kecil
    ax.plot(xs, ys, marker='o', linewidth=2, markersize=6)
    for idx, (px, py) in enumerate(path, start=1):
        ax.text(px + 0.5, py + 0.5, str(idx), ha='center', va='center', fontsize=6, color='black')

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_xticks([i + 0.5 for i in range(8)])
    ax.set_xticklabels(['A','B','C','D','E','F','G','H'])
    ax.set_yticks([i + 0.5 for i in range(8)])
    ax.set_yticklabels(['1','2','3','4','5','6','7','8'])

    ax.set_title("Knight's Tour Path")
    ax.set_aspect('equal')
    plt.grid(False)
    if save_png:
        plt.savefig(png_name, bbox_inches='tight', dpi=200)
        print(f"Saved PNG: {png_name}")
    plt.show()

def tour():
    start = input("Input start (A1..H8): ") # Input start
    sx, sy = chess_to_xy(start)

    mode = int(input("Mode (1 = OPEN, 2 = CLOSED): ")) # Input mau open/closed (open dipastikan tidak closed)

    while True:
        if not generate_tour(sx, sy):
            continue

        # posisi langkah ke-64
        lx = ly = -1
        for x in range(8):
            for y in range(8):
                if board[x][y] == 64:
                    lx, ly = x, y

        closed = attacks(lx, ly, sx, sy)

        # Jika mode == 1 dan closed, ulangi tour... jika mode == 2 dan tidak closed ulangi tour..
        if mode == 1 and not closed:
            print("\nOPEN TOUR FOUND!\n")
            break
        if mode == 2 and closed:
            print("\nCLOSED TOUR FOUND!\n")
            break

    print_board()
    print("\n")
    plot_chess_knight_path(save_png=True, png_name="knight_tour.png")

def main():
    random.seed(int(time.time()))
    tour()

if __name__ == "__main__":
    main()
