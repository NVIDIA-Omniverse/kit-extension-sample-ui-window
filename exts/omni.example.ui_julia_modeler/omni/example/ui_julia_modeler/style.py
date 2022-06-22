# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["example_window_style"]

from ctypes import alignment
from omni.ui import color as cl
from omni.ui import constant as fl
from omni.ui import url
import omni.kit.app
import omni.ui as ui
import pathlib

EXTENSION_FOLDER_PATH = pathlib.Path(
    omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__)
)

# Pre-defined constants. It's possible to change them runtime.
cl.example_window_attribute_bg = cl("#1f2124")
cl.example_window_attribute_fg = cl.red
# cl.example_window_attribute_fg = cl("#0f1115")
cl.example_window_hovered = cl("#FFFFFF")
cl.example_window_text = cl("#CCCCCC")
fl.example_window_attr_hspacing = 10
fl.example_window_attr_spacing = 1
fl.example_window_group_spacing = 2
url.example_window_icon_closed = f"{EXTENSION_FOLDER_PATH}/data/closed.svg"
url.example_window_icon_opened = f"{EXTENSION_FOLDER_PATH}/data/opened.svg"
url.slider_bg_texture = f"{EXTENSION_FOLDER_PATH}/data/diagonal_texture_tmp.png"

fl.example_border_radius = 3

# The main style dict
example_window_style = {
    "Label::attribute_name": {
        "alignment": ui.Alignment.RIGHT_CENTER,
        "margin_height": fl.example_window_attr_spacing,
        "margin_width": fl.example_window_attr_hspacing,
    },
    "Label::attribute_name:hovered": {"color": cl.example_window_hovered},
    "Label::collapsable_name": {"alignment": ui.Alignment.LEFT_CENTER},
    "Slider::attribute_int:hovered": {"color": cl.example_window_hovered},
    "Slider": {
        "background_color": cl.example_window_attribute_bg,
        "draw_mode": ui.SliderDrawMode.HANDLE,
    },
    "Slider::attribute_float": {
        "draw_mode": ui.SliderDrawMode.FILLED,
        "secondary_color": cl.example_window_attribute_fg,
    },
    "Slider::attribute_float:hovered": {"color": cl.example_window_hovered},
    "Slider::attribute_vector:hovered": {"color": cl.example_window_hovered},
    "Slider::attribute_color:hovered": {"color": cl.example_window_hovered},

    "ColorWidget::color_block": {"border_width": 0, "border_radius": fl.example_border_radius},
    "Field::attribute_color": {
        "background_color": cl(0.18, 0.18, 0.18, 1.0),
        "padding_width": 30,
        "border_radius": fl.example_border_radius,
        "border_color": cl(1.0, 1.0, 1.0, 0.3),
        "border_width": 1,
        "font_size": 12,
    },
    "CollapsableFrame::group": {"margin_height": fl.example_window_group_spacing},
    "Image::collapsable_opened": {"color": cl.example_window_text, "image_url": url.example_window_icon_opened},
    "Image::collapsable_closed": {"color": cl.example_window_text, "image_url": url.example_window_icon_closed},
    "Image::slider_bg_texture": {
        "image_url": url.slider_bg_texture,
        "border_radius": fl.example_border_radius,
        "corner_flag": ui.CornerFlag.LEFT,
    },
    "Slider::attr_slider": {
        "draw_mode": ui.SliderDrawMode.FILLED,
        # "margin": 0,
        "padding": 0,
        "color": cl(0.0, 0.0, 0.0, 0.0),  # Turn off text
        "background_color": cl(0.28, 0.28, 0.28, 0.01),
        "secondary_color": cl(1.0, 1.0, 1.0, .3),
        "border_radius": fl.example_border_radius,
        "corner_flag": ui.CornerFlag.LEFT,
    },
    "Field::attr_field": {
        "background_color": cl(0.18, 0.18, 0.18, 1.0),
        "padding_width": 30,
        # "padding_height": 0,
        "border_radius": fl.example_border_radius,
        "border_color": cl(1.0, 1.0, 1.0, 0.3),
        "border_width": 1,
        "corner_flag": ui.CornerFlag.RIGHT,
        "font_size": 12,
    },
    # TODO: make hover state for Field::attr_field that keeps the border on rather than disappearing, and keeps bg color the same
    "HeaderLine": {"color": cl(.5, .5, .5, .5)},
    "ScrollingFrame::window_bg": {"background_color": cl(0.2, 0.2, 0.2, 1.0)},
}
