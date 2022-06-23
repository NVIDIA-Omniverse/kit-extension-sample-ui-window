# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["CustomRadioCollection"]

from typing import List, Optional

import omni.ui as ui

from .style import ATTR_LABEL_HEIGHT, ATTR_LABEL_WIDTH

SPACING = 5


class CustomRadioCollection:
    """A custom collection of radio buttons"""

    def __init__(self,
                 group_name: str,
                 labels: List[str],
                 model: ui.AbstractItemModel = None,
                 default_value: bool = True,
                 **kwargs):
        self.__group_name = group_name
        self.__labels = labels
        self.__default_val = default_value
        self.__images = []
        self.__selection_model = ui.SimpleIntModel(default_value)
        self.__frame = ui.Frame()
        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__images = []
        self.__selection_model = None
        self.__frame = None

    @property
    def model(self) -> Optional[ui.AbstractValueModel]:
        """The widget's model"""
        if self.__selection_model:
            return self.__selection_model

    @model.setter
    def model(self, value: int):
        """The widget's model"""
        self.__selection_model.set(value)

    def __getattr__(self, attr):
        """
        Pretend it's self.__frame, so we have access to width/height and
        callbacks.
        """
        return getattr(self.__frame, attr)

    def _on_value_changed(self, index: int = 0):
        self.__selection_model.set_value(index)
        for i, img in enumerate(self.__images):
            img.checked = i == index
            img.name = "radio_on" if img.checked else "radio_off"

    def _build_fn(self):

        with ui.VStack(spacing=SPACING):
            ui.Spacer(height=2)
            ui.Label(self.__group_name.upper(), name="radio_group_name",
                     width=ATTR_LABEL_WIDTH, height=ATTR_LABEL_HEIGHT)

            for i, label in enumerate(self.__labels):
                with ui.HStack():
                    ui.Label(label, name="attribute_name",
                             width=ATTR_LABEL_WIDTH, height=ATTR_LABEL_HEIGHT)

                    with ui.HStack():
                        with ui.VStack():
                            ui.Spacer(height=2)
                            self.__images.append(
                                ui.Image(name=("radio_on" if self.__default_val == i
                                                          else "radio_off"),
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                                         height=16, width=16, checked=self.__default_val)
                            )
                        ui.Spacer()
            ui.Spacer(height=2)

        for i in range(len(self.__labels)):
            self.__images[i].set_mouse_pressed_fn(lambda x, y, b, m, i=i: self._on_value_changed(i))
