import pygame
from time import sleep

class Display:
    
    def __init__(self, colors, images, imageSize, imagePositions, textSize, textFont, borderWidth):

        self.colors = colors
        self.imageSize = imageSize
        self.textSize = textSize
        self.textFont = textFont
        self.borderWidth = borderWidth
        self.imagePositions = imagePositions

        #Initialize pygame
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

        #Load images and scale them to fit the specified size
        self.images = {}
        for image in images:
            originalImage = pygame.image.load(images[image]['path'])
            originalWidth, originalHeight = originalImage.get_size()
            widthScale = imageSize / originalWidth
            heightScale = imageSize / originalHeight
            scale_factor = min(widthScale, heightScale)
            new_width = int(originalWidth * scale_factor)
            new_height = int(originalHeight * scale_factor)
            scaledImage = pygame.transform.scale(originalImage, (new_width, new_height))
            imagePosition = imagePositions[images[image]['type']]
            self.images.update({
                image : {
                    'figure' : scaledImage, 
                    'position' : imagePosition, 
                    'path' : images[image]['path'], 
                    'type' : images[image]['type']
                }
            })

    #Update one single image
    def updateImage(self, image):
        imageInfo = self.images[image]
        path = imageInfo['path']
        originalImage = pygame.image.load(path)
        originalWidth, originalHeight = originalImage.get_size()
        widthScale = self.imageSize / originalWidth
        heightScale = self.imageSize / originalHeight
        scale_factor = min(widthScale, heightScale)
        new_width = int(originalWidth * scale_factor)
        new_height = int(originalHeight * scale_factor)
        scaledImage = pygame.transform.scale(originalImage, (new_width, new_height))
        imageInfo.update('figure', scaledImage)
        self.images.update({image : imageInfo})

    #Display a text breaking lines
    def displayText(surface, text, pos, font, color):
        collection = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        x,y = pos
        for lines in collection:
            for words in lines:
                word_surface = font.render(words, True, color)
                word_width , word_height = word_surface.get_size()
                if x + word_width >= 800:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x,y))
                x += word_width + space
            x = pos[0]
            y += word_height
    
    def displayTextCentered(self, surface, text, font, color):
        lines = text.splitlines()
        
        screen_width, screen_height = surface.get_size()

        total_text_height = sum([font.size(line)[1] for line in lines])
        y = (screen_height - total_text_height) // 2

        for line in lines:
            words = line.split()
            
            total_word_width = sum([font.size(word)[0] for word in words])
            space_width = font.size(' ')[0]
            
            x = (screen_width - total_word_width - (len(words) - 1) * space_width) // 2
            
            for word in words:
                word_surface = font.render(word, True, color)
                surface.blit(word_surface, (x, y))
                x += word_surface.get_width() + space_width

            y += font.size(line)[1]

    def displayContent(self, type, message, images):
        font = pygame.font.Font(self.textFont, self.textSize)
        background_color = self.colors['Background']
        border_color = self.colors[type]
        border_thickness = self.borderWidth
        self.screen.fill(background_color)
        pygame.draw.rect(self.screen, border_color, (0, 0, self.screen_width, self.screen_height), border_thickness)
        counter = {'Gesture' : 0, 'Candy' : 0, 'Icon' : 0}
        for image in images:
            offset = self.imageSize*counter[self.images[image]['type']] + 10
            self.screen.blit(self.images[image]['figure'], (self.images[image]['position'][0] - offset, self.images[image]['position'][1]))
            counter.update({self.images[image]['type'] : counter[self.images[image]['type']]+1})
        self.displayTextCentered(self.screen, message, font, self.colors['Text'])
        pygame.display.flip()