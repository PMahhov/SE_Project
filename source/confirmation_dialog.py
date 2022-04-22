import warnings
from typing import Union

import pygame

from pygame_gui.core import ObjectID
from pygame_gui._constants import UI_CONFIRMATION_DIALOG_CONFIRMED, UI_BUTTON_PRESSED, OldType
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIWindow, UIButton, UITextBox


class UIConfirmationDialog(UIWindow):

    def __init__(self, rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 action_long_desc: str,
                 *,
                 window_title: str = 'pygame-gui.Confirm',
                 action1_short_name: str = 'pygame-gui.OK',
                 action2_short_name: str = 'pygame-gui.Cancel',
                 blocking: bool = True,
                 object_id: Union[ObjectID, str] = ObjectID('#confirmation_dialog', None),
                 visible: int = 1):

        super().__init__(rect, manager,
                         window_display_title=window_title,
                         object_id=object_id,
                         resizable=True,
                         visible=visible)

        minimum_dimensions = (260, 200)
        if rect.width < minimum_dimensions[0] or rect.height < minimum_dimensions[1]:
            warn_string = ("Initial size: " + str(rect.size) +
                           " is less than minimum dimensions: " + str(minimum_dimensions))
            warnings.warn(warn_string, UserWarning)
        self.set_minimum_dimensions(minimum_dimensions)

        self.action2_button = UIButton(relative_rect=pygame.Rect(-10, -40, -1, 30),
                                      text=action2_short_name,
                                      manager=self.ui_manager,
                                      container=self,
                                      object_id='#action2_button',
                                      anchors={'left': 'right',
                                               'right': 'right',
                                               'top': 'bottom',
                                               'bottom': 'bottom'})

        self.action1_button = UIButton(relative_rect=pygame.Rect(-10, -40, -1, 30),
                                       text=action1_short_name,
                                       manager=self.ui_manager,
                                       container=self,
                                       object_id='#action1_button',
                                       anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'bottom',
                                                'bottom': 'bottom',
                                                'left_target': self.action2_button,
                                                'right_target': self.action2_button})

        text_width = self.get_container().get_size()[0] - 10
        text_height = self.get_container().get_size()[1] - 50
        self.confirmation_text = UITextBox(html_text=action_long_desc,
                                           relative_rect=pygame.Rect(5, 5,
                                                                     text_width,
                                                                     text_height),
                                           manager=self.ui_manager,
                                           container=self,
                                           anchors={'left': 'left',
                                                    'right': 'right',
                                                    'top': 'top',
                                                    'bottom': 'bottom'})

        self.set_blocking(blocking)

    def process_event(self, event: pygame.event.Event) -> bool:
        # Process any events relevant to the confirmation dialog.

        consumed_event = super().process_event(event)

        # close whindow when a button is pressed
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.action2_button:
            self.kill()
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.action1_button:
            self.kill()

        return consumed_event