import pygame
import os
from OpenGL.GL import *
from PIL import Image


class Texture(object):
    def __init__(self, fileName=None, properties={}):
        #pygame surface object for storing pixel data;
        #can load from image or manipulation directly
        self.surface = None

        #reference of available texture from GPU
        self.textureRef = glGenTextures(1)

        #default property values
        self.properties = {
            "magFilter":GL_LINEAR,
            "minFilter":GL_LINEAR_MIPMAP_LINEAR,
            "wrap":GL_REPEAT
        }
        
        #Overwrite default property values
        self.setProperties(properties)

        if fileName is not None:
            self.loadImage(fileName)
            self.uploadData()

        
    #load image from file
    def loadImage(self, fileName):
        # Cek apakah file ada
        if not os.path.exists(fileName):
            print(f"WARNING: Texture file not found: {fileName}")
            print(f"Creating default texture...")
            # Buat texture default (checkerboard pattern)
            self.surface = pygame.Surface((64, 64))
            for y in range(64):
                for x in range(64):
                    color = (255, 255, 255) if (x//8 + y//8) % 2 == 0 else (200, 200, 200)
                    self.surface.set_at((x, y), color)
            return
        
        try:
            # Try loading with pygame first
            self.surface = pygame.image.load(fileName)
            print(f"Successfully loaded texture: {fileName}")
        except pygame.error as e:
            # If pygame fails, try PIL (Pillow) as fallback
            try:
                print(f"Pygame failed, trying PIL for {fileName}...")
                pil_image = Image.open(fileName)
                # Convert to RGBA mode if not already
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                # Convert PIL image to pygame surface
                image_data = pil_image.tobytes()
                self.surface = pygame.image.fromstring(image_data, pil_image.size, 'RGBA')
                print(f"Successfully loaded texture with PIL: {fileName}")
            except Exception as pil_error:
                print(f"ERROR loading texture {fileName}: {e}")
                print(f"PIL also failed: {pil_error}")
                print(f"Creating default texture...")
                # Buat texture default
                self.surface = pygame.Surface((64, 64))
                for y in range(64):
                    for x in range(64):
                        color = (255, 0, 255) if (x//8 + y//8) % 2 == 0 else (200, 0, 200)
                        self.surface.set_at((x, y), color)


    
    #set property values
    def setProperties(self, props):
        for name, data in props.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else: #unkown property type
                raise Exception("Texture has no property: " + name)
    
    #upload pixel data to GPU
    def uploadData(self):
        #store image dimensions
        width = self.surface.get_width()
        height = self.surface.get_height()

    
        #convert image data to string buffer
        pixelData = pygame.image.tostring(self.surface, "RGBA", 1)

        #specify texture used by the following functions
        glBindTexture(GL_TEXTURE_2D, self.textureRef)

        #send pixel data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
                    width, height, 0, GL_RGBA, 
                    GL_UNSIGNED_BYTE, pixelData)

        #Generate mipmap image from uploaded pixel data
        glGenerateMipmap(GL_TEXTURE_2D)

        #specify technique for magnifying/minifying textures
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties["minFilter"])

        #specify what happens to texture coordinates outside range[0,1]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.properties["wrap"])


        #set default border color to white; 
        #important for rendering shadaws
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1,1,1,1])
