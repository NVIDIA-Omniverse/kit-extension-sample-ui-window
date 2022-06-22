# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["SliderWidget"]

from ctypes import Union, alignment
from typing import List, Optional
import omni.ui as ui

NUM_FIELD_WIDTH = 50  # TODO: change to field width or something else?
SLIDER_WIDTH = ui.Percent(100)  # TODO: change to field width or something else?
FIELD_HEIGHT = 17  # TODO: why doesn't height of anything change?
SPACING = 4
TEXTURE_NAME = "slider_bg_texture"


class SliderWidget:
    """A compound widget for scalar slider input"""

    def __init__(self, # *args,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=1.0,
                 display_range: bool = False,
                 **kwargs):
        # self.__defaults: List[Union[float, int]] = args
        self.__model: Optional[ui.AbstractItemModel] = kwargs.pop("model", None)

        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None

        self.__frame = ui.Frame()

        self.__min = min
        self.__max = max
        self.__num_type = num_type
        self.__display_range = display_range

        with self.__frame:
            self._build_fn()

    def destroy(self):
        self.__model = None
        self.__slider = None
        self.__numberfield = None
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
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _build_fn(self):
        with ui.HStack(spacing=0):
            # The construction of multi field depends on what the user provided,
            # defaults or a model
            if self.__model:
                # TODO: implement this part still

                # the user provided a model
                self.__slider = ui.MultiFloatDragField(
                    min=self.__min, max=self.__max, model=self.__model, name="attr_slider"
                )
                model = self.__model

            else:
                # the user provided a list of default values
                with ui.VStack(spacing=3):
                    with ui.ZStack():
                        # Put texture image here, with rounded corners, then make slider bg be fully transparent,
                        # and fg be gray and partially transparent
                        ui.Image(name=TEXTURE_NAME, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT,
                                 width=SLIDER_WIDTH, height=FIELD_HEIGHT,)
                        if self.__num_type == "float":
                            self.__slider = ui.FloatSlider(
                                width=SLIDER_WIDTH,
                                height=FIELD_HEIGHT,
                                min=self.__min, max=self.__max, name="attr_slider"
                            )
                        else:
                            self.__slider = ui.IntSlider(
                                width=SLIDER_WIDTH,
                                height=FIELD_HEIGHT,
                                min=self.__min, max=self.__max, name="attr_slider"
                            )
                    if self.__display_range:
                        with ui.HStack():
                            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, style={"font_size": 10})
                            ui.Spacer()
                            # TODO: Need to add support for a middle value (always 0?), but it may or may not be
                            #       centered, depending on the min/max values.
                            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, style={"font_size": 10})
                        ui.Spacer(height=.75)

                with ui.VStack():
                    model = self.__slider.model
                    field_cls = ui.FloatField if self.__num_type == "float" else ui.IntField
                    self.__numberfield = field_cls(model, width=NUM_FIELD_WIDTH, height=FIELD_HEIGHT, name="attr_field")
                    if self.__display_range:
                        ui.Spacer()
