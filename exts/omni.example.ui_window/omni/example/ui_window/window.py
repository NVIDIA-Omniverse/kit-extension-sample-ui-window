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
        self.frame.set_build_fn(self._build_fn)

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
        """Build the widgets of the "Calculations" group"""
        with ui.CollapsableFrame("Calculations", name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    ui.Label("Precision", name="attribute_name", width=self.label_width)
                    ui.IntSlider(name="attribute_int")

                with ui.HStack():
                    ui.Label("Iterations", name="attribute_name", width=self.label_width)
                    ui.IntSlider(name="attribute_int", min=0, max=5)

    def _build_parameters(self):
        """Build the widgets of the "Parameters" group"""
        with ui.CollapsableFrame("Parameters", name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    ui.Label("Value", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float")

                with ui.HStack():
                    ui.Label("i", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("j", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("k", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("Theta", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float")

    def _build_light_1(self):
        """Build the widgets of the "Light 1" group"""
        with ui.CollapsableFrame("Light 1", name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    ui.Label("Orientation", name="attribute_name", width=self.label_width)
                    ui.MultiFloatDragField(0.0, 0.0, 0.0, h_spacing=SPACING, name="attribute_vector")

                with ui.HStack():
                    ui.Label("Intensity", name="attribute_name", width=self.label_width)
                    ui.FloatSlider(name="attribute_float")

                with ui.HStack():
                    ui.Label("Color", name="attribute_name", width=self.label_width)
                    # The custom compound widget
                    ColorWidget(0.25, 0.5, 0.75)

                with ui.HStack():
                    ui.Label("Shadow", name="attribute_name", width=self.label_width)
                    ui.CheckBox(name="attribute_bool")

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame():
            with ui.VStack(height=0):
                self._build_calculations()
                self._build_parameters()
                self._build_light_1()
