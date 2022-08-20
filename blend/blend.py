from PIL import Image, ImageDraw, ImageFilter
import random

fp1 = '../samples/uzi.jpeg'
fp2 ='../samples/kdot.jpg'
fp3 = '../samples/21_savage.jpg'

b = Image.open(fp1)
a = Image.open(fp2)
c = Image.open(fp3)

# Simple Blend Test
res = Image.blend(a, b, 0.5)
res.save('simple.jpg')


# Random Polygon Test
pg = Image.new('L', b.size, 0)
pg2 = Image.new('L', b.size, 0)
draw = ImageDraw.Draw(pg)
draw2 = ImageDraw.Draw(pg2)

def gp(n):
    p = []
    for i in range(n):
        max = 640
        p.append((
            random.randint(0,max),
            random.randint(0,max)
        ))
    return p

draw.polygon(gp(4), fill=255)
draw2.polygon(gp(4), fill=255)

pg_blur = pg.filter(ImageFilter.GaussianBlur(10))
pg2_blur = pg2.filter(ImageFilter.GaussianBlur(10))

res = Image.composite(b,a, pg_blur)
res = Image.composite(c,res, pg2_blur)
res.save('shape.jpg')

# Random Noise Test
noise = Image.effect_noise(b.size, 255)
res = Image.composite(b,a,noise)
res.save('noise.jpg')

# Mandle
e = (0-2,1,-1.5,1.5)
man = Image.effect_mandelbrot(b.size,e, 50)

