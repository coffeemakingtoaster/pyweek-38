from ui.ui_base import ui_base
from panda3d.core import TransparencyAttrib, TextNode
from constants.events import EVENT_NAMES

from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame, DGG

class game_over(ui_base):
    def __init__(self):
        ui_base.__init__(self)

        
        TEXT_COLOR = (1, 0, 0, 1)  # Red color for text

        # Large "GAME OVER" text
        self.game_over_label = DirectLabel(
            text="GAME OVER",  # Text to display
            scale=0.3,  # Size of the text
            pos=(0, 0, 0.3),  # Position on the screen (x, y, z)
            text_fg=TEXT_COLOR,  # Text color (red)
            text_align=TextNode.ACenter,  # Center the text
             # Use custom font if you have one (optional)
            relief=None  # No background box
        )

        # Smaller "Your cover has been blown" text
        self.blow_cover_label = DirectLabel(
            text="Your cover has been blown",
            scale=0.07,  # Smaller size
            pos=(0, 0, 0),  # Slightly below the GAME OVER text
            text_fg=TEXT_COLOR,  # Same red color
            text_align=TextNode.ACenter,
             # Use custom font if available
            relief=None
        )

        # Set transparency (optional, in case you need transparent UI elements)
        self.game_over_label.setTransparency(TransparencyAttrib.MAlpha)
        self.blow_cover_label.setTransparency(TransparencyAttrib.MAlpha)


        
    

