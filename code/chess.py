import os
import sys

import pygame

from controller.game_controller import GameController

class Menu:
    """
    Handles the game menu system including main menu and options.
    """
    def draw_text(self, text, font, color, surface, x, y):
        """
        Utility method to render text on a surface.
        
        Args:
            text: The text to display
            font: The font to use
            color: RGB color tuple
            surface: The surface to draw on
            x, y: Top-left position coordinates
        """
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        """
        Displays the main menu with play and options buttons.
        Handles user interaction with the menu.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'  # Position window at top-left
        mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Chess Game')
        screen = pygame.display.set_mode((600, 300), 0, 32)
        font = pygame.font.SysFont(None, 30)

        while True:
            screen.fill((60, 80, 60))  # Background color
            mx, my = pygame.mouse.get_pos()  # Get mouse position
            
            # Define button rectangles
            button_1 = pygame.Rect(200, 100, 200, 50)  # Play button
            button_2 = pygame.Rect(200, 180, 200, 50)  # Options button

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if play button is clicked
            if button_1.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                game_controller = GameController()
                game_controller.run()  # Start the game

            # Check if options button is clicked
            if button_2.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                self.options(screen, mainClock, font)  # Open options menu

            # Draw buttons and their text
            pygame.draw.rect(screen, (200, 0, 0), button_1)
            pygame.draw.rect(screen, (200, 0, 0), button_2)
            self.draw_text('PLAY', font, (255, 255, 255), screen, 270, 115)
            self.draw_text('OPTIONS', font, (255, 255, 255), screen, 250, 195)

            pygame.display.update()
            mainClock.tick(60)  # Cap at 60 FPS

    def options(self, screen, mainClock, font):
        """
        Displays the options menu.
        
        Args:
            screen: The pygame display surface
            mainClock: The game clock
            font: The font to use for text
        """
        pygame.display.set_caption('Options')
        running = True

        while running:
            screen.fill((60, 80, 60))  # Background color
            self.draw_text('Options Menu', font, (255, 255, 255), screen, 20, 20)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False  # Return to main menu

            pygame.display.update()
            mainClock.tick(60)  # Cap at 60 FPS



# Start the game when the script is run directly
if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()