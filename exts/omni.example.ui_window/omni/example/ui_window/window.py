# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["ExampleWindow"]

import omni.ui as ui
from .style import example_window_style
from .color_widget import ColorWidget

LABEL_WIDTH = 120
SPACING = 4


class ExampleWindow(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        # Apply the style to all the widgets of this window
        self.frame.style = example_window_style
        # Set the function that is called to build widgets when the window is
        # visible

    def destroy(self):
        # It will destroy all the children
        super().destroy()

    @property
    def label_width(self):
        """The width of the attribute label"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """The width of the attribute label"""
        self.__label_width = value
        self.frame.rebuild()

    def _build_collapsable_header(self, collapsed, title):
        """Build a custom title of CollapsableFrame"""
        with ui.HStack():
            ui.Label(title, name="collapsable_name")

            if collapsed:
                image_name = "collapsable_opened"
            else:
                image_name = "collapsable_closed"
            ui.Image(name=image_name, width=20, height=20)

    def _build_calculations(self):
        # Build the widgets of the "Calculations" group

            # A VStack is a vertical stack and aligns widgets vertically one after the other

                # An HStack is a horizontal stack and aligns widgets horizontally one after the other

                    # A label displays text

                    # An IntSlider lets a user choos an integer by sliding a bar back and forth

                # Pairing a label with a control is a common UI comb

                    # The label makes the purpose of the control clear

                    # You can set the min and max value on an IntSlider
        pass

    def _build_parameters(self):
        # Build the widgets of the "Parameters" group

                    # A Float Slider is similar to an Int Slider
                    # controls a 'float' which is a number with a decimal point (A Real number)

                    # You can set the min and max of a float slider as well

                # Setting the labels all to the same width gives the UI a nice alignment

                # A few more examples of float sliders

        pass

    def _build_light_1(self):
        # Build the widgets of the "Light 1" group
        
                    # A multi float drag field lets you control a group of floats (Real numbers)

                # Notice what we use the same label width in all of the collapsable frames
                #   This ensures that the entire UI has a consistent feel

                #Feel free to copy this color widget and use it in your on UIs

                    # The custom compound widget

                #An example of a checkbox
        pass

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
