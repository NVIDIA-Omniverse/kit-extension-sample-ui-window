# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["CustomColorWidget"]

from ctypes import Union
import re
from typing import List, Optional

import omni.ui as ui

from .custom_base_widget import CustomBaseWidget
from .style import BLOCK_HEIGHT

COLOR_PICKER_WIDTH = ui.Percent(35)
FIELD_WIDTH = ui.Percent(65)
COLOR_WIDGET_NAME = "color_block"
SPACING = 4


class CustomColorWidget(CustomBaseWidget):
    """The compound widget for color input"""

    def __init__(self, *args, model=None, **kwargs):

        self.__defaults: List[Union[float, int]] = [a for a in args if a is not None]
        self.__strfield: Optional[ui.StringField] = None
        self.__colorpicker: Optional[ui.ColorWidget] = None
        self.__color_sub = None
        self.__strfield_sub = None

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__strfield = None
        self.__colorpicker = None
        self.__color_sub = None
        self.__strfield_sub = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__colorpicker:
            return self.__colorpicker.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__colorpicker.model = value

    @staticmethod
    def simplify_str(val):
        s = str(round(val, 3))
        s_clean = re.sub(r'0*$', '', s)  # clean trailing 0's
        s_clean = re.sub(r'[.]$', '', s_clean)  # clean trailing .
        s_clean = re.sub(r'^0', '', s_clean)  # clean leading 0
        return s_clean

    def set_color_stringfield(self, item_model, children):
        field_str = ", ".join([self.simplify_str(item_model.get_item_value_model(c).as_float)
                               for c in children])
        self.__strfield.model.set_value(field_str)
        if self.revert_img:
            self._on_value_changed()

    def set_color_widget(self, str_model, children):
        """Parse the new StringField value and set the ui.ColorWidget component items
        to the new values.

        Args:
            str_model (_type_): SimpleStringModel for the StringField
            children (_type_): Children of the ui.ColorWidget's model
        """
        joined_str = str_model.get_value_as_string()
        for model, comp_str in zip(children, joined_str.split(",")):
            comp_str_clean = comp_str.strip()
            try:
                self.__colorpicker.model.get_item_value_model(model).as_float = float(comp_str_clean)
            except ValueError:
                # Usually in the middle of typing, but may want better error if still
                # a problem after losing focus.
                pass

    def _on_value_changed(self, *args):
        default_str = ", ".join([self.simplify_str(val) for val in self.__defaults])
        cur_str = self.__strfield.model.as_string
        self.revert_img.enabled = default_str != cur_str

    def _restore_default(self):
        if self.revert_img.enabled:
            field_str = ", ".join([self.simplify_str(val) for val in self.__defaults])
            self.__strfield.model.set_value(field_str)
            self.revert_img.enabled = False

    def _build_body(self):
        with ui.HStack(spacing=SPACING):
            # The construction of the widget depends on what the user provided,
            # defaults or a model
            if self.existing_model:
                # the user provided a model
                self.__colorpicker = ui.ColorWidget(self.existing_model, width=COLOR_PICKER_WIDTH, height=BLOCK_HEIGHT,
                                                    name=COLOR_WIDGET_NAME)
                color_model = self.existing_model
            else:
                # the user provided a list of default values
                self.__colorpicker = ui.ColorWidget(*self.__defaults, width=COLOR_PICKER_WIDTH, height=BLOCK_HEIGHT,
                                                    name=COLOR_WIDGET_NAME)
                color_model = self.__colorpicker.model

            self.__strfield = ui.StringField(width=FIELD_WIDTH, name="attribute_color")
            self.__color_sub = self.__colorpicker.model.subscribe_item_changed_fn(
                lambda m, _, children=color_model.get_item_children(): self.set_color_stringfield(m, children))
            self.__strfield_sub = self.__strfield.model.subscribe_value_changed_fn(
                lambda m, children=color_model.get_item_children():
                    self.set_color_widget(m, children))
            self.set_color_stringfield(self.__colorpicker.model,
                                       children=color_model.get_item_children())  # show data at the start
