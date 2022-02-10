import PIL
import random
import arcade



# фиксированное количество строк и колонн

rows = 15
colu = 15
# высота и ширина ячеек

wid = 30
hei = 30
# ширина сетки
marg = 5
# определяем размер экрана

scrw = (wid + marg) * colu + marg
scrh = (hei + marg) * rows + marg
scrt = "тетрис-_-"



# список цветов
col = [
       (130, 120, 180),
       (75, 0, 0),
       (0, 65, 0),
       (0, 0, 75),
       (75, 62, 0),
       (75, 75, 52),
       (68, 0, 75),
       (0, 72, 72)
        ]

# список форм

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]


def crtex():

    # создаем список
    netex = []
    for colo in col:
        im = PIL.Image.new('RGB', (wid, hei), colo)
        netex.append(arcade.Texture(str(colo), image=im))
    return netex


texl = crtex()


def rotcl(a):

    # устанавливаем врашение
    # по часовой стрелке
    return [[a[y][x] for y in range(len(a))] for x in range(len(a[0]) - 1, -1, -1)]


def checo(bo, a, ofs):

    # проверяем столкновения
    ofx, ofy = ofs
    for cy, row in enumerate(a):
        for cx, cell in enumerate(row):
            if cell and bo[cy + ofy][cx + ofx]:
                return True
    return False


def remor(bo, r):

    #при получении строки, её удаление
    del bo[r]
    # добавление строки сверху
    return [[0 for _ in range(colu)]] + bo



def jomat(ma1, ma2, ma2ofs):

    # здесь мы копируем копируем в первую матрицу вторую
    # основываясь на смещения х и у
    ofx, ofy = ma2ofs
    for cy, row in enumerate(ma2):
        for cx, val in enumerate(row):
            ma1[cy + ofy - 1][cx + ofx] += val
    return ma1


def nb():

    # создаем основную доску
    bo = [[0 for _x in range(colu)] for _y in range(rows)]
    # делаем нижнюю границу
    bo += [[1 for _x in range(colu)]]
    return bo


class mg(arcade.Window):

    def __init__(self, width, height, title):
        # настроим приложение

        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        self.bd = None
        self.frco = 0
        self.gaov = False
        self.pa = False
        self.bospl = None

        self.st = None
        self.stx = 0
        self.sty = 0

    def new_st(self):

        # выбираем рандомно фигуру
        self.st = random.choice(shapes)
        # устанавливаем местоположение
        self.stx = int(colu / 2 - len(self.st[0]) / 2)
        self.sty = 0

        if checo(self.bd, self.st, (self.stx, self.sty)):
            self.gaov = True

    def setup(self):
        self.bd = nb()

        self.bospl = arcade.SpriteList()
        for row in range(len(self.bd)):
            for column in range(len(self.bd[0])):
                sprite = arcade.Sprite()
                for texture in texl:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (marg + wid) * column + marg + wid // 2
                sprite.center_y = scrh - (marg + hei) * row + marg + hei // 2

                self.bospl.append(sprite)

        self.new_st()
        self.update_board()

    def drop(self):
        # функция пацения
        if not self.gaov and not self.pa:
            self.sty += 1
            if checo(self.bd, self.st, (self.stx, self.sty)):
                self.bd = jomat(self.bd, self.st, (self.stx, self.sty))
                while True:
                    for i, row in enumerate(self.bd[:-1]):
                        if 0 not in row:
                            self.bd = remor(self.bd, i)
                            break
                    else:
                        break
                self.update_board()
                self.new_st()

    def rotast(self):
        # поворот
        if not self.gaov and not self.pa:
            new_stone = rotcl(self.st)
            if not checo(self.bd, new_stone, (self.stx, self.sty)):
                self.st = new_stone

    def on_update(self, dt):

        self.frco += 1
        if self.frco % 10 == 0:
            self.drop()

    def move(self, delta_x):
        # перемещение фигуры
        if not self.gaov and not self.pa:
            new_x = self.stx + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > colu - len(self.st[0]):
                new_x = colu - len(self.st[0])
            if not checo(self.bd, self.st, (new_x, self.sty)):
                self.stx = new_x

    def on_key_press(self, key, modifiers):
        # связь с клавиатурой
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.UP:
            self.rotast()
        elif key == arcade.key.DOWN:
            self.drop()


    def draw_grid(self, grid, offset_x, offset_y):
        #  рисуем сетку
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column]:
                    color = col[grid[row][column]]
                    x = (marg + wid) * (column + offset_x) + marg + wid // 2
                    y = scrh - (marg + hei) * (row + offset_y) + marg + hei // 2

                    arcade.draw_rectangle_filled(x, y, wid, hei, color)

    def update_board(self):
        for row in range(len(self.bd)):
            for column in range(len(self.bd[0])):
                v = self.bd[row][column]
                i = row * colu + column
                self.bospl[i].set_texture(v)

    def on_draw(self):

        arcade.start_render()
        self.bospl.draw()
        self.draw_grid(self.st, self.stx, self.sty)


def main():

    my_game = mg(scrw, scrh, scrt)
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
