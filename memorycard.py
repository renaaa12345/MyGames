from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import random

class MemoryCardGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.cards = []
        self.create_cards()
        self.selected_cards = []

    def create_cards(self):
        values = list(range(8)) * 2  # Create pairs of numbers
        random.shuffle(values)

        for value in values:
            card = Button(text='?', on_press=self.card_selected)
            card.value = value  # Store the actual value
            self.cards.append(card)
            self.add_widget(card)

    def card_selected(self, button):
        if button not in self.selected_cards and len(self.selected_cards) < 2:
            button.text = str(button.value)  # Show the card value
            self.selected_cards.append(button)

            if len(self.selected_cards) == 2:
                self.check_match()

    def check_match(self):
        if self.selected_cards[0].value == self.selected_cards[1].value:
            self.selected_cards.clear()  # Clear selected cards
        else:
            from kivy.clock import Clock
            Clock.schedule_once(self.hide_cards, 1)

    def hide_cards(self, dt):
        for card in self.selected_cards:
            card.text = '?'  # Hide the values again
        self.selected_cards.clear()

class MemoryCardGameApp(App):
    def build(self):
        return MemoryCardGame()

if __name__ == '__main__':
    MemoryCardGameApp().run()
