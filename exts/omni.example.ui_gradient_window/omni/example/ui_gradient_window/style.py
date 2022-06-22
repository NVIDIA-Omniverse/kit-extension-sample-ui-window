# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["main_window_style"]

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
fl_attr_hspacing = 10
fl_attr_spacing = 1
fl_group_spacing = 5

cl_attribute_dark = cl("#202324")
cl_attribute_red = cl("#ac6060")
cl_attribute_green = cl("#60ab7c")
cl_attribute_blue = cl("#35889e")
cl_line = cl("#404040")
cl_text_blue = cl("#5eb3ff")
cl_text_gray = cl("#707070")
cl_text = cl("#a1a1a1")
cl_text_hovered = cl("#ffffff")
cl_field_text = cl("#5f5f5f")
cl_widget_background = cl("#1f2123")
cl_attribute_default = cl("#505050")
cl_attribute_changed = cl("#55a5e2")
cl_slider = cl("#383b3e")
cl_combobox_background = cl("#252525")
cl_main_background = cl("#2a2b2c")

cls_temperature_gradient = [cl("#fe0a00"), cl("#f4f467"), cl("#a8b9ea"), cl("#2c4fac"), cl("#274483"), cl("#1f334e")]
cls_color_gradient = [cl("#fa0405"), cl("#95668C"), cl("#4b53B4"), cl("#33C287"), cl("#9fE521"), cl("#ff0200")]
cls_tint_gradient = [cl("#1D1D92"), cl("#7E7EC9"), cl("#FFFFFF")]
cls_grey_gradient = [cl("#020202"), cl("#525252"), cl("#FFFFFF")]
cls_button_gradient = [cl("#232323"), cl("#656565")]


# The main style dict
main_window_style = {
    "Button::add": {"background_color": cl_widget_background},
    "Field::add": { "font_size": 14, "color": cl_text},
    "Field::search": { "font_size": 16, "color": cl_field_text},
    "Field::path": { "font_size": 14, "color": cl_field_text},

    "ScrollingFrame::main_frame": {"background_color": cl_main_background},
    "CollapsableFrame::group": {
        "margin_height": fl_group_spacing,
        "background_color": 0x0,
        "secondary_color": 0x0,
    },
    "CollapsableFrame::group:hovered": {
        "margin_height": fl_group_spacing,
        "background_color": 0x0,
        "secondary_color": 0x0,
    },

    "Circle::group_circle": {
        "background_color": cl_line,
    },

    "Circle::slider_handle":{"background_color": 0x0, "border_width": 2, "border_color": cl_combobox_background},

    "Line::group_line": {"color": cl_line},

    "Label::collapsable_name": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_text
        },

    "Label::attribute_bool": {
        "alignment": ui.Alignment.LEFT_BOTTOM,
        "margin_height": fl_attr_spacing,
        "margin_width": fl_attr_hspacing,
        "color": cl_text
    },
    
    "Label::attribute_name": {
        "alignment": ui.Alignment.RIGHT_CENTER,
        "margin_height": fl_attr_spacing,
        "margin_width": fl_attr_hspacing,
        "color": cl_text
    },
    "Label::attribute_name:hovered": {"color": cl_text_hovered},

    "Label::header_attribute_name": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_text
    },

    "Label::details": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_text_blue,
        "font_size": 19,
    },

    "Label::layers": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_text_gray,
        "font_size": 19,
    },

    "Label::attribute_r": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_attribute_red
    },
    "Label::attribute_g": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_attribute_green
    },
    "Label::attribute_b": {
        "alignment": ui.Alignment.LEFT_CENTER,
        "color": cl_attribute_blue
    },

    "Slider::float_slider":{
        "background_color": cl_widget_background,
        "secondary_color": cl_slider,
        "border_radius": 3,
        "corner_flag": ui.CornerFlag.ALL,
        "draw_mode": ui.SliderDrawMode.FILLED,
    },

    "Image::pin": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/Pin.svg"},
    "Image::expansion": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/Details_options.svg"},
    "Image::transform": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/offset_dark.svg"},
    "Image::link": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/link_active_dark.svg"},
    "Image::on_off": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/on_off.svg"},

    "Rectangle::attribute_changed": {"background_color":cl_attribute_changed, "border_radius": 2},
    "Rectangle::attribute_default": {"background_color":cl_attribute_default, "border_radius": 1},

    "Image::header_frame": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/head.png"},
    "Image::checked": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/checked.svg"},
    "Image::unchecked": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/unchecked.svg"},

    "Image::separator":{"image_url": f"{EXTENSION_FOLDER_PATH}/icons/separator.svg"},

    "Image::collapsable_opened": {"color": cl_text, "image_url": f"{EXTENSION_FOLDER_PATH}/icons/closed.svg"},
    "Image::collapsable_closed": {"color": cl_text, "image_url": f"{EXTENSION_FOLDER_PATH}/icons/open.svg"},
    "Image::combobox": {"image_url": f"{EXTENSION_FOLDER_PATH}/icons/combobox_bg.svg"},

    "ComboBox::dropdown_menu":{
        "color": cl_text,  # label color
        "background_color": cl_combobox_background,
        "secondary_color": 0x0, # button background color
    },

    "ImageWithProvider::gradient_slider":{"border_radius": 4, "corner_flag": ui.CornerFlag.ALL},
    "ImageWithProvider::button_background_gradient": {"border_radius": 3, "corner_flag": ui.CornerFlag.ALL},
}

def hex_to_color(hex: int) -> tuple:
    # convert Value from int
    red = hex & 255
    green = (hex >> 8) & 255
    blue = (hex >> 16) & 255
    alpha = (hex >> 24) & 255
    rgba_values = [red, green, blue, alpha]
    return rgba_values

def _interpolate_color(hex_min: int, hex_max: int, intep):
    max_color = hex_to_color(hex_max)
    min_color = hex_to_color(hex_min)
    color = [int((max - min) * intep) + min for max, min in zip(max_color, min_color)]
    return (color[3] << 8 * 3) + (color[2] << 8 * 2) + (color[1] << 8 * 1) + color[0]

def get_gradient_color(value, max, colors):
    step_size = len(colors) - 1
    step = 1.0/float(step_size)
    percentage = value / float(max)

    idx = (int) (percentage / step)
    if idx == step_size:
        color = colors[-1]
    else:
        color = _interpolate_color(colors[idx], colors[idx+1], percentage)
    return color

def generate_byte_data(colors):
    data = []
    for color in colors:
        data += hex_to_color(color)

    _byte_provider = ui.ByteImageProvider()
    _byte_provider.set_bytes_data(data, [len(colors), 1])
    return _byte_provider

def build_gradient_image(colors, height, style_name):
    byte_provider = generate_byte_data(colors)
    ui.ImageWithProvider(byte_provider,fill_policy=omni.ui.IwpFillPolicy.IWP_STRETCH, height=height, name=style_name)
    return byte_provider