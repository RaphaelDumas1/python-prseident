import time

from models import PresidentGame
import numpy
from tkinter import *
from PIL import Image, ImageTk, ImageFont
import PIL.Image
import PIL.ImageTk
from functools import partial


def print_ln():
    print('\n')
from tkinter import *
from tkinter import ttk






def game_loop(g: PresidentGame):
    """
    The main game loop.
    Loops in circle until the user wants to quit the application.
    Args:
        g: The President Game instance.
    """
    winner = 0
    global current_player
    current_player = 0
    global loop
    loop = None


    while winner < 3:
        nb_cards = 1
        print('test')
        cant_play = 0
        choice = None
        choice_value = 0
        print(cant_play)
        while cant_play < 3:
            global player
            player = g.players[current_player]
            root = Tk()
            root.geometry("600x600")
            image = PIL.Image.open("./tapis.webp")
            image = image.resize((600, 600), PIL.Image.ANTIALIAS)
            image.save('resized_compressed_image.jpg')
            photo = PIL.ImageTk.PhotoImage(image)
            cadredessin = Canvas(root, bg="black", width=600, height=600)
            bg = cadredessin.create_image(300, 300, anchor='center', image=photo)
            cadredessin.pack(side=BOTTOM)
            image1 = PIL.Image.open("./Card_back_01.svg.png")
            rgb_im1 = image1.convert('RGB')
            rgb_im1.save("yo.jpg")
            rgb_im1 = rgb_im1.resize((37, 25), PIL.Image.ANTIALIAS)
            rgb_im1.save('carte.jpg')
            photo1 = PIL.ImageTk.PhotoImage(rgb_im1)
            image2 = PIL.Image.open("./Card_back_01.svg.png")
            rgb_im2 = image1.convert('RGB')
            rgb_im2.save("yor.jpg")
            rgb_im2 = rgb_im2.resize((25, 37), PIL.Image.ANTIALIAS)
            rgb_im2.save('carte2.jpg')
            photo2 = PIL.ImageTk.PhotoImage(rgb_im2)
            widget = Label(cadredessin, text='', fg='black', bg='white', borderwidth=2, relief='solid')
            widget.pack()
            cadredessin.create_window(300, 300, window=widget, width=50, height=75)
            var1 = IntVar()
            cant_play = IntVar()

            def place_names():
                for i, player in enumerate(g.players):
                    if i == 0:
                        cadredessin.create_text(300, 580, width=100, text=f'{player.name}', font=('Helvetica', '18'), anchor='center', justify=CENTER)
                    elif i == 1:
                        cadredessin.create_text(20, 300, width=10, text=f'{player.name}', font=('Helvetica', '18'), anchor='center', justify=CENTER)
                    elif i == 2:
                        cadredessin.create_text(300, 20, width=100, text=f'{player.name}', font=('Helvetica', '18'), anchor='center', justify=CENTER)
                    elif i == 3:
                        cadredessin.create_text(580, 300, width=10, text=f'{player.name}', font=('Helvetica', '18'), anchor='center', justify=CENTER)
            def place_cards(previous_choice = None, placed_cards ={}):
                for card in placed_cards:
                    if isinstance(placed_cards[card], int):
                        cadredessin.delete(placed_cards[card])
                    else:
                        placed_cards[card].destroy()
                num = 0
                for f, player in enumerate(g.players):
                    for i, card in enumerate(player.hand):
                        num += 1
                        m = (600 - ((len(player.hand) - 1) * 30)) / 2
                        l = m + i * 30
                        if f == 0:
                            m = (600 - ((len(player.hand) + 1) * 4 + len(player.hand) * 30)) / 2
                            l = m + i * 30
                            if previous_choice is None:
                                placed_card = Button(cadredessin, text=f"{card.symbol}",
                                                command=lambda card=card: button_choice(card), width=3, height=2)
                            elif previous_choice is not None:
                                print(card.value)
                                if card.value >= previous_choice.value:
                                    placed_card = Button(cadredessin, text=f"{card.symbol}",
                                                         command=lambda card=card: button_choice(card), width=3,
                                                         height=2)
                                else:
                                    placed_card = Label(cadredessin, text=f"{card.symbol}", width=3,
                                                         height=2)
                            placed_card.place(x=l, y=520)
                            placed_cards[num] = placed_card
                            if i == (len(player.hand) - 1):
                                pass_button = Button(cadredessin, text=f"Pass",
                                            command=lambda card=previous_choice: button_pass(card), width=3, height=2)
                                pass_button.place(x=(l + 40), y=520)
                                placed_cards[0] = pass_button
                        if f == 1:
                            placed_card = cadredessin.create_image(55, l, anchor='center', image=photo1)
                            placed_cards[num] = placed_card
                        elif f == 2:
                            placed_card = cadredessin.create_image(l, 55, anchor='center', image=photo2)
                            placed_cards[num] = placed_card
                        elif f == 3:
                            placed_card = cadredessin.create_image(545, l, anchor='center', image=photo1)
                            placed_cards[num] = placed_card
                        else:
                            pass
                print(placed_cards)
                return placed_cards
            f = place_cards()
            place_names()
            def manage_list(current_player):
                current_player += 1
                if 0 < current_player <= 3:
                    return current_player
                elif current_player > 3:
                    current_player = 0
                    return current_player
                elif current_player < 0:
                    z = [0, 1, 2, 3]
                    current_player = z[current_player]
                    return current_player
            def next_player(choice = None, current_player = None):
                new_current_player = manage_list(current_player)
                global player
                player = g.players[new_current_player]
                if new_current_player != 0:
                    if choice is not None:
                        card_played = player.play(choice.symbol, 1)
                    else:
                        card_played = player.play(None, 1)
                    if len(card_played) != 0:
                        root.after(1, cant_play.set, 0)
                        choice = card_played[0]

                        cadredessin.after(2000, lambda: widget.config(text=f'{choice.symbol}'))
                        root.after(2000, var1.set, 1)
                        root.wait_variable(var1)
                        print(card_played[0])
                        place_cards(choice, f)
                        return next_player(choice, new_current_player)
                    elif len(card_played) == 0:
                        o = cant_play.get() + 1
                        root.after(1, cant_play.set, o)
                        place_cards(choice, f)
                        if cant_play.get() == 3:
                            current_player = current_player - 4
                            y = manage_list(current_player)
                            widget1 = Label(cadredessin, text=f'{g.players[y].name} a gagner le tour', fg='black', bg='white',
                                            borderwidth=2, relief='solid')
                            cadredessin.create_window(300, 300, window=widget1, width=200, height=200)
                            root.after(2000, var1.set, 1)
                            root.wait_variable(var1)
                            widget1.destroy()
                            root.after(1, cant_play.set, 0)
                            if y == 0:
                                pass
                            else:
                                return next_player(None, y)
                        else:
                            widget1 = Label(cadredessin, text=f'{player.name} ne peut pas jouer', fg='black',
                                            bg='white', borderwidth=2, relief='solid')
                            cadredessin.create_window(300, 400, window=widget1, width=200, height=100)
                            root.after(2000, var1.set, 1)
                            root.wait_variable(var1)
                            widget1.destroy()
                            return next_player(choice, new_current_player)
                else:
                    pass
            def button_pass(previous_choice):
                choice = previous_choice
                current_player = 0
                o = cant_play.get() + 1
                root.after(1, cant_play.set, o)
                if cant_play.get() == 3:
                    current_player = current_player - 4
                    y = manage_list(current_player)
                    widget1 = Label(cadredessin, text=f'{g.players[y].name} a gagner le tour', fg='black', bg='white',
                                    borderwidth=2, relief='solid')
                    cadredessin.create_window(300, 300, window=widget1, width=200, height=200)
                    root.after(2000, var1.set, 1)
                    root.wait_variable(var1)
                    widget1.destroy()
                    root.after(1, cant_play.set, 0)
                    return next_player(None, y)
                return next_player(choice, current_player)
            def button_choice(choice = None):
                root.after(1, cant_play.set, 0)
                card_played = player.play(choice.symbol, 1)
                choice = card_played[0]
                cadredessin.after(0, lambda: widget.config(text=f'{choice}'))
                place_cards(None, f)
                return next_player(choice, current_player)
            root.mainloop()


            if len(player.hand) == 0:
                winner += 1

            ### nb_cards = len(test)



if __name__ == '__main__':
    print(
        """        *********************************************
        *** President : The cards game (TM) v.0.1 ***
        ********************************************* """)
    g = PresidentGame()
    g.distribute_cards()
    g.announce_players()
    print_ln()
    game_loop(g)
    print('Thank you for playing. I hope you enjoyed !')


""" jeu :
    tant qu'il n'y a pas de perdant (dernier joueur ayant des cartes en main)
    tant qu'un joueur n'a pas jouer un 2 ou que les autres joeurs ne peux plus jouer
    boucle des joeurs
    
    tour : 
    joueur une carte superieur ou egale
"""