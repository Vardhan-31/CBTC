def get_valid_number(prompt):
    while True:
        try:
            number = input(prompt)
            if number.isdigit():
                return number
            else:
                print("Enter a valid multi-digit number.")
        except ValueError:
            print("Invalid input,Enter a valid multi-digit number.")

def check_guess(secret, guess):
    correct_digits = 0
    correct_positions = 0
    
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            correct_positions += 1
        elif guess[i] in secret:
            correct_digits += 1
    
    return correct_digits, correct_positions

def play_round(player_name, secret_number):
    attempts = 0
    while True:
        guess = get_valid_number(f"{player_name}, Enter your guess (must be {len(secret_number)} digits): ")
        
        # Ensure the guess is the same length as the secret number
        if len(guess) != len(secret_number):
            print(f"Your guess must be exactly {len(secret_number)} digits long.")
            continue
        
        attempts += 1
        
        if guess == secret_number:
            print(f"Congratulations {player_name}! You've guessed the number in {attempts} attempts.")
            return attempts
        
        correct_digits, correct_positions = check_guess(secret_number, guess)
        print(f"{correct_digits} digits are correct but in the wrong position.")
        print(f"{correct_positions} digits are correct and in the correct position.")

def main():
    
   
    print("Player 1, set a multi-digit number for Player 2 to guess:")  # Player 1 sets the number
    player1_secret = get_valid_number("Player 1, enter your secret number: ")
    
    
    print("\nPlayer 2, it's your turn to guess.") # Player 2 guesses
    player2_attempts = play_round("Player 2", player1_secret)
    
   
    print("\nPlayer 2, set a multi-digit number for Player 1 to guess:")  # Player 2 sets the number
    player2_secret = get_valid_number("Player 2, enter your secret number: ")
    
    
    print("\nPlayer 1, it's your turn to guess.") # Player 1 guesses
    player1_attempts = play_round("Player 1", player2_secret)
    
    # Determine the winner
    if player1_attempts < player2_attempts:
        print("\nPlayer 1 wins the game and is crowned Mastermind!")
    elif player1_attempts > player2_attempts:
        print("\nPlayer 2 wins the game and is crowned Mastermind!")
    else:
        print("\nIt's a tie!")

if __name__ == "__main__":
    main()
