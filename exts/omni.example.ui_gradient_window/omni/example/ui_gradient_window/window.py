# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved./icons/
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["PropertyWindowExample"]

from ast import With
from ctypes import alignment
import omni.kit
import omni.ui as ui
from .style import main_window_style, get_gradient_color, build_gradient_image
from .style import cl_combobox_background, cls_temperature_gradient, cls_color_gradient, cls_tint_gradient, cls_grey_gradient, cls_button_gradient
from .color_widget import ColorWidget
from .collapsable_widget import CustomCollsableFrame, build_collapsable_header

LABEL_WIDTH = 120
SPACING = 10


def _get_plus_glyph():
    return omni.kit.ui.get_custom_glyph_code("${glyphs}/menu_context.svg")

def _get_search_glyph():
    return omni.kit.ui.get_custom_glyph_code("${glyphs}/menu_search.svg")


class PropertyWindowExample(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        # Apply the style to all the widgets of this window
        self.frame.style = main_window_style
        # Set the function that is called to build widgets when the window is visible
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

    def _build_transform(self):
        """Build the widgets of the "Calculations" group"""
        with ui.ZStack():
            with ui.VStack():
                ui.Spacer(height=5)
                with ui.HStack():
                    ui.Spacer()
                    ui.Image(name="transform", fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, width=24, height=24)
                    ui.Spacer(width=30)
                ui.Spacer()
            with CustomCollsableFrame("TRANSFORMS").collapsable_frame:
                with ui.VStack(height=0, spacing=SPACING):
                    ui.Spacer(height=2)
                    self._build_vector_widget("Position", 70)
                    self._build_vector_widget("Rotation", 70)
                    with ui.ZStack():
                        self._build_vector_widget("Scale", 85)
                        with ui.HStack():
                            ui.Spacer(width=42)
                            ui.Image(name="link", fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, width=20)

    def _build_path(self):
        CustomCollsableFrame("PATH", collapsed=True)

    def _build_light_properties(self):
        """Build the widgets of the "Parameters" group"""
        with CustomCollsableFrame("LIGHT PROPERTIES").collapsable_frame:
            with ui.VStack(height=0, spacing=SPACING):
                ui.Spacer(height=2)
                self._build_combobox("Type", ["Sphere Light", "Disk Light", "Rect Light"])
                self.color_gradient_data, self.tint_gradient_data, self.grey_gradient_data = self._build_color_widget("Color")
                self._build_color_temperature()

                self.diffuse_button_data = self._build_gradient_float_slider("Diffuse Multiplier")
                self.exposture_button_data = self._build_gradient_float_slider("Exposture")
                self.intensity_button_data = self._build_gradient_float_slider("Intensity", default_value=3000, min=0, max=6000)

                self._build_checkbox("Normalize Power", False)
                self._build_combobox("Purpose", ["Default", "Customized"])
                self.radius_button_data = self._build_gradient_float_slider("Radius")

                self._build_shaping()
                self.specular_button_data = self._build_gradient_float_slider("Specular Multiplier")
                self._build_checkbox("Treat As Point")

    def _build_line_dot(self, line_width, height):
        with ui.HStack():
            ui.Spacer(width=10)
            with ui.VStack(width=line_width):
                ui.Spacer(height=height)
                ui.Line(name="group_line", alignment=ui.Alignment.TOP)
            with ui.VStack(width=6):
                ui.Spacer(height=height-2)
                ui.Circle(name="group_circle", width=6, height=6, alignment=ui.Alignment.BOTTOM)          

    def _build_shaping(self):
        """Build the widgets of the "SHAPING" group"""
        with ui.ZStack():
            with ui.HStack():
                ui.Spacer(width=3)
                self._build_line_dot(10, 17)
            with ui.HStack():
                ui.Spacer(width=13)
                with ui.VStack():
                    ui.Spacer(height=17)
                    ui.Line(name="group_line", alignment=ui.Alignment.RIGHT, width=0)
                    ui.Spacer(height=80)
            with ui.CollapsableFrame("          SHAPING", name="group", build_header_fn=build_collapsable_header):
                with ui.VStack(height=0, spacing=SPACING):
                    self.angle_button_data = self._build_gradient_float_slider("Cone Angle")
                    self.softness_button_data = self._build_gradient_float_slider("Cone Softness")
                    self.focus_button_data = self._build_gradient_float_slider("Focus")
                    self.focus_color_data, self.focus_tint_data, self.focus_grey_data  = self._build_color_widget("Focus Tint")

    def _build_vector_widget(self, widget_name, space):
        with ui.HStack():
            ui.Label(widget_name, name="attribute_name", width=0)
            ui.Spacer(width=space)
            # The custom compound widget
            ColorWidget(1.0, 1.0, 1.0, draw_colorpicker=False)
            ui.Spacer(width=10)        

    def _build_color_temperature(self):
        with ui.ZStack():
            with ui.HStack():
                ui.Spacer(width=10)
                with ui.VStack():
                    ui.Spacer(height=8)
                    ui.Line(name="group_line", alignment=ui.Alignment.RIGHT, width=0)
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    self._build_line_dot(10, 8)
                    ui.Label("Enable Color Temperature", name="attribute_name", width=0)
                    ui.Spacer()
                    ui.Image(name="on_off", fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, width=20)
                    rect_changed, rect_default = self.__build_value_changed_widget()

                self.temperature_button_data = self._build_gradient_float_slider("    Color Temperature", default_value=6500.0)
                self.temperature_slider_data = self._build_slider_handle(cls_temperature_gradient)

                with ui.HStack():
                    ui.Spacer(width=10)
                    ui.Line(name="group_line", alignment=ui.Alignment.TOP)

    def _build_color_widget(self, widget_name):
        with ui.ZStack():
            with ui.HStack():
                ui.Spacer(width=10)
                with ui.VStack():
                    ui.Spacer(height=8)
                    ui.Line(name="group_line", alignment=ui.Alignment.RIGHT, width=0)
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    self._build_line_dot(40, 9)
                    ui.Label(widget_name, name="attribute_name", width=0)
                    # The custom compound widget
                    ColorWidget(0.25, 0.5, 0.75)
                    ui.Spacer(width=10)
                color_data = self._build_slider_handle(cls_color_gradient)
                tint_data = self._build_slider_handle(cls_tint_gradient)
                grey_data = self._build_slider_handle(cls_grey_gradient)
                with ui.HStack():
                    ui.Spacer(width=10)
                    ui.Line(name="group_line", alignment=ui.Alignment.TOP)
        return color_data, tint_data, grey_data

    def _build_slider_handle(self, colors):
        handle_Style = {"background_color": colors[0], "border_width": 2, "border_color": cl_combobox_background}
        def set_color(placer, handle, offset):
            # first clamp the value
            max = placer.computed_width - handle.computed_width
            if offset < 0:
                placer.offset_x = 0
            elif offset > max:
                placer.offset_x = max
            color = get_gradient_color(placer.offset_x.value, max, colors)
            handle_Style.update({"background_color": color})
            handle.style = handle_Style

        with ui.HStack():
            ui.Spacer(width=18)
            with ui.ZStack():
                with ui.VStack():
                    ui.Spacer(height=3)
                    byte_provider = build_gradient_image(colors, 8, "gradient_slider")
                with ui.HStack():
                    handle_placer = ui.Placer(draggable=True, drag_axis=ui.Axis.X, offset_x=0)
                    with handle_placer:
                        handle = ui.Circle(width=15, height=15, style=handle_Style)
                    handle_placer.set_offset_x_changed_fn(lambda offset: set_color(handle_placer, handle, offset.value))
            ui.Spacer(width=22)
        return byte_provider

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame(name="main_frame"):
            with ui.VStack(height=0, spacing=SPACING):
                self._build_head()
                self._build_transform()
                self._build_path()
                self._build_light_properties()
                ui.Spacer(height=30)

    def _build_head(self):
        with ui.ZStack():
            ui.Image(name="header_frame", height=150,  fill_policy=ui.FillPolicy.STRETCH)
            with ui.HStack():
                ui.Spacer(width=12)
                with ui.VStack(spacing=8):
                    self._build_tabs()
                    ui.Spacer(height=1)
                    self._build_selection_widget()
                    self._build_stage_path_widget()
                    self._build_search_field()
                ui.Spacer(width=12)

    def _build_tabs(self):
        with ui.HStack(height=35):
            ui.Label("DETAILS", width=ui.Percent(17), name="details")
            with ui.ZStack():
                ui.Image(name="combobox", fill_policy=ui.FillPolicy.STRETCH, height=35)
                with ui.HStack():
                    ui.Spacer(width=15)
                    ui.Label("LAYERS      |    ", name="layers", width=0)
                    ui.Label(f"{_get_plus_glyph()}", width=0)
                    ui.Spacer()
                    ui.Image(name="pin", width=20)

    def _build_selection_widget(self):
        with ui.HStack(height=20):
            add_button = ui.Button(f"{_get_plus_glyph()} Add", width=60, name="add")
            ui.Spacer(width=14)
            ui.StringField(name="add").model.set_value("(2 models selected)")
            ui.Spacer(width=8)
            ui.Image(name="expansion", width=20)

    def _build_stage_path_widget(self):
        with ui.HStack(height=20):
            ui.Spacer(width=3)
            ui.Label("Stage Path", name="header_attribute_name", width=70)
            ui.StringField(name="path").model.set_value("/World/environment/tree")

    def _build_search_field(self):
        with ui.HStack():
            ui.Spacer(width=2)
            # would add name="search" style, but there is a bug to use glyph together with style
            # make sure the test passes for now
            ui.StringField(height=23).model.set_value(f"{_get_search_glyph()} Search")

    def _build_checkbox(self, label_name, default_value=True):
        def _restore_default(rect_changed, rect_default):
            image.name = "checked" if default_value else "unchecked"

            rect_changed.visible = False
            rect_default.visible = True
        
        def _on_value_changed(image, rect_changed, rect_default):
            image.name = "unchecked" if image.name == "checked" else "checked"

            if (default_value and image.name == "unchecked") or (not default_value and image.name == "checked"):
                rect_changed.visible = True
                rect_default.visible = False
            else:
                rect_changed.visible = False
                rect_default.visible = True

        with ui.HStack():
            ui.Label(label_name, name=f"attribute_bool", width=self.label_width, height=20)
            name = "checked" if default_value else "unchecked"
            image =ui.Image(name=name, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, height=18, width=18)
            ui.Spacer()
            rect_changed, rect_default = self.__build_value_changed_widget()
            image.set_mouse_pressed_fn(lambda x, y, b, m: _on_value_changed(image, rect_changed, rect_default))  

            # add call back to click the rect_changed to restore the default value
            rect_changed.set_mouse_pressed_fn(lambda x, y, b, m: _restore_default(rect_changed, rect_default))

    def __build_value_changed_widget(self):
        with ui.VStack(width=20):
            ui.Spacer(height=3)
            rect_changed = ui.Rectangle(name="attribute_changed", width=15, height=15, visible= False)
            ui.Spacer(height=4)
            with ui.HStack():
                ui.Spacer(width=3)
                rect_default = ui.Rectangle(name="attribute_default", width=5, height=5, visible= True)
        return rect_changed, rect_default    

    def _build_gradient_float_slider(self, label_name, default_value=0, min=0, max=1):
        def _on_value_changed(model, rect_changed, rect_defaul):
            if model.as_float == default_value:
                rect_changed.visible = False
                rect_defaul.visible = True
            else:
                rect_changed.visible = True
                rect_defaul.visible = False

        def _restore_default(slider):
            slider.model.set_value(default_value)

        with ui.HStack():
            ui.Label(label_name, name=f"attribute_name", width=self.label_width)
            with ui.ZStack():
                button_background_gradient = build_gradient_image(cls_button_gradient, 22, "button_background_gradient")
                with ui.VStack():
                    ui.Spacer(height=1.5)
                    with ui.HStack():
                        slider = ui.FloatSlider(name="float_slider", height=0, min=min, max=max)
                        slider.model.set_value(default_value)
                        ui.Spacer(width=1.5)
            ui.Spacer(width=4)
            rect_changed, rect_default = self.__build_value_changed_widget()
            # switch the visibility of the rect_changed and rect_default to indicate value changes
            slider.model.add_value_changed_fn(lambda model: _on_value_changed(model, rect_changed, rect_default))
            # add call back to click the rect_changed to restore the default value
            rect_changed.set_mouse_pressed_fn(lambda x, y, b, m: _restore_default(slider))
        return button_background_gradient

    def _build_combobox(self, label_name, options):
        def _on_value_changed(model, rect_changed, rect_defaul):
            index = model.get_item_value_model().get_value_as_int()
            if index == 0:
                rect_changed.visible = False
                rect_defaul.visible = True
            else:
                rect_changed.visible = True
                rect_defaul.visible = False
        def _restore_default(combo_box):
            combo_box.model.get_item_value_model().set_value(0)
        with ui.HStack():
            ui.Label(label_name, name=f"attribute_name", width=self.label_width)
            with ui.ZStack():
                ui.Image(name="combobox", fill_policy=ui.FillPolicy.STRETCH, height=35)
                with ui.HStack():
                    ui.Spacer(width=10)
                    with ui.VStack():
                        ui.Spacer(height=10)
                        option_list = list(options)
                        combo_box = ui.ComboBox(0, *option_list, name="dropdown_menu")
            with ui.VStack(width=0):
                ui.Spacer(height=10)
                rect_changed, rect_default = self.__build_value_changed_widget()
            # switch the visibility of the rect_changed and rect_default to indicate value changes
            combo_box.model.add_item_changed_fn(lambda m, i: _on_value_changed(m, rect_changed, rect_default))
            # add call back to click the rect_changed to restore the default value
            rect_changed.set_mouse_pressed_fn(lambda x, y, b, m: _restore_default(combo_box))
