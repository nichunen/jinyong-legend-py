import fonts
from texture import TextureGroup
import config
import pygame as pg
import utils

def viewer():
    import os
    names = []
    allT = {}
    for f in os.listdir(config.resource('data')):
        name, ext = os.path.splitext(f)
        if ext == '.grp':
            names.append(name)
    excludes = [
        'alldef', 'allsin', 'allsinbk', 'd1', 'd2', 'd3', 'mmap', 'wmap',
        'warfld', 'smap', 's1', 's2', 's3', 'ranger', 'r1', 'r2', 'r3',
    ]
    for name in excludes:
        names.remove(name)
    names.sort()
    print(names)
    idx = names.index('thing')

    pg.display.init()
    pg.font.init()
    screen = pg.display.set_mode((800, 600), 0, 32)

    font = fonts.get_default_font()

    def draw(idx_new):
        nonlocal idx
        idx = idx_new % len(names)
        name = names[idx]
        if name not in allT:
            allT[name] = TextureGroup(name)
        textures = allT[name]

        screen.fill((0, 0, 0, 0))
        w, h = screen.get_size()
        x, y = 0, 0
        rowMaxH = 0
        margin = 2
        for texture in textures.get_all():
            image = texture.image
            w1, h1 = image.get_size()
            if x + w1 < w:
                screen.blit(image, (x, y))
                rowMaxH = max(rowMaxH, h1)
            else:
                x = 0
                y += rowMaxH + margin
                rowMaxH = 0
            screen.blit(image, (x, y))
            x += w1 + margin
        textSize = font.size(name)
        rect = pg.Rect((0, 0), (textSize[0], textSize[1]))
        rect.right = screen.get_width() - 10
        rect.bottom = screen.get_height() - 10
        screen.blit(font.render(name, 1, (0xff, 0xff, 0xff)), rect)
        pg.display.update()

    tm = pg.time.Clock()
    draw(idx)
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT \
                    or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    draw(idx + 1)
                elif event.key == pg.K_LEFT:
                    draw(idx - 1)
        tm.tick(config.FPS)


if __name__ == '__main__':
    viewer()