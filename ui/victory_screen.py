from ui.ui_base import ui_base 

from direct.gui.DirectGui import DirectButton, DirectLabel

class victory_screen(ui_base):
    def __init__(self, player_score, enemy_score):
        ui_base.__init__(self)
        self.ui_elements = []

        self.font = loader.loadFont("assets/fonts/NewAmsterdam-Regular.ttf")
              
        outcome_label = DirectLabel(text=("You did it!"),pos=(0,0,0), scale=0.2, text_font=self.font, relief=None, text_fg=(255,255,255,1))
        self.ui_elements.append(outcome_label)

        timer_info = DirectLabel(text=(f"{player_score} - {enemy_score} = {player_score - enemy_score}"), pos=(0,0,-.4), scale=0.1 , text_font=self.font, relief=None, text_fg=(255,255,255,1))
        self.ui_elements.append(timer_info)
        
        main_menu_button = DirectButton(text=("Return to main menu"), pos=(0,0,-0.7), scale=0.1, command=self.goto_main_menu, text_font=self.font, relief=None, text_fg =(255,255,255,1))
        self.ui_elements.append(main_menu_button)
    
    def goto_main_menu(self):
        messenger.send('goto_main_menu') 
