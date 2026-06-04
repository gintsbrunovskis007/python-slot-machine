import random
# import pygame

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

# How many times each symbol appears in the pool.
symbol_count = {
    "🍒": 2,
    "🍇": 4,
    "🍊": 6,
    "🍌": 8
}

# Payout multiplier per symbol.
symbol_value = {
    "🍒": 5,
    "🍇": 4,
    "🍊": 3,
    "🍌": 2
}

# Col 0   Col 1   Col 2
# Row 0:    🍒  |   🍒  |   🍒    ← Line 1 (all match = WIN)
# Row 1:    🍇  |   🍊  |   🍇    ← Line 2 (no match = LOSE)
# Row 2:    🍌  |   🍌  |   🍊    ← Line 3 (not betting on this)


# columns = [
#     ["🍒", "🍇", "🍌"],   # column 0 (left)
#     ["🍒", "🍊", "🍌"],   # column 1 (middle)
#     ["🍒", "🍇", "🍌"]    # column 2 (right)
# ]
# lines = 2 | checking row 0 and row 1 only.
# bet = 10 | $10 per line
# values = {"🍒": 5, "🍇": 4, "🍊": 3, "🍌": 2}
def check_winnings(columns, lines, bet, values):
    winnings = 0

    # Stores the winning lines, for example won on 1,2,3.
    # The reason it is not 0,1,2 because nobody counts from 0, so line + 1.
    winning_lines = []

    # Line is basically just saying "which row am I currently checking?"
    # If line = 3 then we check line's 0,1,2.
    for line in range(lines):

        # columns[0] is the left column (vertical strip):
        # 🍒   ← columns[0][0]
        # 🍇   ← columns[0][1]
        # 🍌   ← columns[0][2]
        # columns[0][line] is grabbing the symbol from the left column at the row we are currently checking.
        symbol = columns[0][line]
        # If line = 0: symbol = columns[0][0]  →  🍒, etc.

        # We are currently on row 0 (line = 0) and we already grabbed our reference symbol: symbol = 🍒 from the left column.

        # Slot machine look like:
        # 🍒 | 🍒 | 🍒   ← We are checking this row.
        # 🍇 | 🍊 | 🍇
        # 🍌 | 🍌 | 🍌

        # This loops through each column one by one:
        # first loop:  column = ["🍒", "🍇", "🍌"]  (left column)
        # second loop: column = ["🍒", "🍊", "🍌"]  (middle column)
        # third loop:  column = ["🍒", "🍇", "🍌"]  (right column)
        for column in columns:

            # Grabs the symbol from the current column at row 0:
            # first loop:  symbol_to_check = 🍒
            # second loop: symbol_to_check = 🍒
            # third loop:  symbol_to_check = 🍒
            symbol_to_check = column[line]

            # Compares reference symbol against current symbol:
            # 🍒 != 🍒? → No  → keep going ✅
            # 🍒 != 🍒? → No  → keep going ✅
            # 🍒 != 🍒? → No  → keep going ✅

            # Losing row 1:
            # symbol = 🍇  (reference from left column)
            # 🍇 != 🍇? → No  → keep going ✅
            # 🍇 != 🍊? → YES → BREAK! ❌
            if symbol != symbol_to_check:
                break 
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)


    
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):

    # Stores the pool of symbols before we randomly pick.
    # all_symbols = [
    #     "🍒", "🍒",  # 2 times
    #     "🍇", "🍇", "🍇", "🍇",  # 4 times
    #     "🍊", "🍊", "🍊", "🍊", "🍊", "🍊",  # 6 times
    #     "🍌", "🍌", "🍌", "🍌", "🍌", "🍌", "🍌", "🍌"  # 8 times
    # ]
    all_symbols = []

    # Loops through the symbols dictionary and grabs both the key and value at the same time.
    for symbol, symbol_count in symbols.items():

        # _ is often used as a throwaway variable name in Python loops when the loop variable itself is not needed.
        for _ in range(symbol_count):

            # So for 🍒 where symbol_count = 2: repeat 2 times → append "🍒" → append "🍒".
            # For 🍌 where symbol_count = 8: repeat 8 times → append "🍌" eight times.
            all_symbols.append(symbol)

    # Store each column with the randomly selected symbols on each row.
    columns = []

    for _ in range(cols):

        # Store the symbols for the current column being built.
        column = []

        # [:] creates a copy of the all_symbols array.
        # Reason, so every column always starts with the full bag of symbols.
        current_symbols = all_symbols[:]

        # Loop 3 times for each row in the current column.
        # first loop: picking symbol for row 0 col 1.
        # second loop: picking symbol for row 1 col 1.
        # third loop: picking symbol for row 2 col 1.
        for _ in range(rows):

            # Random pick of a symbol
            value = random.choice(current_symbols)

            # Removes it from the bag so it can't be picked again in this column:
            current_symbols.remove(value)

            # Add the symbol to the current column
            column.append(value)

            # column = ["🍇", "🍒", "🍌"]  ✅

            # So at this point we have two nested loops:
            #   for _ in range(cols):  # repeats 3 times (columns)
            #       for _ in range(rows):  # repeats 3 times (rows)

            # building column 0:
            # → pick symbol for row 0
            # → pick symbol for row 1
            # → pick symbol for row 2
            #
            # building column 1:
            # → pick symbol for row 0
            # → pick symbol for row 1
            # → pick symbol for row 2
            #
            # building column 2:
            # → pick symbol for row 0
            # → pick symbol for row 1
            # → pick symbol for row 2

        columns.append(column)

    return columns

def print_slot_machine(columns):

    # columns[0] is the left column which has 3 symbols, so len(columns[0] is 3.
    for row in range(len(columns[0])):

        # enumerate() give you the index number and the value at the same time.
        # i = 0, column = ["🍒", "🍇", "🍌"]  # left column
        # i = 1, column = ["🍒", "🍊", "🍌"]  # middle column
        # i = 2, column = ["🍒", "🍇", "🍊"]  # right column

        for i, column in enumerate(columns):

            # len(columns) - 1 is 3 - 1 = 2, which is the index of the last column.
            # If I am NOT the last column → print with " | " after.
            # If I AM the last column     → print with nothing after.
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        # Row is complete, go to the next line.
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

            # if lines >= 1 and lines <= MAX_LINES:
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

            # if amount >= MIN_BET and amount <= MAX_BET:
            if MIN_BET <= amount <= MAX_BET:
                break
            else: 
                print(f"Amount must be between {MIN_BET} - {MAX_BET}.")
        else:
            print("Please enter a valid number!")
    
    return amount

def spin(balance):
    lines = get_number_of_lines()

    # while (TRUE) loop, keeps asking the bet until they bet something they can actually afford.
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
           print(f"Not enough funds. Current balance: ${balance}") 
        else:
            break


    print(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    # unpacking. calling the function, we catch both values.
    # first value  → goes into winnings.
    # second value → goes into winning_lines.
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}!")
    print(f"You won on lines: ", *winning_lines)

    # returns the net change to the player's balance.
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break

        # call spin(balance) which runs the entire game round.
        # takes whatever spin() returned and adds it to balance.
        balance += spin(balance)

    print(f"you left with ${balance}")

# def screen():
#     pygame.init()
#     screen = pygame.display.set_mode((1280, 720))
#     clock = pygame.time.Clock()
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         screen.fill("red")
#
#         pygame.display.flip()
#
#         clock.tick(60)
#     pygame.quit()

main()
# screen()
