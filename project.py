import pygame
import pymunk
import pymunk.pygame_util

def create_ball(space, ball_type, x_position):
    """Creates a ball based on user input (rubber, steel, or wood)"""
    if ball_type == 1:
        mass = 1
        radius = 20
        elasticity = 0.8  # Bouncy Rubber Ball
        color = (255, 0, 0)  # Red
    elif ball_type == 2:
        mass = 3
        radius = 20
        elasticity = 0.3  # Less Bouncy Steel Ball
        color = (100, 100, 100)  # Gray
  

    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = (x_position, 50)  # Each ball starts at different x-positions
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity
    #shape.color = color
    space.add(body, shape)
    return body, shape

def create_line(space, angle):
    """Creates a rotating platform"""
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (400, 550)
    
    length = 200
    a = (-length // 2, 0)
    b = (length // 2, 0)
    
    shape = pymunk.Segment(body, a, b, 5)
    shape.elasticity = 1.0
    shape.friction = 0.8
    shape.body.angle = angle
    space.add(body, shape)
    return body, shape

def create_walls(space):
    """Creates walls to keep the balls inside the screen"""
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (0, 0), (800, 0), 5),  # Top Wall
        pymunk.Segment(static_body, (0, 600), (800, 600), 5),  # Bottom Wall
        pymunk.Segment(static_body, (0, 0), (0, 600), 5),  # Left Wall
        pymunk.Segment(static_body, (800, 0), (800, 600), 5)  # Right Wall
    ]
    
    for wall in walls:
        wall.elasticity = 1.0
        space.add(wall)

def game():
    """Main game loop"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Bouncing Balls with Different Materials")
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # User input: Choose ball types
    print("Choose three ball types:")
    print("1 - Rubber Ball (Bouncy)")
    print("2 - Steel Ball (Less Bouncy)")
    print("3 - Wooden Ball (Medium Bouncy)")
    
    ball_types = []
    for i in range(3):
        choice = int(input(f"Enter choice for ball {i+1} (1, 2, or 3): "))
        ball_types.append(choice)

    # Display countdown before starting the game
    font = pygame.font.Font(None, 50)
    screen.fill((0, 0, 0))
    text = font.render("Game Starting in 2 seconds...", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    pygame.display.flip()
    pygame.time.delay(2000)  # Wait for 2 seconds before starting

    # Create game objects
    x_positions = [300, 400, 500]  # Different starting positions for each ball
    balls = [create_ball(space, ball_types[i], x_positions[i]) for i in range(3)]
    
    if any(ball is None for ball in balls):
        print("Invalid input. Exiting game.")
        return
    
    line_body, line = create_line(space, angle=0.1)
    create_walls(space)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for ball_body, _ in balls:
                        ball_body.velocity = (ball_body.velocity.x, -700)  # Boost all balls upwards

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            line_body.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            line_body.angle += 0.05

        space.step(1 / 60)
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)

        # Game Over Condition
        for ball_body, _ in balls:
            if ball_body.position.y > 600:
                print("Game Over!")
                running = False

    pygame.quit()

if __name__ == "__main__":
    game()
