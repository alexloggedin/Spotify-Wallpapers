import math
import os
from PIL import Image, ImageFilter
import random
import requests
from datetime import datetime
from Handlers.SpotifyHandler import AlbumCoverGetter
from CollageMaker.Sampler import poisson_disk_sampling

IMG_HEIGHT = 640
MIN_VAR = 0.5
MAX_VAR = 1.5


class CollageMakerV2:

    def __init__(self, 
    covers,                         # List of URLs pointing to images
    width = 1080,           
    height = 1080, 
    scale = 1,                      # 1, 2, 3
    type = 'collage',               # grid, collage 
    tilt = 'rand',                  # none, uniform, grid, rand
    bgType = 'solid',                 # grid, solid
    bgColor = (0,0,0),              # Black default, no transparency
    transparentTiltBg= True,           # Transparent Bg for tilt
    randomType = 'full',             # semi, full
    varySize = False
    ):
        self.collage_height = round(height)
        self.collage_width = round(width)
        self.cover_list = covers
        self.type = type
        self.scale = scale
        self.tilt = tilt
        self.bg_type = bgType
        self.bg_color = bgColor
        self.random_type = randomType
        self.transparent_bg = transparentTiltBg
        self.vary_size = varySize
        self.img_size = self.scaleDimensions() / self.scale 
        print(f"Image Size: {self.img_size}") 

    def scaleDimensions(self):
        # Use GCF to determine scale factor
        h, w = self.collage_height, self.collage_width
        if h > w:
            h, w = w, h
        for x in range(IMG_HEIGHT, 0, -1):
            if h % x == 0 and w % x == 0:
                if (x < 100):
                    x = x * 20
                return int(x)

    """
    Takes the covers and populates a matrix where [row][col] = image link 
    Write a new cover assignment function if I want frequency data
    """
    def organizeCoords(self):
        # Calculate number of rows and columns based on image size
        img_size = round(self.scaleDimensions() / self.scale)
        n_rows = int(self.collage_width / img_size)
        n_cols = int(self.collage_height / img_size)
        print(f"Total Items: {n_rows * n_cols}")

        # Generate Grid
        c = set()

        for row in range(n_rows):
            for col in range(n_cols):
                c.add((row, col))
        
        return c

    def nameCollage(self):
        dimensions = str(self.collage_width) + 'x' + str(self.collage_height)
        date = str(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        folder = 'dev_collages'
        return f'{folder}/{self.type}_scale{self.scale}_{date}.png'
    
    def expand2square(self, pil_img):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), self.bg_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), self.bg_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result
    
    def setRandomImageCoords(self, row, col, sz):
        offset = round(self.scaleDimensions() / 8)

        # Set boundary
        MAX_X = self.collage_width - round(.5*sz)
        MAX_Y = self.collage_height - round(.5*sz)

        # full random
        fullrandom = (random.randint(0 - offset, MAX_X), random.randint(0 - offset, MAX_Y))

        # pseudo random
        min = round(-offset)
        max = round(offset)

        x = (row * sz) + random.randint(min, max)
        y = (col * sz) + random.randint(min, max)
        
        # MAX CHECK MAX_X - offset
        x = x if x < MAX_X else random.randint(0 - offset, MAX_X)
        y = y if y < MAX_Y else random.randint(0 - offset, MAX_Y)

        # #MIN CHECK
        x = x if x > 0 - offset else random.randint(0, offset)
        y = y if y > 0 - offset else random.randint(0, offset)

        pseudo = (round(x),round(y))

        return pseudo if self.random_type == 'semi' else fullrandom

    def setTilt(self, img):
        angle = 35
        if img.size[0] != img.size[1]:
            img = self.expand2square(img)

        if self.tilt == 'uniform': 
            angle = 45
            img = img.rotate(angle, fillcolor = self.bg_color, expand=True)
        
        elif self.tilt == 'grid': 
            angle = random.randrange(-270, 270, 90)
            img = img.rotate(angle, fillcolor = self.bg_color, expand=True)
        
        elif self.tilt == 'rand':
            angle = random.randint(-angle,angle)
            img = img.rotate(angle, fillcolor = "black", expand=True)
        
        elif self.tilt == 'none':
            angle = 0
            img = img.rotate(angle, fillcolor = "black", expand=True)           

        return img,angle

    def layoutBaseGrid(self, collage, coords, covers):
        total = len(coords)

        while coords:
            if len(covers) == 0:
                covers = set(self.cover_list)

            img_url  = covers.pop()
            row, col, = coords.pop()
            diff = total - len(coords)
            # print(f"Printing Grid -> ({ math.trunc(((diff/total) * 100)) } %) | {diff} out of {total}")

            # Load Image
            img = Image.open(requests.get(img_url, stream=True).raw)
            #img = Image.open(img_url)
            
            #Resize image based on scale
            img.thumbnail((self.img_size, self.img_size))

            #Get coordinates
            location = (round((row * self.img_size)),round((col * self.img_size)))

            # Add Image to document    
            collage.paste(img, (location))
            img.close()
        
        return collage

    def layoutCollage(self, collage, coords, covers):
        total = len(coords)

        while coords:
            if len(covers) == 0:
                print("Resetting Cover list")
                covers = set(self.cover_list)

            img_url  = covers.pop()
            row, col, = coords.pop()
            diff = total - len(covers)
            print(f"Printing Collage -> ({ math.trunc(((diff/total) * 100)) } %) | {diff} out of {total}")

            # Load Image
            img = Image.open(requests.get(img_url, stream=True).raw)
            #img = Image.open(img_url)
            
            #Resize image based on scale
            f = 1 if not self.vary_size else random.uniform(0.5,1.5)
            sz = round(self.img_size * f)
            img.thumbnail((sz, sz))

            # Tilt Image if enabled
            t = self.setTilt(img)
            img = t[0]

            #Get coordinates

            if self.transparent_bg:
                mask = Image.new("RGBA", (sz,sz), color='white')
                mask = mask.rotate(t[1], expand = True)

                mask.save('mask.png')
                img.save('img.png')
                collage.paste(img, (location), mask)
                img.close()
                mask.close()
                continue

            # Add Image to document    
            collage.paste(img, (location))
            img.close()
        
        # Save Collage and Return it?
        return collage

    def createCollage(self):
        collage = Image.new('RGBA', (self.collage_width, self.collage_height), color=self.bg_color)
        coords = self.organizeCoords()
        covers = set(self.cover_list)
        if not self.bg_type == 'solid':
            collage =  self.layoutBaseGrid(collage, coords, covers)
        
        if self.type == 'collage':
            collage = self.layoutCollage(collage, coords, covers)
        
        # Save Collage and Return it?
        print(f"Save Location: {self.nameCollage()}")
        collage.save(self.nameCollage())
        return collage

g = AlbumCoverGetter()
#covers = g.getPlaylistTracks('3tFCJHUdyOH6wItKvVBBlJ')
covers = g.getTopTracks()

w = int(input("Enter Width: "))
h = int(input("Enter Height: "))
s = int(input('Enter Scale (1 is default): '))

c = CollageMaker(covers,
    width= w,
    height=h,
    scale = s, 
    type = 'collage', 
    bgColor = (255,255,255), # 4 value makes bg Transparent
    tilt='none', 
    transparentTiltBg=False, # Meant for tilts
    varySize=True, 
    randomType='semi',
    bgType= 'solid'
    )
c.createCollage()

# 3024 x 1984 pixels