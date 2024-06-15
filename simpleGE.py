import pygame

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = None

    def change_state(self, state):
        self.state = state

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Limit to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state:
                    self.state.handle_event(event)
            if self.state:
                self.state.update(dt)
                self.state.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
