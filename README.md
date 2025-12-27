## object-oriented programming (oop)

# 🌙 Moonlight Cards Game 

A modern Blackjack (21) casino-style desktop game built with Python & PyQt5, featuring a sleek UI, betting system, player stats, and smooth gameplay inspired by classic casino rules with a custom MoonlightCard twist.

<img width="1102" height="845" alt="Screenshot 2025-12-28 004724" src="https://github.com/user-attachments/assets/d993e895-5b00-4284-9b63-7234e32129d3" />


## Features

   - Classic Blackjack (21) gameplay
    
   - Betting system with balance management
    
   - Automatic Ace handling (1 or 11)
    
   - Moonlight Rule: Blackjack (21 with 2 cards) pays 2x

   - Player statistics:
    
        - Wins
        
        - Losses
        
        - Ties

   - Modern casino-themed PyQt5 UI
    
   - Keyboard shortcuts for fast gameplay
    
   - Restart round without restarting the app


## Gameplay Rules

   - Dealer hits until score >= 17
    
   - Player busts if score > 21
    
   - Face cards (J, Q, K) = 10
    
   - Ace = 11 (or 1 if needed)
    
   - Blackjack (21 with 2 cards) -> 2x payout
    
   - Tie returns the bet


## Technologies

   - Python 3.8+
    
   - PyQt5


### Install dependencies

   ```bash
        pip install PyQt5
   ```

### How to Run

   ```bash
        python MoonlightCards.py
   ```

## Architecture Overview

   - Card / Deck -> Card creation & shuffling
    
   - MoonlightCardHand -> Score calculation with Ace logic
    
   - Player -> Balance, betting, statistics
    
   - MoonlightCardGame -> Core Blackjack rules
    
   - MoonlightCardGUI -> PyQt5 interface & interactions
