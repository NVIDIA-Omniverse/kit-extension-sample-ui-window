# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["ColorWidget"]

from ctypes import Union
from typing import List, Optional
import omni.ui as ui

from .style import build_gradient_image, cl_attribute_red, cl_attribute_green, cl_attribute_blue, cl_attribute_dark
SPACING = 16


class ColorWidget:
    """The compound widget for color input"""

    def __init__(self, *args, model=None, **kwargs):
        self.__defaults: List[Union[float, int]] = args
        self.__model: Optional[ui.AbstractItemModel] = kwargs.pop("model", None)

        self.__multifield: Optional[ui.MultiFloatDragField] = None
        self.__colorpicker: Optional[ui.ColorWidget] = None

        self.__draw_colorpicker = kwargs.pop("draw_colorpicker", True)

        self.__frame = ui.Frame()
        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__model = None
        self.__multifield = None
        self.__colorpicker = None
        self.__frame = None

    def __getattr__(self, attr):
        """
        Pretend it's self.__frame, so we have access to width/height and
        callbacks.
        """
        return getattr(self.__root_frame, attr)

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__multifield:
            return self.__multifield.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__multifield.model = value
        self.__colorpicker.model = value

    def _build_fn(self):
        def _on_value_changed(model, rect_changed, rect_default):
            if model.get_item_value_model().get_value_as_float() != 0:
                rect_changed.visible = False
                rect_default.visible = True
            else:
                rect_changed.visible = True
                rect_default.visible = False

        def _restore_default(model, rect_changed, rect_default):
            items = model.get_item_children()
            for id, item in enumerate(items):
                model.get_item_value_model(item).set_value(self.__defaults[id])
            
            rect_changed.visible = False
            rect_default.visible = True

        with ui.HStack(spacing=SPACING):
            # The construction of multi field depends on what the user provided,
            # defaults or a model
            if self.__model:
                # the user provided a model
                self.__multifield = ui.MultiFloatDragField(
                    min=0, max=1, model=self.__model, h_spacing=SPACING, name="attribute_color"
                )
                model = self.__model
            else:
                # the user provided a list of default values
                with ui.ZStack():
                    with ui.HStack():
                        self.color_button_gradient_R = build_gradient_image([cl_attribute_dark, cl_attribute_red], 22, "button_background_gradient")
                        ui.Spacer(width=9)
                        with ui.VStack(width=6):
                            ui.Spacer(height=8)
                            ui.Circle(name="group_circle", width=4, height=4)
                        self.color_button_gradient_G = build_gradient_image([cl_attribute_dark, cl_attribute_green], 22, "button_background_gradient")
                        ui.Spacer(width=9)
                        with ui.VStack(width=6):
                            ui.Spacer(height=8)
                            ui.Circle(name="group_circle", width=4, height=4)
                        self.color_button_gradient_B = build_gradient_image([cl_attribute_dark, cl_attribute_blue], 22, "button_background_gradient")
                        ui.Spacer(width=2)
                    with ui.HStack():
                        with ui.VStack():
                            ui.Spacer(height=1)
                            self.__multifield = ui.MultiFloatDragField(
                                *self.__defaults, min=0, max=1, h_spacing=SPACING, name="attribute_color")
                        ui.Spacer(width=3)
                    with ui.HStack(spacing=22):
                        labels = ["R", "G", "B"] if self.__draw_colorpicker else ["X", "Y", "Z"]
                        ui.Label(labels[0], name="attribute_r")
                        ui.Label(labels[1], name="attribute_g")
                        ui.Label(labels[2], name="attribute_b")
                model = self.__multifield.model
            if self.__draw_colorpicker:
                self.__colorpicker = ui.ColorWidget(model, width=0)
            rect_changed, rect_default = self.__build_value_changed_widget()
            model.add_item_changed_fn(lambda model, i: _on_value_changed(model, rect_changed, rect_default))
            rect_changed.set_mouse_pressed_fn(lambda x, y, b, m: _restore_default(model, rect_changed, rect_default))

    def __build_value_changed_widget(self):
        with ui.VStack(width=0):
            ui.Spacer(height=3)
            rect_changed = ui.Rectangle(name="attribute_changed", width=15, height=15, visible= False)
            ui.Spacer(height=4)
            with ui.HStack():
                ui.Spacer(width=3)
                rect_default = ui.Rectangle(name="attribute_default", width=5, height=5, visible= True)
        return rect_changed, rect_default  
