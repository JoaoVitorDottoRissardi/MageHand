import pygame
import sys

"""
Class for handling the display functions

Attributes
----------

colors: dict
    dictionary of colors the display should use. It should follow this format:
        'colors' : {
            'Alert' : (255,0,0),
            'Info' : (0,0,255),
            'Confirm' : (0,255,0),
            'Text' : (0,0,0),
            'Background' : (255,255,255)
 	    }

images: dict
    dictionary of images the display should render. It should follow this format:
        'images' : {
            'Info' : {
                'type' : 'Icon',
                'path' : './images/info.png'
            },
            'ThumbsUp' : {
                'type' : 'Gesture',
                'path' : './images/thumbs_up.png'
            },
            'Candy1' : {
                'type' : 'Candy',
                'path' : './images/mms.jpg'
            },
        }

imageSize: int
    value that will be the maximum size a dimension of a image could have in absolute pixels

imagePositions: dict
    dictionary containg the positions each type of image should be rendered when requested, like this:
        'imagePositions' : {
            'Icon' : (30,30),
            'Candy' : (375, 30),
            'Gesture' : (375, 215)
        },  

textSize: int
    the size the text will assume in absolute pixels

textFont: Font
    font that the text will be displayed

borderWidth: int
    width of the border the display will always render in absolute pixels      

"""

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
        self.screen_width = 480
        self.screen_height = 320
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        #self.screen_width = 480 if "--test" in sys.argv else self.screen_info.current_w
        #self.screen_height = 320 if "--test" in sys.argv else self.screen_info.current_h
        #self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE if "--test" in sys.argv else pygame.FULLSCREEN)

        #Load images and scale them to fit the specified size
        self.images = {}
        for image in images:
            #print(images[image]['path'])
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

    """
        Function to update on single image

        Parameters
        ----------
        image : str
             name of the image the sould be reloaded.
        
        obs : this functions consider the path of the image to be reloaded didn't change, only the image

    """

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
        imageInfo['figure'] = scaledImage
        self.images.update({image : imageInfo})

    """
        Function to display a text left justified breaking lines

        Parameters
        ----------
        surface : Surface
             surface in which the text will be displayed, usually self.screen
        
        text : str
             text to be displayed, the line break point should be specified using '\n' inside the text

        pos : tuple (int, int)
             top left corner the text will be rendered in absolute pixels
        
        font: Font
             font in which the text will be displayed, usually self.font
        
        color: tuple RGB
             color in which the text will be displayed, usually self.color

    """
        
    def displayText(self, surface, text, pos, font, color):
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
    
    """
        Function to display a text centered on screen while breaking lines

        Parameters
        ----------
        surface : Surface
             surface in which the text will be displayed, usually self.screen
        
        text : str
             text to be displayed, the line break point should be specified using '\n' inside the text
        
        font: Font
             font in which the text will be displayed, usually self.font
        
        color: tuple RGB
             color in which the text will be displayed, usually self.color

    """


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

    """
        Function to display a certain pre-defined content

        Parameters
        ----------
        type : str
             string the indicate the type of content that should be displayed. For now it must be
             either 'Alert', 'Info' our 'Confirm'. Other types may be added.
        
        message : str
             message to be displayed in the 'type' context. This message must contain '\n' inside
             it when it should break lines.

        images : list[str]
             images that sould be displayed along with the text. Theses images must be along the ones
             loaded during constructor and therefore should have the same names.

    """

    def displayContent(self, type, message, images, pos=False):
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
        if pos:
            self.displayText(self.screen, message, pos, font, self.colors['Text'])
        else:
            self.displayTextCentered(self.screen, message, font, self.colors['Text'])
        pygame.display.flip()

        
    def showImage(self, image, make_surface=True, pos=(0, 0), clear=True):
        if clear:
            background_color = self.colors['Background']
            self.screen.fill(background_color)
        
        if make_surface:
            self.screen.blit(pygame.surfarray.make_surface(image), pos)
        else:
            self.screen.blit(image, pos)
        pygame.display.flip()
