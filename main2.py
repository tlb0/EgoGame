import random
import sys
import pygame

pygame.mixer.init()
pygame.font.init()
suits = ["clubs", "diamonds", "hearts", "spades"]


class Card:
    def __init__(self, value, suit, image):
        self.value = value
        self.suit = suit
        self.image = image

    def __str__(self):
        if self.value == 11:
            return f"jack_of_{self.suit}"
        elif self.value == 12:
            return f"queen_of_{self.suit}"
        elif self.value == 13:
            return f"king_of_{self.suit}"
        elif self.value == 1:
            return f"ace_of_{self.suit}"
        else:
            return f"{self.value}_of_{self.suit}"


class Pile:
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_list = []
        for card in self.cards:
            card_list.append(str(card))
        return str(card_list)

    def draw_card(self, pile):
        try:
            pile.cards.append(self.cards[-1])
            self.cards.pop()
            PLAY_CARD_SOUND.play()
        except IndexError:
            INVALID_SOUND.play()

    def draw_all_cards(self, pile):
        for card in self.cards:
            pile.cards.append(card)
            SHUFFLE_CARD_SOUND.play()
        self.cards = []

    def getimage(self, index):  # function to get image of any card
        searched_card = self.cards[index]
        return searched_card.image


class Deck(Pile):
    def create(self):
        for s in suits:
            for v in range(1, 14):
                card = Card(v, s, image=None)
                card_image = pygame.image.load(f"Assets/{str(card)}.png")
                card = Card(v, s, card_image)
                self.cards.append(card)

    def create_small(self):
        for s in suits:
            for v in range(1, 14):
                if v == 1 or v >= 6:
                    card = Card(v, s, image=None)
                    card_image = pygame.image.load(f"Assets/{str(card)}.png")
                    card = Card(v, s, card_image)
                    self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)


class Environment:
    def __init__(self):
        self.spots = []

    def add(self):
        x = 10 + (len(self.spots)) * (WIDTH_CARD + 10)
        spot = Spot(x)
        self.spots.append(spot)

    def get_spot_pile(self, index):
        try:
            searched_spot = self.spots[index]
            return searched_spot.pile
        except IndexError:
            pass

    def remove(self):
        for spot in self.spots:
            if not spot.pile.cards:
                self.spots.remove(spot)

    def check_if_movable(self, selection_index):
        try:
            if self.get_spot_pile(selection_index - 1).cards[-1].suit \
                    == self.get_spot_pile(selection_index + 1).cards[-1].suit:
                return True
            elif self.get_spot_pile(selection_index - 1).cards[-1].value \
                    == self.get_spot_pile(selection_index + 1).cards[-1].value:
                return True
            else:
                return False
        except IndexError:
            pass
        except AttributeError:
            pass


class Spot:
    def __init__(self, x):
        self.position_x = x
        self.position_y = (HEIGHT-HEIGHT_CARD)//2
        self.pile = Pile()

    def __str__(self):
        return self.pile


class Button:
    def __init__(self, b_x, b_y, b_img, hover_img, b_name):
        self.name = b_name
        self.coordinates = (b_x, b_y)
        self.image = b_img
        self.hover = hover_img
        self.rect = pygame.Rect(b_x, b_y, 233, 100)
        self.clicked = False

    def __str__(self):
        return self.name

    def draw(self):
        WIN.blit(self.image, self.coordinates)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            WIN.blit(self.hover, self.coordinates)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                print("clicked")
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


BUTTON_NAMES = ["medium", "hard", "exit"]
buttons = []
button_x = 50
for name in BUTTON_NAMES:
    button_image = pygame.image.load(f"Assets/button_{name}.png")
    hover_image = pygame.image.load(f"Assets/button_hover_{name}.png")
    button_y = 310
    button = Button(button_x, button_y, button_image, hover_image, name)
    buttons.append(button)
    button_x += 50 + button_image.get_width()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EGO GAME")

WIDTH_CARD, HEIGHT_CARD = 57, 89

GREEN = (34, 177, 76)
DARK_GREEN = (49, 135, 70)
WHITE = (255, 255, 255)
DARKER_GREEN = (31, 109, 51)

GAME_OVER = pygame.USEREVENT + 1
WINNER = pygame.USEREVENT + 2

SHUFFLE_CARD_SOUND = pygame.mixer.Sound("Assets/shuffle_card.mp3")
PLAY_CARD_SOUND = pygame.mixer.Sound("Assets/place_card.mp3")
INVALID_SOUND = pygame.mixer.Sound("Assets/invalid.mp3")
WIN_SOUND = pygame.mixer.Sound("Assets/win_sound.mp3")

TITLE = pygame.image.load("Assets/egogame_title.png")

FONT = pygame.font.SysFont("comicsans", 50)

card_selection = pygame.image.load("Assets/card_selection.png")


def draw_window(environment, selection, general_x, time, deck):
    WIN.fill(GREEN)
    for spots in environment.spots:
        spot_rect = pygame.Rect(spots.position_x + general_x, spots.position_y, WIDTH_CARD, HEIGHT_CARD)
        pygame.draw.rect(WIN, DARK_GREEN, spot_rect)
        for card in spots.pile.cards:
            WIN.blit(card.image, (spots.position_x + general_x, spots.position_y))
    WIN.blit(card_selection, (selection.x - 2 + general_x, selection.y-2))
    if len(deck.cards) > 0:
        pile = pygame.image.load(f"Assets/card_pile_{len(deck.cards)}.png.")
        WIN.blit(pile, ((WIDTH - WIDTH_CARD) // 2, HEIGHT - pile.get_height()))
    time = FONT.render("Time: " + str(time) + " seconds", True, WHITE)
    WIN.blit(time, (WIDTH - time.get_width(), HEIGHT - time.get_height()))
    cards_left = FONT.render("Cards left: " + str(len(deck.cards)), True, WHITE)
    WIN.blit(cards_left, (0, HEIGHT - time.get_height()))


def draw_titlecard():
    WIN.fill(DARKER_GREEN)
    WIN.blit(TITLE, (WIDTH//2-TITLE.get_width()//2, 50))
    for b in buttons:
        b.draw()


def check_win(deck, environment):
    keep_playing = False
    if len(deck.cards) == 0:
        if len(environment.spots) == 2:
            pygame.event.post(pygame.event.Event(WINNER))

        elif len(environment.spots) > 2:
            for index in range(0, len(environment.spots)):
                if environment.check_if_movable(index) is True:
                    return True
            if keep_playing is False:
                pygame.event.post(pygame.event.Event(GAME_OVER))


def draw_winner(time):
    WIN_SOUND.play()
    WIN.fill(DARK_GREEN)
    win = FONT.render("You win!!", True, WHITE)
    WIN.blit(win, (WIDTH // 2 - win.get_width() // 2, 100))
    draw_time = FONT.render("Time: " + str(time) + "seconds", True, WHITE)
    WIN.blit(draw_time, (WIDTH // 2 - draw_time.get_width() // 2, 300))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_game_over():
    WIN.fill(DARK_GREEN)
    draw_text = FONT.render("Game over!", True, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2,
                         HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def game(difficulty):
    environment = Environment()
    deck = Deck()
    if difficulty == "medium":
        deck.create_small()
    else:
        deck.create()
    deck.shuffle()
    clock = pygame.time.Clock()
    selection = pygame.Rect(10, (HEIGHT - HEIGHT_CARD) // 2, WIDTH_CARD, HEIGHT_CARD)
    selection_index = 0
    general_x = 0
    play_game = True
    while play_game:
        clock.tick(60)
        time = pygame.time.get_ticks() // 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == WINNER:
                draw_winner(time)
                play_game = False
            if event.type == GAME_OVER:
                draw_game_over()
                play_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    environment.add()
                    deck.draw_card(environment.get_spot_pile(-1))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selection.x -= (WIDTH_CARD + 10)
                    selection_index -= 1
                if event.key == pygame.K_RIGHT:
                    selection.x += (WIDTH_CARD + 10)
                    selection_index += 1
                if event.key == pygame.K_SPACE:
                    if environment.check_if_movable(selection_index) is True:
                        for q in range(selection_index, len(environment.spots)):
                            pile = environment.get_spot_pile(q)
                            pile.draw_all_cards(environment.get_spot_pile(q - 1))
                        environment.remove()
                    else:
                        INVALID_SOUND.play()
                if event.key == pygame.K_DOWN and general_x < 0:  # moves to the left
                    general_x += (10 + WIDTH_CARD)
                    selection.x -= (WIDTH_CARD + 10)
                    selection_index -= 1
                try:
                    if event.key == pygame.K_UP and environment.spots[-1].position_x \
                            + general_x >= 50:  # moves to the right
                        general_x -= (10 + WIDTH_CARD)
                        selection.x += (WIDTH_CARD + 10)
                        selection_index += 1
                except IndexError:
                    pass
                if event.key == pygame.K_RETURN:
                    for q in range(selection_index, len(environment.spots)):
                        pile = environment.get_spot_pile(q)
                        pile.draw_all_cards(environment.get_spot_pile(q - 1))
                    environment.remove()
        draw_window(environment, selection, general_x, time, deck)
        check_win(deck, environment)

        pygame.display.update()
    main()


def main():
    run = True
    while run:
        buttons[0].clicked = False
        buttons[1].clicked = False
        draw_titlecard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if buttons[0].clicked is True:
            game("medium")
        if buttons[1].clicked is True:
            game("hard")
        if buttons[2].clicked is True:
            pygame.quit()
            sys.exit()
        draw_titlecard()
        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
