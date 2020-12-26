import re
import copy

def score_game(p1_deck_end, p2_deck_end):
    winning_deck = []
    if p1_deck_end:
        winning_deck = p1_deck_end
    elif p2_deck_end:
        winning_deck = p2_deck_end
    winning_player_score = 0
    for i, v in enumerate(winning_deck[::-1]):
        winning_player_score += v*(i+1)
    return winning_player_score

def play_game(p1_deck, p2_deck, game_number=1):
    # print(f"=== Game {game_number} ===")
    game_history = set()
    p1_deck = copy.copy(p1_deck)
    p2_deck = copy.copy(p2_deck)
    game_winner = None

    round_numer = 1
    while not( len(p1_deck) == 0 or len(p2_deck) == 0):
        # print(f"-- Round {round_numer} --")
        # print(f"p1_deck: {p1_deck}")
        # print(f"p2_deck: {p2_deck}")

        current_game_state = (tuple(p1_deck), tuple(p2_deck))
        if current_game_state in game_history:
            # print("Game state seen before...")
            game_winner = 'p1'
            break
        else:
            game_history.add(current_game_state)
            
        p1_card = p1_deck.pop(0)
        p2_card = p2_deck.pop(0)
        # print(f"p1_card: {p1_card}")
        # print(f"p2_card: {p2_card}")
        
        if len(p1_deck) >= p1_card and len(p2_deck) >= p2_card:
            # print("Going into a sub-game...")
            game_number+=1
            round_winner, _, _ = play_game(p1_deck[:p1_card], p2_deck[:p2_card], game_number)
            # print(f"Sub-game winner: {round_winner}")
        else:
            # print("Playing like normal...")
            if p1_card > p2_card:
                round_winner = 'p1'
            elif p2_card > p1_card:
                round_winner = 'p2'
            # print(f"Bigger card: {round_winner}")
        
        if round_winner == 'p1':
            p1_deck.append(p1_card)
            p1_deck.append(p2_card)
        elif round_winner == 'p2':
            p2_deck.append(p2_card)
            p2_deck.append(p1_card)
        
        # print(f"Round winner: {round_winner}")
        round_numer +=1
        # print()
    
    if not game_winner:
        if p1_deck:
            game_winner = 'p1'
        if p2_deck: 
            game_winner = 'p2'

    # print(f"game_winner: {game_winner}")
    # print()
    return game_winner, p1_deck, p2_deck

def play_game_simple(p1_deck, p2_deck):
    p1_deck = copy.copy(p1_deck)
    p2_deck = copy.copy(p2_deck)

    while not( len(p1_deck) == 0 or len(p2_deck) == 0):
        # print("--Round--")
        # print(f"p1_deck: {p1_deck}")
        # print(f"p2_deck: {p2_deck}")
        
        p1_card = p1_deck.pop(0)
        p2_card = p2_deck.pop(0)

        # print(f"p1_card: {p1_card}")
        # print(f"p2_card: {p2_card}")

        if p1_card > p2_card:
            # print("p1 wins")
            p1_deck.append(p1_card)
            p1_deck.append(p2_card)
        elif p2_card > p1_card:
            # print("p2 wins")
            p2_deck.append(p2_card)
            p2_deck.append(p1_card)
    
    if p1_deck:
        game_winner = 'p1'
    if p2_deck: 
        game_winner = 'p2'
    return game_winner, p1_deck, p2_deck

if __name__ == "__main__":
    with open("input.txt") as f:
        input_data = f.read()
    
    player_moves = re.split(r'\r?\n\r?\n', input_data)
    player_moves = [i.splitlines()[1:] for i in player_moves]

    p1_deck = list(map(int, player_moves[0]))
    p2_deck = list(map(int, player_moves[1]))

    winner, p1_deck_end, p2_deck_end = play_game_simple(p1_deck, p2_deck)
    winning_player_score = score_game(p1_deck_end, p2_deck_end)
    print(f"Part 1: {winning_player_score}")

    winner_2, p1_deck_end_2, p2_deck_end_2 = play_game(p1_deck, p2_deck)
    winning_player_score_2 = score_game(p1_deck_end_2, p2_deck_end_2)
    print(f"Part 2: {winning_player_score_2}")

