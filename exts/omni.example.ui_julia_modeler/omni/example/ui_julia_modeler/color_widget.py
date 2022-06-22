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
import re
from typing import List, Optional

import omni.ui as ui

COLOR_PICKER_WIDTH = 115
FIELD_WIDTH = 70
COLOR_WIDGET_NAME = "color_block"
SPACING = 4


class ColorWidget:
    """The compound widget for color input"""

    def __init__(self, *args, model=None, **kwargs):
        self.__defaults: List[Union[float, int]] = args
        self.__model: Optional[ui.AbstractItemModel] = kwargs.pop("model", None)

        self.__strfield: Optional[ui.StringField] = None
        self.__colorpicker: Optional[ui.ColorWidget] = None
        self.__color_sub = None

        self.__frame = ui.Frame()
        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__model = None
        self.__strfield = None
        self.__colorpicker = None
        self.__color_sub = None
        self.__frame = None

    def __getattr__(self, attr):
        """
        Pretend it's self.__frame, so we have access to width/height and
        callbacks.
        """
        return getattr(self.__frame, attr)

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__colorpicker:
            return self.__colorpicker.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        # TODO: this won't work the same way for both now
        # self.__strfield.model = value
        self.__colorpicker.model = value

    def set_color_stringfield(self, item_model, item):

        def clean_trailing_zeros(_str):
            return re.sub(r'0*$', '', _str)

        print(f"In set_color_stringfield - item_model: {item_model}  {item}")
        sub_models = item_model.get_item_children(item)
        print(f"submodels: {sub_models}")
        print(f"current value changed: {item_model.get_item_value_model(item).as_float}")
        # field_str = ", ".join([clean_trailing_zeros(item_model.get_item_value_model(m).as_string)
        #                        for m in sub_models])
        # print(f"New field str to set: {args[0]}")
        self.__strfield.model.set_value("hello")  # set to field_str

    def _build_fn(self):

        def set_color_widget(item_model, joined_str):
            for m in joined_str.split(", "):
                item_model.get_item_value_model(m).as_string = m

        with ui.HStack(spacing=SPACING):
            # The construction of multi field depends on what the user provided,
            # defaults or a model
            if self.__model:
                # the user provided a model
                self.__colorpicker = ui.ColorWidget(self.__model, width=COLOR_PICKER_WIDTH,
                                                    name=COLOR_WIDGET_NAME)
                # model = self.__model
                # self.__multifield = ui.MultiFloatDragField(
                #     min=0, max=1, model=model, h_spacing=SPACING, name="attribute_color"
                # )
            else:
                # the user provided a list of default values
                self.__colorpicker = ui.ColorWidget(*self.__defaults, width=COLOR_PICKER_WIDTH,
                                                    name=COLOR_WIDGET_NAME)
                # model = self.__colorpicker.model
                # self.__multifield = ui.MultiFloatDragField(
                #     model, min=0, max=1, h_spacing=SPACING, name="attribute_color"
                # )
            # sub_models = model.get_item_children()
            # field_str = ", ".join([clean_trailing_zeros(model.get_item_value_model(m).as_string) for m in sub_models])
            self.__strfield = ui.StringField(width=FIELD_WIDTH, name="attribute_color")
            self.__color_sub = self.__colorpicker.model.subscribe_item_changed_fn(self.set_color_stringfield)
            # self.__strfield.model.add_value_changed_fn(lambda: set_color_widget())  #m, i))
