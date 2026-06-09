import random
import pygame
from pygame import mixer

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "🥝": 2,
    "🍇": 4,
    "🍊": 6,
    "🍉": 8
}

symbol_value = {
    "🥝": 5,
    "🍇": 4,
    "🍊": 3,
    "🍉": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break 
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
            mixer.init()
            mixer.music.load("jackpot.mp3")
            mixer.music.set_volume(2)
            mixer.music.play()
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []

    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]

        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns):

    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        amount = input("How much would you like to deposit? ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else: 
                print("Invalid amount! Please enter a value greater than 0.")
        else:
            print("Please enter a valid number!")
    
    return amount

def get_number_of_lines():
    while True:
        lines = input("How many lines do you want to play (1-"+ str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else: 
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number!")
    
    return lines

def get_bet():
    while True:
        amount = input("How much do you want to bet on each line? $ ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else: 
                print(f"Amount must be between {MIN_BET} - {MAX_BET}.")
        else:
            print("Please enter a valid number!")
    
    return amount

def spin(balance, lines, bet, slots):

    # while True:

        #total_bet = bet * lines

        # the reason the app cashes when we have not enough funds is because,
        # the game runs at x fps about 60 IDK, to it prints 60 times a second to the
        # terminal, which results in a crash.
        # let's just comment this out, and check it when we click the spin button

        #if total_bet > balance:
        #   print(f"Not enough funds. Current balance: ${balance}")
        #else:
        #    break

    total_bet = bet * lines

    print(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}")
    # slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}!")
    print(f"You won on lines: ", *winning_lines)

    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break

        balance += spin(balance)

    print(f"you left with ${balance}")

def screen():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    # printed_slot_grid = print_slot_machine(slots);

    current_bet = 10
    current_balance = 1000

    line_1_value = 1
    line_2_value = 2
    line_3_value = 3

    # this won't work and throw will throw an error
    # selected_line_box_value = None

    selected_line_box_value = 1

    # 1. check events
    # 2. clear screen
    # 3. draw symbols
    # 4. draw buttons
    # 5. update screen

    winnings = 0
    winning_lines = []

    info_message = ""

    kiwi_img = pygame.image.load("symbols/kiwi.png")
    grape_img = pygame.image.load("symbols/grapes.png")
    orange_img = pygame.image.load("symbols/orange.png")
    watermelon_img = pygame.image.load("symbols/watermelon.png")

    symbol_images = {
        "🥝": kiwi_img,
        "🍇": grape_img,
        "🍊": orange_img,
        "🍉": watermelon_img
    }

    # total_bet = current_bet * selected_line_box_value;

    while running:

        total_bet = current_bet * selected_line_box_value;

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if spin_button.collidepoint(event.pos):

                    if winnings == 0:
                        mixer.music.load("gunshot.mp3")
                        mixer.music.set_volume(2)
                        mixer.music.play()
                    if current_bet > current_balance:
                        info_message = "you dont have enough money to bet"
                        mixer.music.load("no_money.mp3")
                        mixer.music.set_volume(2)
                        mixer.music.play()
                    if total_bet > current_balance:
                    # if current_bet * selected_line_box_value > current_balance:
                        info_message = "you don't have enough money to bet, sorry!"
                        # print(total_bet)
                    else:
                        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
                        winnings, winning_lines = check_winnings(slots, selected_line_box_value, current_bet, symbol_value)
                        current_balance += spin(current_balance, selected_line_box_value, current_bet, slots)


                if bet_up_button.collidepoint(event.pos):
                    if current_bet >= 100:
                        info_message = "max bet is 100"
                        print("max bet is 100")
                    else:
                        current_bet += 10
                        info_message = ""

                if bet_down_button.collidepoint(event.pos):
                    if current_bet > 10:
                        current_bet -= 10
                    else:
                        info_message = "minimum bet is 10"
                        print("you cannot bet under 0 or negative")
                        break
                if line_1.collidepoint(event.pos):
                    selected_line_box_value = 1
                elif line_2.collidepoint(event.pos):
                    selected_line_box_value = 2
                elif line_3.collidepoint(event.pos):
                    selected_line_box_value = 3

        screen.fill("red")

        size = (50, 50)
        kiwi_img = pygame.transform.scale(kiwi_img, size)
        grape_img = pygame.transform.scale(grape_img, size)
        orange_img = pygame.transform.scale(orange_img, size)
        watermelon_img = pygame.transform.scale(watermelon_img, size)

        text_font = pygame.font.SysFont("Arial", 64)
        text = text_font.render("Slot Machine", True, "white")
        screen.blit(text, (500, 100))

        spin_button = pygame.Rect(840, 600, 200, 60)
        bet_box = pygame.Rect(840, 400, 300, 60)

        balance_box = pygame.Rect(100, 200, 100, 50)

        bet_up_button = pygame.Rect(840, 115, 200, 60)
        bet_down_button = pygame.Rect(840, 215, 300, 60)

        line_1 = pygame.Rect(100,300, 50, 50)
        line_2 = pygame.Rect(100,400, 50, 50)
        line_3 = pygame.Rect(100,500, 50, 50)

        line_value_box = pygame.Rect(900, 30, 70,70)

        won_on_line_box = pygame.Rect(50, 100, 300, 55)
        won_amount_box = pygame.Rect(50, 20, 300, 55)

        # printed_slot_grid_box = pygame.Rect(100,100, 1000, 1000)

        info_box = pygame.Rect(50, 600, 300, 80)

        symbol_font = pygame.font.SysFont("Segoe UI Emoji", 64)
        for col_index, column in enumerate(slots):
            for row_index, symbol in enumerate(column):
                img = symbol_images[symbol]
                x = 400 + col_index * 150
                y = 250 + row_index * 150
                screen.blit(img, (x, y))

                pygame.draw.rect(screen, "green", spin_button)
                font_button = pygame.font.SysFont("Arial", 36)
                button_text = font_button.render("SPIN", True, "white")
                screen.blit(button_text, (890, 615))

                pygame.draw.rect(screen, "blue", bet_box)
                font_bet_box = pygame.font.SysFont("Arial", 36)
                bet_box_text = font_bet_box.render(str(current_bet), True, "white")
                screen.blit(bet_box_text, (890, 415))

                pygame.draw.rect(screen, "yellow", bet_up_button)
                font_bet_up_button = pygame.font.SysFont("Arial", 36)
                bet_up_button_text = font_bet_up_button.render("UP", True, "black")
                screen.blit(bet_up_button_text, (890, 115))

                pygame.draw.rect(screen, "yellow", bet_down_button)
                font_bet_down_button = pygame.font.SysFont("Arial", 36)
                bet_down_button_text = font_bet_down_button.render("DOWN", True, "black")
                screen.blit(bet_down_button_text, (890, 215))

                pygame.draw.rect(screen, "aqua", balance_box)
                font_balance_box = pygame.font.SysFont("Arial", 36)
                balance_box_text = font_balance_box.render(str(current_balance), True, "black")
                screen.blit(balance_box_text, (100, 200))

                pygame.draw.rect(screen, "purple", line_1)
                font_line_1 = pygame.font.SysFont("Arial", 36)
                line_1_text = font_line_1.render(str(line_1_value), True, "white")
                screen.blit(line_1_text, (100, 300))

                pygame.draw.rect(screen, "purple", line_2)
                font_line_2 = pygame.font.SysFont("Arial", 36)
                line_2_text = font_line_2.render(str(line_2_value), True, "white")
                screen.blit(line_2_text, (100, 400))

                pygame.draw.rect(screen, "purple", line_3)
                font_line_3 = pygame.font.SysFont("Arial", 36)
                line_3_text = font_line_3.render(str(line_3_value), True, "white")
                screen.blit(line_3_text, (100, 500))

                pygame.draw.rect(screen, "purple", line_value_box)
                font_line_value_box = pygame.font.SysFont("Arial", 36)
                line_value_box_text = font_line_value_box.render(str(selected_line_box_value), True, "white")
                screen.blit(line_value_box_text, (900, 50))

                pygame.draw.rect(screen, "brown", won_amount_box)
                font_won_amount_box = pygame.font.SysFont("Arial", 36)
                won_amount_box_text = font_won_amount_box.render(f"Won: ${winnings}", True, "white")
                screen.blit(won_amount_box_text, (50, 20))

                pygame.draw.rect(screen, "brown", won_on_line_box)
                font_won_on_line_box = pygame.font.SysFont("Arial", 36)
                won_on_line_text = font_won_on_line_box.render(f"Winning Lines: ${winning_lines}", True, "white")
                screen.blit(won_on_line_text, (50, 100))

                pygame.draw.rect(screen, "white", info_box)
                font_info_box = pygame.font.SysFont("Arial", 36)
                info_box_text = font_info_box.render(info_message, True, "black")
                screen.blit(info_box_text, (50, 600))

                # pygame.draw.rect(screen, "black", printed_slot_grid_box)
                # font_slot_grid_box = pygame.font.SysFont("Segoe UI Emoji", 36)
                # slot_grid_box_value = font_slot_grid_box.render(printed_slot_grid, True, "white")
                # screen.blit(slot_grid_box_value, (1000, 1000))

                # this shit was the reason the GUI and CLI dont match
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if spin_button.collidepoint(event.pos):
                #         slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

                # check_winnings(slots, selected_line_box_value, current_bet, symbol_value)
                # current_balance += spin(current_balance, selected_line_box_value, current_bet)

        pygame.display.flip()

        clock.tick(60)
    pygame.quit()

# main()
screen()
