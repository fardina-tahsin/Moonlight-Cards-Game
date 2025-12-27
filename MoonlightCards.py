
import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QGridLayout, 
                             QInputDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Card Class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()
    
    def _get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.suit[0]}"

# Deck class, 52 cards  
class Deck:
    def __init__(self):
        suits = ['♥ Hearts', '♦ Diamonds', '♣ Clubs', '♠ Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()

# Hand value logic
class MoonlightCardHand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def score(self):
        score = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

# Player logic
class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.balance = balance
        self.bet = 0
        self.hand = MoonlightCardHand()
        
        # new stats
        self.wins = 0
        self.losses = 0
        self.tie = 0
    

    def place_bet(self, amount):
        if amount <= self.balance and amount > 0:
            self.bet = amount
            self.balance -= amount
            return True
        return False

    def win_bet(self, multiplier=1):
        win_amount = self.bet * (1 + multiplier)
        self.balance += win_amount
        self.bet = 0
        self.wins += 1 

    def lose_bet(self):
        self.bet = 0
        self.losses += 1

    def push_bet(self):
        self.balance += self.bet
        self.bet = 0
        self.tie += 1

    def reset_hand(self):
        self.hand = MoonlightCardHand()

# Game logic
class MoonlightCardGame:
    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.dealer = Player("Dealer")
    
    def deal_initial(self):
        for _ in range(2):
            for player in self.players:
                player.hand.add_card(self.deck.deal_card())
            self.dealer.hand.add_card(self.deck.deal_card())

    def dealer_turn(self):
        while self.dealer.hand.score() < 17:
            self.dealer.hand.add_card(self.deck.deal_card())

    def settle_bets(self):
        dealer_score = self.dealer.hand.score()
        for player in self.players:
            player_score = player.hand.score()
            if player_score > 21:
                player.lose_bet()
            elif dealer_score > 21 or player_score > dealer_score:
                if player_score == 21 and len(player.hand.cards) == 2:
                    player.win_bet(multiplier=2)  
                else:
                    player.win_bet()
            elif player_score == dealer_score:
                player.push_bet()
            else:
                player.lose_bet()

    def reset_round(self):
        self.deck = Deck()
        self.dealer.reset_hand()
        for player in self.players:
            player.reset_hand()

# Main GUI Window
class MoonlightCardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = None
        self.current_player = None
        self.game_active = False
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('BlackJack Game')
        self.setGeometry(300, 100, 1100, 780)

        self.setStyleSheet("""
            QMainWindow { background-color: #F2F1C2; }
            QLabel { font-family: 'Segoe UI'; }
        """)
        
        central = QWidget()
        central.setContentsMargins(30, 25, 30, 25)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(18)
        
        # Title
        title = QLabel('Moonlight Cards Game')
        title.setFont(QFont('Segoe UI', 30, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#1C1C1E; letter-spacing:2.5px;")
        main_layout.addWidget(title) 

        subtitle = QLabel("Moonlight 21 Casino Edition")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#555; font-size:18px;")
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(15)
        
        # Game Area
        game_area = QHBoxLayout()
        game_area.setSpacing(40)
        
        # Cards Display (Left side)
        cards_area = QVBoxLayout()
        cards_area.setSpacing(20)

        card_style = """
            QLabel {
                background-color:#0F0F10;
                color:white;
                border-radius:28px;
                padding:16px;
                font-size:17px;
                border: 2px solid #333;
            }
        """
        
        # Dealer Section
        dealer_title = QLabel('(: DEALER')
        dealer_title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        dealer_title.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(dealer_title)
        
        self.dealer_cards = QLabel('No cards dealt yet')
        self.dealer_cards.setFixedHeight(120)
        self.dealer_cards.setStyleSheet(card_style)
        self.dealer_cards.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(self.dealer_cards)
        
        self.dealer_score = QLabel('Score: 0')
        self.dealer_score.setStyleSheet("color:#1C1C1E; font-size:19px;")
        self.dealer_score.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(self.dealer_score)        
        cards_area.addSpacing(25)
        
        # Player Section
        player_title = QLabel(':) PLAYER')
        player_title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        player_title.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(player_title)

        self.player_cards = QLabel('No cards dealt yet')
        self.player_cards.setFixedHeight(120)
        self.player_cards.setStyleSheet(card_style)   
        self.player_cards.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(self.player_cards)
        
        self.player_score = QLabel('Score: 0')
        self.player_score.setStyleSheet("color:#1C1C1E; font-size:19px;")
        self.player_score.setAlignment(Qt.AlignCenter)
        cards_area.addWidget(self.player_score)
        
        game_area.addLayout(cards_area, 3)
        
        # Controls Panel (Right side)
        controls_panel = QVBoxLayout()
        controls_panel.setSpacing(20)
        controls_panel.setContentsMargins(0, 45, 0, 0)

        # Decorative Cards
        decor_cards_layout = QHBoxLayout()
        decor_cards_layout.setSpacing(10)
        decor_cards_layout.setAlignment(Qt.AlignCenter)
        
        def make_card(text):
            lbl = QLabel(text)
            lbl.setFixedSize(98, 125)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("""
                QLabel {
                    background:#0F0F10;
                    color:#FFD977;
                    border-radius:12px;
                    font-size:18px;
                    font-weight:bold;
                    border:2px solid #333;
                }
            """)
            return lbl
        
        decor_cards_layout.addWidget(make_card("A♠"))
        decor_cards_layout.addWidget(make_card("K♥"))
        decor_cards_layout.addWidget(make_card("Q♦"))
        decor_cards_layout.addWidget(make_card("J♣"))
        
        controls_panel.addLayout(decor_cards_layout)
     
        # Balance Display
        self.balance_label = QLabel(' ৳ Balance: 1000Tk')
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("""
            background:#1C1C1E;
            color:#FFD977;
            padding:38px;
            border-radius:26px;
            font-size:19px;
            border: 2px solid #333;
        """)
        controls_panel.addWidget(self.balance_label)

        # display stats 
        self.stats_label = QLabel('Wins: 0  |  Losses: 0  |  Ties: 0')
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            background:#1C1C1E;
            color:#FFD977;
            padding:18px;
            border-radius:20px;
            font-size:16px;
        """)
        controls_panel.addSpacing(-13)
        controls_panel.addWidget(self.stats_label)
        
        # Main Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.new_game_btn = QPushButton('ඞ NEW GAME')
        self.deal_btn = QPushButton('✌︎︎ DEAL')
        self.hit_btn = QPushButton('⚔︎ HIT')
        self.stand_btn = QPushButton('~ STAND')
        
        # Button styling
        buttons = [self.new_game_btn, self.deal_btn, self.hit_btn, self.stand_btn]
        for btn in buttons:
            btn.setFont(QFont('Segoe UI', 14, QFont.Bold))
            btn.setStyleSheet("""
                    QPushButton {
                        background:#2C2C2E;
                        color:white;
                        border-radius285px;
                        padding:12px 22px;
                        font-size:15px;
                    }
                    QPushButton:hover { background:#3A3A3C; }
                    QPushButton:disabled { background:#8E8E93; }
                    """)
            btn.setFixedHeight(55)
            btn.setEnabled(False)
        
        self.new_game_btn.setEnabled(True)
        
        btn_layout.addWidget(self.new_game_btn)
        btn_layout.addWidget(self.deal_btn)
        btn_layout.addWidget(self.hit_btn)
        btn_layout.addWidget(self.stand_btn)
        controls_panel.addLayout(btn_layout)
        self.new_game_btn.setShortcut(Qt.Key_N) # press key N to trigger new game
        self.deal_btn.setShortcut(Qt.Key_D) # press key D to trigger deal
        self.hit_btn.setShortcut(Qt.Key_H) # press key H to trigger hit
        self.stand_btn.setShortcut(Qt.Key_S) # press key S to trigger stand
        
        # Status Display
        self.status_label = QLabel('-`♡´- Welcome to Moonlight! Click NEW GAME to start!')
        self.status_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.status_label.setStyleSheet("""
                background:#0F0F10;
                color:#FFD977;
                border-radius:26px;
                padding:26px;
                font-size:17px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        controls_panel.addWidget(self.status_label)
        controls_panel.addStretch()

        # Restart button 

        restart_layout = QHBoxLayout()
        restart_layout.addStretch()

        self.restart_round_btn = QPushButton('♻ RESTART ROUND')
        self.restart_round_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.restart_round_btn.setFixedHeight(42)
        self.restart_round_btn.setEnabled(False)
        self.restart_round_btn.setStyleSheet("""
            QPushButton {
                background:#3A3A3C;
                color:#FFD977;
                border-radius:20px;
                padding:8px 18px;
            }
            QPushButton:hover { background:#4A4A4C; }
            QPushButton:disabled { background:#8E8E93; }
        
        """)
        restart_layout.addWidget(self.restart_round_btn)
        controls_panel.addLayout(restart_layout)
        self.restart_round_btn.setShortcut(Qt.Key_R)  # press key R to trigger restart

        game_area.addLayout(controls_panel, 2)
        main_layout.addLayout(game_area)
        
        # Connect signals
        self.new_game_btn.clicked.connect(self.new_game)
        self.deal_btn.clicked.connect(self.place_bet_and_deal)
        self.hit_btn.clicked.connect(self.hit)
        self.stand_btn.clicked.connect(self.stand)
        self.restart_round_btn.clicked.connect(self.restart_round)
    
    def new_game(self):
        if self.game:
            self.game.reset_round()
            
        names, ok = QInputDialog.getText(self, 'Player Setup', 
                                       'Enter player name (or press OK for "Player"):')
        if not ok:
            names = "Player"
        self.game = MoonlightCardGame([str(names)])
        self.current_player = self.game.players[0]
        self.game_active = False
        self.update_display()
        self.new_game_btn.setEnabled(True)
        self.deal_btn.setEnabled(True)
        self.hit_btn.setEnabled(False)
        self.stand_btn.setEnabled(False)
        self.status_label.setText(f'-`♡´- Welcome {self.current_player.name}! Balance: Tk{self.current_player.balance}\nClick DEAL to place bet and start!')
    
    def place_bet_and_deal(self):
        bet, ok = QInputDialog.getInt(self, 'Place Bet', 
                                    f'Balance: Tk{self.current_player.balance}\nEnter bet amount:', 
                                    100, 50, self.current_player.balance)
        
        if ok and self.current_player.place_bet(bet):
            self.game.deal_initial()
            self.game_active = True
            self.deal_btn.setEnabled(False)
            self.hit_btn.setEnabled(True)
            self.stand_btn.setEnabled(True)
            self.update_display()
            self.status_label.setText('╰┈➤ Your turn! HIT or STAND?')
        else:
            QMessageBox.warning(self, 'Invalid Bet', 'Not enough money or invalid amount!')
    
    def hit(self):
        if self.game_active and self.current_player.hand.score() <= 21:
            self.current_player.hand.add_card(self.game.deck.deal_card())
            self.update_display()
            if self.current_player.hand.score() > 21:
                self.game_active = False
                self.hit_btn.setEnabled(False)
                self.stand_btn.setEnabled(False)
                self.status_label.setText('✗ Dealer Wins! ⚡︎ Player Busts!')
    
    def stand(self):
        self.game_active = False
        self.hit_btn.setEnabled(False)
        self.stand_btn.setEnabled(False)
        self.game.dealer_turn()
        self.game.settle_bets()
        self.update_display()
        self.show_result()
    
    def update_display(self):
        # Dealer cards (hide second card until stand)
        dealer_cards_str = [str(card) for card in self.game.dealer.hand.cards]
        if len(dealer_cards_str) > 1 and self.hit_btn.isEnabled():
            dealer_cards_str[1] = ' ？'
        
        self.dealer_cards.setText(' | '.join(dealer_cards_str))
        self.dealer_score.setText(f'Score: {self.game.dealer.hand.score()}')
        
        self.player_cards.setText(' | '.join(str(card) for card in self.current_player.hand.cards))
        self.player_score.setText(f'Score: {self.current_player.hand.score()}')
        self.balance_label.setText(f' ৳Balance: ৳{self.current_player.balance} (Bet: ৳{self.current_player.bet})')
    
    def show_result(self):
        player_score = self.current_player.hand.score()
        dealer_score = self.game.dealer.hand.score()
        
        if player_score > 21:
            result = '✗ Dealer Wins! ⚡︎ Player Busts!'
        elif dealer_score > 21:
            result = '🏆 Player Wins! ⚡︎ Dealer Busts!'
        elif player_score > dealer_score:
            if player_score == 21 and len(self.current_player.hand.cards) == 2:
                result = '˗ˋˏ৳ˎˊ˗ MoonlightCard Rule! Player Wins 2x!'
            else:
                result = '🏆 Player Wins!'
        elif player_score == dealer_score:
            result = '୨ৎ Tie!'
        else:
            result = '✗ Dealer Wins!'
        
        self.status_label.setText(result)
        self.deal_btn.setEnabled(True)
        self.restart_round_btn.setEnabled(True)
        
        self.stats_label.setText(
            f'Wins: {self.current_player.wins} | '
            f'Losses: {self.current_player.losses} | '
            f'Ties: {self.current_player.tie}'
        )

    def reset_round(self):
        self.game.reset_round()
        self.game_active = False
        self.update_display()
        self.hit_btn.setEnabled(False)
        self.stand_btn.setEnabled(False)
        self.deal_btn.setEnabled(True)
    
    def restart_round(self):
        if not self.game:
            return 
        
        self.game.reset_round() 
        self.game_active = False 
        self.update_display() 
        self.deal_btn.setEnabled(True)
        self.hit_btn.setEnabled(False)
        self.stand_btn.setEnabled(False)
        self.restart_round_btn.setEnabled(False)
        
        self.status_label.setText(
            f'Round restarted! Place your bet'
        )
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion') 
    window = MoonlightCardGUI()
    window.show()
    sys.exit(app.exec_())
