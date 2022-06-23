# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["JuliaModelerWindow"]

import omni.ui as ui

from .custom_bool_widget import CustomBoolWidget
from .custom_color_widget import CustomColorWidget
from .custom_combobox_widget import CustomComboboxWidget
from .custom_multifield_widget import CustomMultifieldWidget
from .custom_radio_collection import CustomRadioCollection
from .custom_slider_widget import CustomSliderWidget
from .style import example_window_style, ATTR_LABEL_HEIGHT, ATTR_LABEL_WIDTH, BLOCK_HEIGHT

SPACING = 5


# TODO: rename class and __all__ above
class JuliaModelerWindow(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = ATTR_LABEL_WIDTH

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

    def _build_title(self):
        with ui.VStack():
            ui.Spacer(height=10)
            ui.Label("JULIA QUATERNION MODELER - 1.0", name="window_title")
            ui.Spacer(height=10)

    def _build_collapsable_header(self, collapsed, title):
        """Build a custom title of CollapsableFrame"""
        with ui.VStack():
            ui.Spacer(height=8)
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

                CustomSliderWidget(min=0, max=20, num_type="int",
                                   label="Precision", default_val=6)

                CustomSliderWidget(min=0, max=20, num_type="int",
                                   label="Iterations", default_val=10)

    def _build_parameters(self):
        """Build the widgets of the "Parameters" group"""
        with ui.CollapsableFrame("Parameters".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                CustomSliderWidget(min=-2, max=2, display_range=True,
                                   label="Iterations", default_val=0.75)

                CustomSliderWidget(min=0, max=2, display_range=True,
                                   label="i", default_val=0.65)

                CustomSliderWidget(min=0, max=2, display_range=True,
                                   label="j", default_val=0.25)

                CustomSliderWidget(min=0, max=2, display_range=True,
                                   label="k", default_val=0.55)

                CustomSliderWidget(min=0, max=3.14, display_range=True,
                                   label="Theta", default_val=1.25)

    def _build_light_1(self):
        """Build the widgets of the "Light 1" group"""
        with ui.CollapsableFrame("Light 1".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                CustomMultifieldWidget(
                    label="Orientation",
                    default_vals=[0.0, 0.0, 0.0]
                )

                CustomSliderWidget(min=0, max=1.75, label="Intensity", default_val=1.75)

                CustomColorWidget(1.0, 0.875, 0.5, label="Color")

                CustomBoolWidget(label="Shadow", default_value=True)

                CustomSliderWidget(min=0, max=2, label="Shadow Softness", default_val=.1)

    def _build_scene(self):
        """Build the widgets of the "Scene" group"""
        with ui.CollapsableFrame("Scene".upper(), name="group",
                                 build_header_fn=self._build_collapsable_header):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=6)

                CustomSliderWidget(min=0, max=160, display_range=True,
                                   num_type="int", label="Field of View", default_val=60)

                CustomMultifieldWidget(
                    label="Orientation",
                    default_vals=[0.0, 0.0, 0.0]
                )

                CustomSliderWidget(min=0, max=2, label="Camera Distance", default_val=.1)

                # TODO: Could use a Switch rather than a checkbox here
                CustomBoolWidget(label="Antialias", default_value=False)

                CustomBoolWidget(label="Ambient Occlusion", default_value=True)

                CustomMultifieldWidget(
                    label="Ambient Distance",
                    sublabels=["Min", "Max"],
                    default_vals=[0.0, 200.0]
                )

                CustomComboboxWidget(label="Ambient Falloff",
                                     options=["Linear", "Quadratic", "Cubic"])

                CustomColorWidget(.6, 0.62, 0.9, label="Background Color")

                CustomRadioCollection("Render Method", labels=["Path Traced", "Volumetric"],
                                      default_value=1)

                with ui.HStack():
                    ui.Label("Export Path", name="attribute_name", width=self.label_width, height=ATTR_LABEL_HEIGHT)
                    pathfield = ui.StringField(name="attribute_color", height=BLOCK_HEIGHT, width=ui.Fraction(2))
                    pathfield.model.set_value(".../export/mesh1.usd")
                    ui.Button("Export", name="tool_button", height=BLOCK_HEIGHT, width=ui.Fraction(1))

                ui.Spacer(height=10)

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame(name="window_bg"):
            with ui.VStack(height=0):
                self._build_title()
                self._build_calculations()
                self._build_parameters()
                self._build_light_1()
                self._build_scene()
