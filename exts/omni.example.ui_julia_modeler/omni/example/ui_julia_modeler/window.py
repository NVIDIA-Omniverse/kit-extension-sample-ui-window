# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["ExampleWindow"]

from ctypes import alignment
import omni.ui as ui
from .style import example_window_style
from .color_widget import ColorWidget
from .slider_widget import SliderWidget

LABEL_WIDTH = 150
ATTR_LABEL_HEIGHT = 15
SPACING = 5


# TODO: rename class and __all__ above
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
        with ui.VStack():
            ui.Spacer(height=10)
            with ui.HStack():
                ui.Label(title, name="collapsable_name")

                if collapsed:
                    image_name = "collapsable_opened"
                else:
                    image_name = "collapsable_closed"
                ui.Image(name=image_name, width=10, height=10)
            ui.Spacer(height=8)
            ui.Line(style_type_name_override="HeaderLine")

    def _build_calculations(self):
        """Build the widgets of the "Calculations" group"""
        with ui.CollapsableFrame("Calculations".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                with ui.HStack():
                    ui.Label("Precision", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=20, num_type="int")  # TODO: set start val to 6

                with ui.HStack():
                    ui.Label("Iterations", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=20, num_type="int")  # TODO: set start val to 10

    def _build_parameters(self):
        """Build the widgets of the "Parameters" group"""
        with ui.CollapsableFrame("Parameters".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                with ui.HStack():
                    ui.Label("Value", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=-2, max=2, display_range=True)  # TODO: set start val to 0.75
                    # ui.FloatSlider(name="attribute_float")

                with ui.HStack():
                    ui.Label("i", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=2, display_range=True)  # TODO: set start val to 0.65
                    # ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("j", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=2, display_range=True)  # TODO: set start val to 0.25
                    # ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("k", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=2, display_range=True)  # TODO: set start val to 0.55
                    # ui.FloatSlider(name="attribute_float", min=-1, max=1)

                with ui.HStack():
                    ui.Label("Theta", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=3.14, display_range=True)  # TODO: set start val to 1.25
                    # ui.FloatSlider(name="attribute_float")

    def _build_light_1(self):
        """Build the widgets of the "Light 1" group"""
        with ui.CollapsableFrame("Light 1".upper(), name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                with ui.HStack():
                    ui.Label("Orientation", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.MultiFloatDragField(0.0, 0.0, 0.0, h_spacing=SPACING, name="attribute_vector")

                with ui.HStack():
                    ui.Label("Intensity", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=1.75)  # TODO: set start val to 1.75
                    # ui.FloatSlider(name="attribute_float")

                with ui.HStack():
                    ui.Label("Color", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    # The custom compound widget
                    ColorWidget(0.25, 0.5, 0.75)

                with ui.HStack():
                    ui.Label("Shadow", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.CheckBox(name="attribute_bool")

                with ui.HStack():
                    ui.Label("Shadow Softness", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=2)  # TODO: set start val to .1

    def _build_scene(self):
        """Build the widgets of the "Scene" group"""
        with ui.CollapsableFrame("Scene".upper(), name="group", build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                with ui.HStack():
                    ui.Label("Field of View", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=160, display_range=True, num_type="int")  # TODO: set start val to 60

                with ui.HStack():
                    ui.Label("Orientation", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.MultiFloatDragField(0.0, 0.0, 0.0, h_spacing=SPACING, name="attribute_vector")

                with ui.HStack():
                    ui.Label("Camera Distance", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    SliderWidget(min=0, max=2)  # TODO: set start val to .1

                with ui.HStack():
                    ui.Label("Antialias", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.CheckBox(name="attribute_bool")  # TODO: Maybe use switch instead of checkbox here?

                with ui.HStack():
                    ui.Label("Ambient Occlusion", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.CheckBox(name="attribute_bool")

                with ui.HStack():
                    ui.Label("Ambient Distance", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    # TODO: Figure out how to do just 2 here, and name them differently
                    ui.MultiFloatDragField(0.0, 20.0, 0.0, h_spacing=SPACING, name="attribute_vector")

                with ui.HStack():
                    ui.Label("Ambient Falloff", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.ComboBox()  # TODO Customize this

                with ui.HStack():
                    ui.Label("Background Color", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    # The custom compound widget
                    ColorWidget(0.25, 0.5, 0.75)

                with ui.HStack():
                    ui.Label("Render Method", name="attribute_name", width=self.label_width)

                with ui.HStack():
                    ui.Label("Path Traced", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.CheckBox(name="attribute_bool")  # TODO Turn these into Radio buttons instead

                with ui.HStack():
                    ui.Label("Volumetric", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.CheckBox(name="attribute_bool")

                with ui.HStack():
                    ui.Label("Export Path", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    ui.StringField(name="attribute_bool")
                    ui.Button("Export")

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame(name="window_bg"):
            with ui.VStack(height=0):
                self._build_calculations()
                self._build_parameters()
                self._build_light_1()
                self._build_scene()
