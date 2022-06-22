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

COLOR_PICKER_WIDTH = 20
SPACING = 4


class ColorWidget:
    """The compound widget for color input"""

    def __init__(self, *args, model=None, **kwargs):
        self.__defaults: List[Union[float, int]] = args
        self.__model: Optional[ui.AbstractItemModel] = kwargs.pop("model", None)

        self.__multifield: Optional[ui.MultiFloatDragField] = None
        self.__colorpicker: Optional[ui.ColorWidget] = None

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
                self.__multifield = ui.MultiFloatDragField(
                    *self.__defaults, min=0, max=1, h_spacing=SPACING, name="attribute_color"
                )
                model = self.__multifield.model

            self.__colorpicker = ui.ColorWidget(model, width=COLOR_PICKER_WIDTH)
