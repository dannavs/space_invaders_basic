import tkinter as tk
from tkinter import *
from tkinter import ttk
from time import sleep


class Invade(tk.Tk):
    def __init__(self):
        Tk.__init__(self)

        self.an_alien = None
        self.bullet = None
        self.user_paddle = None
        self.player_score = 0
        self.player_x = 110
        self.player_y = 450
        self.count = 0
        self.alien_horiz = 10
        self.alien_reload = 400 # the lower the value, the more often alien rows are created
        self.alien_speed = 0.5 # the higher the value, the faster the aliens move downward
        self.level = 1
        self.bollard_x = 10
        self.bollard_y = 400

        self.app_width = 800
        self.app_height = 600

        self.x_cor = (0.5 * self.winfo_screenwidth()) - (0.5 * self.app_width)
        self.y_cor = (0.5 * self.winfo_screenheight()) - (0.5 * self.app_height)
        self.geometry('%dx%d+%d+%d' % (self.app_width, self.app_height, self.x_cor, self.y_cor))
        self.focus_force()
        self.title = "Destroy the Invaders!"

        self.main_frame = ttk.Frame(master=self, padding="5 5 5 5", relief='sunken')
        self.main_frame.grid(column=0, row=0)

        self.info_frame = ttk.Frame(master=self, padding="5 5 5 5")
        self.info_frame.grid(column=0, row=1)

        self.playing_field = Canvas(master=self.main_frame, borderwidth=0, relief='flat', height=500, width=760)
        self.playing_field.grid(column=0, row=0)

        self.start_button = Button(master=self.info_frame, relief='raised', text="Invade!", anchor='s')
        self.start_button.grid(column=1, row=0)

        self.score = ttk.Label(master=self.info_frame, width=20, text=f'Score: {self.player_score}', anchor='se')
        self.score.grid(column=2, row=0)

        self.level_label = ttk.Label(master=self.info_frame, width=20, text=f'Level: {self.level}', anchor='sw')
        self.score.grid(column=0, row=0)

        # self.user_paddle = self.playing_field.create_rectangle(self.player_x, self.player_y, self.player_x + 50,
        #                                                        self.player_y + 50, fill='white')
        self.user_paddle = self.playing_field.create_polygon(self.player_x, self.player_y+30,
                                                             self.player_x+10, self.player_y+50,
                                                             self.player_x+40, self.player_y+50,
                                                             self.player_x+50, self.player_y+30,
                                                             self.player_x+25, self.player_y,
                                                             fill='white')

        # print(self.playing_field.coords(self.user_paddle))

        self.bollards()

        while True:
            self.bind("<KeyPress-Left>", lambda e: self.user_paddle_sub('left'))
            self.bind("<KeyPress-Right>", lambda e: self.user_paddle_sub('right'))

            if self.count % 10 == 0: # user shooting speed
                self.user_shoots()
            if self.count % self.alien_reload == 0: # new alien row
                self.alien_paddles()

            self.playing_field.move('alien', 0, self.alien_speed)
            self.playing_field.move('bullet', 0, -5) # speed of user bullets

            if self.count % 1 == 0:
                self.check_collision()
                self.check_alien_position()

            self.update()
            sleep(0.00)
            self.count += 1

    def user_paddle_sub(self, move):
        # print(f'The move is: {move}')
        the_move = 0

        if move == 'left':
            if self.playing_field.coords(self.user_paddle)[0] < 12:
                self.playing_field.moveto(self.user_paddle, x=10, y=450)
            else:
                the_move = -8
        elif move == 'right':
            if self.playing_field.coords(self.user_paddle)[2] > 709:
                self.playing_field.moveto(self.user_paddle, x=710, y=self.player_y)
            else:
                the_move = 8
        else:
            pass

        self.playing_field.move(self.user_paddle, the_move, 0)
        # print(self.playing_field.coords(self.user_paddle))

    def user_shoots(self):
        shot_x = self.playing_field.coords(self.user_paddle)[0] + 25
        shot_y = self.playing_field.coords(self.user_paddle)[1] - 25
        self.bullet = self.playing_field.create_oval(shot_x-4, shot_y-12, shot_x+4, shot_y,
                                                          fill='yellow',
                                                          outline='yellow',
                                                          tags='bullet')


    def alien_paddles(self):
        for x in range(0, self.alien_horiz):
            self.an_alien = self.playing_field.create_oval(75*x+20, 20, 75*x+70, 70, fill='red', tags='alien')


    def check_collision(self):
        all_bullets = self.playing_field.find_withtag('bullet')
        all_aliens = self.playing_field.find_withtag('alien')
        all_bollards = self.playing_field.find_withtag('bollard')
        for bullet in all_bullets:
            if self.playing_field.coords(bullet)[3] < 0:
                self.playing_field.delete(bullet)
                return

            for alien in all_aliens:
                for bollard in all_bollards:
                    if alien in self.playing_field.find_overlapping(
                            self.playing_field.coords(bullet)[0],
                            self.playing_field.coords(bullet)[1],
                            self.playing_field.coords(bullet)[2],
                            self.playing_field.coords(bullet)[3]):
                        # print("Collision!")
                        self.player_score += 1
                        self.score.config(text=f'Score: {self.player_score}')
                        self.playing_field.delete(bullet)
                        self.playing_field.delete(alien)

                        if self.player_score % 10 == 0:
                            self.level += 1

                        return


                    if bollard in self.playing_field.find_overlapping(
                            self.playing_field.coords(bullet)[0],
                            self.playing_field.coords(bullet)[1],
                            self.playing_field.coords(bullet)[2],
                            self.playing_field.coords(bullet)[3]):
                        self.playing_field.delete(bullet)
                        return

                    if bollard in self.playing_field.find_overlapping(
                            self.playing_field.coords(alien)[0],
                            self.playing_field.coords(alien)[1],
                            self.playing_field.coords(alien)[2],
                            self.playing_field.coords(alien)[3]):
                        self.playing_field.delete(bollard)
                        self.playing_field.delete(alien)
                        return


    def check_alien_position(self):
        all_aliens = self.playing_field.find_withtag('alien')
        for alien in all_aliens:
            if self.playing_field.coords(alien)[3] > self.player_y:
                print("Aliens win!")
                self.playing_field.delete(self.user_paddle)
                return


    def bollards(self):
        # self.playing_field.create_polygon()
        for x in range(0, 15):
            spacer = 5.2*x
            self.playing_field.create_polygon(spacer*self.bollard_x+5, self.bollard_y+20,
                                              spacer*self.bollard_x+15, self.bollard_y,
                                              spacer*self.bollard_x+25, self.bollard_y+20,
                                              fill='green',
                                              tags='bollard')


if __name__ == "__main__":
    invade = Invade()
    invade.mainloop()