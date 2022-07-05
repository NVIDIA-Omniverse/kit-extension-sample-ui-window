# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["ExampleWindowExtension"]

from .window import ExampleWindow
from functools import partial
import asyncio
import omni.ext
import omni.kit.ui
import omni.ui as ui


class ExampleWindowExtension(omni.ext.IExt):
    """The entry point for Example Window"""

    WINDOW_NAME = "Example Window"
    MENU_PATH = f"Window/{WINDOW_NAME}"

    def on_startup(self):
        # The ability to show the window if the system requires it. 
        # We use it in QuickLayout.

        # Add a Menu Item for the window

        # Show the window through the 'set_show_window_fn' we wired up above
        # It will call `self.show_window`
        pass

    def on_shutdown(self):
        self._menu = None
        if self._window:
            self._window.destroy()
            self._window = None

        # Deregister the function that shows the window from omni.ui
        ui.Workspace.set_show_window_fn(ExampleWindowExtension.WINDOW_NAME, None)

    def _set_menu(self, value):
        """Set the menu to create this window on and off"""
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(ExampleWindowExtension.MENU_PATH, value)

    async def _destroy_window_async(self):
        # wait one frame, this is due to the one frame defer
        # in Window::_moveToMainOSWindow()
        await omni.kit.app.get_app().next_update_async()
        if self._window:
            self._window.destroy()
            self._window = None

    def _visiblity_changed_fn(self, visible):
        # Called when the user pressed "X"
        self._set_menu(visible)
        if not visible:
            # Destroy the window, since we are creating new window
            # in show_window
            asyncio.ensure_future(self._destroy_window_async())

    def show_window(self, menu, value):
        #value is true if the window should be shown
        if value:
            #call our custom window constructor
            
            #Handles the change in visibility of the window gracefuly
            #This is not covered in the tutorial
            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
        elif self._window:
            self._window.visible = False
