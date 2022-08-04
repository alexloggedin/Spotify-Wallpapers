import math
import os
from PIL import Image, ImageFilter
import random
import requests
from datetime import datetime
from Handlers.SpotifyHandler import AlbumCoverGetter

# Temp Dev imports

IMG_HEIGHT = 640


class CollageMaker:

    def __init__(self, 
    covers,                         # List of URLs pointing to images
    width = 1080,           
    height = 1080, 
    scale = 2,                      # 1, 2, 3
    type = 'collage',               # grid, collage 
    tilt = 'rand',                  # none, uniform, grid, rand
    bgColor = (0,0,0),              # Black default, no transparency
    transparentBg= True,           # Transparent Bg for tilt
    randomType = 'full'             # semi, full
    ):
        self.collage_height = round(height)
        self.collage_width = round(width)
        self.cover_list = covers
        self.type = type
        self.scale = scale
        self.tilt = tilt
        self.bg_color = bgColor
        self.random_type = randomType
        self.transparent_bg = transparentBg
        self.img_size = self.scaleDimensions() / self.scale 
        print(f"Image Size: {self.img_size}") 

    def scaleDimensions(self):
        # Use GCF to determine scale factor
        h, w = self.collage_height, self.collage_width
        if h > w:
            h, w = w, h
        for x in range(IMG_HEIGHT, 0, -1):
            if h % x == 0 and w % x == 0:
                return int(x)

    """
    Takes the covers and populates a matrix where [row][col] = image link 
    Write a new cover assignment function if I want frequency data
    """
    def organzieCovers(self):
        # Calculate number of rows and columns based on image size
        img_size = round(self.scaleDimensions() / self.scale)
        n_rows = int(self.collage_width / img_size)
        n_cols = int(self.collage_height / img_size)
        print(f"Total Items: {n_rows * n_cols}")

        # Generate Grid
        unused = set(self.cover_list)
        used = set()
        images = set()

        for row in range(n_rows):
            for col in range(n_cols):
                # Check if unused is empty and reset the sets if so
                if len(unused) == 0:
                    unused = set(self.cover_list)
                    used.clear()

                # Take a cover and add it to the tuple set
                cover = unused.pop()
                images.add((row, col, cover))
                used.add(cover)
        
        return images

    def nameCollage(self):
        dimensions = str(self.collage_width) + 'x' + str(self.collage_height)
        date = str(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
        folder = 'dev_collages'
        return f'{folder}/{self.type}_scale{self.scale}_{date}.png'
    
    def setRandomImageCoords(self, row, col):
        offset = round(self.scaleDimensions() / 8)

        # Set boundary
        MAX_X = self.collage_width - round(.5*self.img_size)
        MAX_Y = self.collage_height - round(.5*self.img_size)

        # full random
        fullrandom = (random.randint(0 - offset, MAX_X), random.randint(0 - offset, MAX_Y))

        # pseudo random
        min = round(-offset)
        max = round(offset)

        x = (row * self.img_size) + random.randint(min, max)
        y = (col * self.img_size) + random.randint(min, max)
        
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

        if self.tilt == 'uniform': 
            angle = 45
            img = img.rotate(angle, fillcolor = self.bg_color, expand=True)
        
        elif self.tilt == 'grid': 
            angle = random.randrange(-270, 270, 90)
            img = img.rotate(angle, fillcolor = self.bg_color, expand=True)
        
        elif self.tilt == 'rand':
            angle = random.randint(-angle,angle)
            img = img.rotate(angle, fillcolor = "black", expand=True)

        return img,angle

    def layoutBaseGrid(self, collage, covers):
        total = len(covers)

        while covers:
            cover = covers.pop()
            row, col, img_url = cover
            diff = total - len(covers)
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

    def layoutCollage(self, collage, covers):
        total = len(covers)
        
        while covers:
            # Unload Tuple
            cover = covers.pop()
            row, col, img_url = cover
            diff = total - len(covers)
            # print(f"Printing Collage -> ({ math.trunc(((diff/total) * 100)) } %) | {diff} out of {total}")

            # Load Image
            img = Image.open(requests.get(img_url, stream=True).raw)
            #img = Image.open(img_url)
            
            #Resize image based on scale
            img.thumbnail((self.img_size, self.img_size))

            # Tilt Image if enabled
            t = self.setTilt(img)
            img = t[0]

            #Get coordinates
            location = self.setRandomImageCoords(row, col)

            if self.transparent_bg:
                 mask = Image.new("RGBA", (round(self.img_size), round(self.img_size)), color='white')
                 mask = mask.rotate(t[1], expand = True)
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
        covers = self.organzieCovers()
        collage =  self.layoutBaseGrid(collage, covers)
        
        if self.type == 'collage':
            covers = self.organzieCovers()
            collage = self.layoutCollage(collage, covers)
        
        # Save Collage and Return it?
        print(f"Save Location: {self.nameCollage()}")
        collage.save(self.nameCollage())
        return collage

g = AlbumCoverGetter()
covers = g.getTopTracks()

c = CollageMaker(covers, scale = 1, width=1000, height=1800, type = 'collage', bgColor = (255,255,255,0), tilt='rand', transparentBg=True)
c.createCollage()
