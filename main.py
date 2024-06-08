import pygame as pg
from AMR import Amr
from assets import LIGHT_GREY, WIN

# Set the window title
pg.display.set_caption("AMR simulation")
# Set the frames per second for the game loop
FPS = 60

def draw_simulation(*objects):
    """
    This function draws all the objects on the screen.
    It first clears the screen, then calls the draw method on each object.
    Finally, it updates the display to show the new frame.

    Args:
        *objects: A variable number of objects that have a draw method.
    """
    # Fill the screen with a light grey color
    WIN.fill(LIGHT_GREY)
    # Draw each object
    for obj in objects:
        obj.draw()
    # Update the display
    pg.display.update()

def handle_events():
    """
    This function handles all the events from the pygame event queue.
    It returns a tuple containing a boolean indicating whether the game should continue running,
    and the positions of the mouse when the left button was pressed and released.

    Returns:
        tuple: A tuple containing a boolean and two position tuples.
    """
    # Initialize the mouse positions to None
    mouse_down = mouse_up = None
    # Process all events
    for event in pg.event.get():
        # If the event is a QUIT event, return False and the mouse positions
        if event.type == pg.QUIT:
            return False, mouse_down, mouse_up
        # If the event is a mouse button event and the left button was pressed or released
        elif event.type in {pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP} and event.button == 1:
            # If the left button was pressed, store the position
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = event.pos
            # If the left button was released, store the position
            else:
                mouse_up = event.pos
    # Return True and the mouse positions
    return True, mouse_down, mouse_up

def main():
    """
    This is the main function of the game.
    It initializes pygame, creates an instance of the Amr class, and enters the game loop.
    In the game loop, it handles events, updates the game state, and draws the new frame.
    When the game loop ends, it quits pygame.
    """
    # Initialize pygame
    pg.init()
    # Create a clock to control the frame rate
    clock = pg.time.Clock()
    # Create an instance of the Amr class
    amr = Amr()

    # Set the run flag to True
    run = True
    # Enter the game loop
    while run:
        # Limit the frame rate
        clock.tick(FPS)
        # Handle events and get the mouse positions
        run, mouse_down, mouse_up = handle_events()
        # Get the state of all keys
        keys = pg.key.get_pressed()
        # Handle the movement of the AMR
        amr.handle_movement(keys, mouse_down)
        # Handle the obstacles on the map
        amr.map.handle_obstacles(mouse_down, mouse_up)
        # Draw the new frame
        draw_simulation(amr.map, amr.interface, amr)

    # Quit pygame
    pg.quit()

# If this file is the main module, run the main function
if __name__ == "__main__":
    main()