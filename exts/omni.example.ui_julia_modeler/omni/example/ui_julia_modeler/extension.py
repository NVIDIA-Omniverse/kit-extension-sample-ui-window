# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["JuliaModelerExtension"]

import asyncio
from functools import partial

import omni.ext
import omni.kit.ui
import omni.ui as ui

from .style import WIN_WIDTH, WIN_HEIGHT
from .window import JuliaModelerWindow


class JuliaModelerExtension(omni.ext.IExt):
    """The entry point for Julia Modeler Example Window."""

    WINDOW_NAME = "Julia Quaternion Modeler"
    MENU_PATH = f"Window/{WINDOW_NAME}"

    def on_startup(self):
        # The ability to show the window if the system requires it. We use it
        # in QuickLayout.
        ui.Workspace.set_show_window_fn(JuliaModelerExtension.WINDOW_NAME, partial(self.show_window, None))

        # Add the new menu
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(
                JuliaModelerExtension.MENU_PATH, self.show_window, toggle=True, value=True
            )

        # Show the window. It will call `self.show_window`
        ui.Workspace.show_window(JuliaModelerExtension.WINDOW_NAME)

    def on_shutdown(self):
        self._menu = None
        if self._window:
            self._window.destroy()
            self._window = None

        # Deregister the function that shows the window from omni.ui
        ui.Workspace.set_show_window_fn(JuliaModelerExtension.WINDOW_NAME, None)

    def _set_menu(self, value):
        """Set the menu to create this window on and off"""
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(JuliaModelerExtension.MENU_PATH, value)

    async def _destroy_window_async(self):
        # wait one frame, this is due to the one frame defer
        # in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._window:
            self._window.destroy()
            self._window = None

    def _visiblity_changed_fn(self, visible):
        # Called when the user presses "X"
        self._set_menu(visible)
        if not visible:
            # Destroy the window, since we are creating a new window
            # in show_window
            asyncio.ensure_future(self._destroy_window_async())

    def show_window(self, menu, value):
        if value:
            self._window = JuliaModelerWindow(
                JuliaModelerExtension.WINDOW_NAME, width=WIN_WIDTH, height=WIN_HEIGHT)
            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
        elif self._window:
            self._window.visible = False
