import os
from creds import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from PIL import Image
import random
import requests
from datetime import datetime

IMG_HEIGHT = 640


class CollageMaker:

    def __init__(self, covers, width = 1080, height = 1080, scale = 2, type = 'grid', tilt = False):
        self.collage_height = height
        self.collage_width = width
        self.cover_list = covers
        self.type = type
        self.scale = 1 if type == 'collage' else scale
        self.tilt = tilt
        self.img_size = self.scaleDimensions()
    
    def scaleDimensions(self):
        # Use GCF to determine scale factor
        h, w = self.collage_height, self.collage_width
        if h > w:
            h, w = w, h
        for x in range(IMG_HEIGHT, 0, -1):
            if h % x == 0 and w % x == 0:
                return int(x / self.scale)

    """
    Takes the covers and populates a matrix where [row][col] = image link 
    Write a new cover assignment function if I want frequency data
    """
    def organzieCovers(self):
        # Calculate number of rows and columns based on image size
        img_size = self.scaleDimensions()
        n_rows = int(self.collage_width / img_size)
        n_ols = int(self.collage_height / img_size)

        # Generate Grid
        unused = set(self.cover_list)
        used = set()
        grid = []
        #Iterate through grid and place covers, reseting when covers run out 
        for row in range(n_rows):
            grid.append([])
            for col in range(n_rows):
                # Check if unused is empty and reset the sets if so
                if len(unused) == 0:
                    unused = used
                    used.clear()

                # Take a cover and add it to the grid
                cover = unused.pop()
                grid[row].append(cover)
                used.add(cover)
         
        return grid

    def nameCollage(self):
        return 'collages/collage' + str(self.collage_width) + 'x' + str(self.collage_height) +"_"+ str(datetime.now().strftime(
            '%d-%m-%Y-%H-%M-%S')) + '.png'
    
    def setImageCoord(self,s, a):
        if self.type == 'grid':
            return a * self.img_size

    def createCollage(self):        
        picture = Image.new('RGB', (self.collage_width, self.collage_height))
        grid = self.organzieCovers()

        for row,i in enumerate(grid):
            for col,j in enumerate(grid):
                img_url = grid[i][j] 
                img = Image.open(requests.get(img_url, stream=True).raw)
                img.thumbnail((self.img_size, self.img_size))

                x_coord = self.setImageCoord('x',i)
                y_coord = self.setImageCoord('y', j)
                
                picture.paste(img, (x_coord,y_coord))
