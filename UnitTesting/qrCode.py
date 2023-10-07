import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 480
screen_height = 320

# Load the QR code image
qr_image = pygame.image.load("qrCode.png")  # Replace with the actual path

qr_image = pygame.transform.rotozoom(qr_image, 0, 0.5)

# Create the Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the QR code image in the center of the screen
    qr_rect = qr_image.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(qr_image, qr_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
