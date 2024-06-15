import pygame
from simpleGE import Game, GameState

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swift Adventure: Trivia Quiz")

# Colors
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Load background image (replace with your actual image path)
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sprite images (replace with your actual image paths)
question_sprite = pygame.image.load("question_sprite.png")
print("Question sprite loaded:", question_sprite)

option_sprite = pygame.image.load("option_sprite.png")
print("Option sprite loaded:", option_sprite)

# Load sounds (replace with your actual sound file paths)
correct_sound = pygame.mixer.Sound("correct_answer.wav")
wrong_sound = pygame.mixer.Sound("wrong_answer.wav")

# Questions and answers (placeholder)
questions = {
    "Debut Era": [
        {"question": '''What year was Taylor Swift's debut album released?
Type either 1,2 or 3 and hit enter''', "options": ["2004", "2006", "2008"], "answer": "2006"},
        {"question": "Which song was Taylor Swift's first single?", "options": ["Tim McGraw", "Love Story", "You Belong with Me"], "answer": "Tim McGraw"},
    ],
    "Fearless Era": [
        {"question": "Which song won Taylor Swift her first Grammy?", "options": ["Love Story", "White Horse", "You Belong with Me"], "answer": "White Horse"},
        {"question": "What year was the album 'Fearless' released?", "options": ["2006", "2008", "2010"], "answer": "2008"},
    ],
    "Red Era": [
        {"question": "Which song from the 'Red' album features Ed Sheeran?", "options": ["Red", "Everything Has Changed", "I Knew You Were Trouble"], "answer": "Everything Has Changed"},
        {"question": "What year was the album 'Red' released?", "options": ["2010", "2012", "2014"], "answer": "2012"},
    ],
    "Lover Era": [
        {"question": "Which song from the 'Lover' album features Brendon Urie?", "options": ["ME!", "You Need to Calm Down", "Lover"], "answer": "ME!"},
        {"question": "What year was the album 'Lover' released?", "options": ["2017", "2018", "2019"], "answer": "2019"},
    ],
}
class TriviaGame(GameState):
    def __init__(self, game, era):
        super().__init__(game)
        self.era = era
        self.questions = questions[era]
        self.current_question = 0
        self.score = 0
        self.selected_option = -1
        self.correct_answers = []

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_option = 0
            elif event.key == pygame.K_2:
                self.selected_option = 1
            elif event.key == pygame.K_3:
                self.selected_option = 2
            elif event.key == pygame.K_RETURN and self.selected_option != -1:
                self.check_answer()

    def check_answer(self):
        if self.questions[self.current_question]["options"][self.selected_option] == self.questions[self.current_question]["answer"]:
            self.score += 1
            self.correct_answers.append((self.current_question, True))
            correct_sound.play()  # Play correct answer sound
        else:
            self.correct_answers.append((self.current_question, False))
            wrong_sound.play()  # Play wrong answer sound
        self.current_question += 1
        self.selected_option = -1
        if self.current_question >= len(self.questions):
            self.game.change_state(ScoreScreen(self.game, self.era, self.score, self.correct_answers, self.questions))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(WHITE)
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]["question"]
            question_text = font.render(question, True, BLACK)
            surface.blit(question_text, (50, 50))

            options = self.questions[self.current_question]["options"]
            for i, option in enumerate(options):
                option_text = font.render(f"{i + 1}. {option}", True, BLACK)
                surface.blit(option_text, (50, 150 + i * 50))
                if self.selected_option == i:
                    pygame.draw.rect(surface, RED, (40, 150 + i * 50, 5, 30))  # Highlight selected option

        else:
            surface.blit(font.render("Loading next question...", True, BLACK), (50, 50))

class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_state(LevelSelection(self.game))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(background_image, (0, 0))
        title_text = font.render("Swift Adventure: Trivia Quiz", True, BLACK)
        start_text = font.render("[Press Enter to Start]", True, BLACK)
        surface.blit(title_text, (100, 100))
        surface.blit(start_text, (100, 200))

class LevelSelection(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.eras = list(questions.keys())
        self.selected_era = 0

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_era = (self.selected_era - 1) % len(self.eras)
            elif event.key == pygame.K_DOWN:
                self.selected_era = (self.selected_era + 1) % len(self.eras)
            elif event.key == pygame.K_RETURN:
                self.game.change_state(TriviaGame(self.game, self.eras[self.selected_era]))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(background_image, (0, 0))
        select_text = font.render("Select an Era:Use Arrows to choose your era & Press Enter", True, BLACK)
        surface.blit(select_text, (100, 100))
        for i, era in enumerate(self.eras):
            era_text = font.render(era, True, BLACK if i != self.selected_era else RED)
            surface.blit(era_text, (100, 200 + i * 40))

class ScoreScreen(GameState):
    def __init__(self, game, era, score, correct_answers, questions):
        super().__init__(game)
        self.era = era
        self.score = score
        self.correct_answers = correct_answers
        self.questions = questions

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_state(LevelSelection(self.game))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(WHITE)
        score_text = font.render(f"You scored {self.score} points in the {self.era} era!", True, BLACK)
        surface.blit(score_text, (100, 100))
        for i, (question_index, correct) in enumerate(self.correct_answers):
            question = self.questions[question_index]["question"]
            answer = self.questions[question_index]["answer"]
            correctness = "Correct" if correct else "Incorrect"
            answer_text = font.render(f"Q: {question} - A: {answer} ({correctness})", True, BLACK)
            surface.blit(answer_text, (100, 200 + i * 40))
        replay_text = font.render("Press Enter to select another era", True, BLACK)
        surface.blit(replay_text, (100, 400 + len(self.correct_answers) * 40))

class SwiftAdventure:
    def __init__(self):
        self.game = Game(screen)
        self.game.change_state(Menu(self.game))

    def run(self):
        self.game.run()

if __name__ == "__main__":
    game = SwiftAdventure()
    game.run()
