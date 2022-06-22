# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["CustomCollsableFrame"]

import omni.ui as ui


def build_collapsable_header(collapsed, title):
    """Build a custom title of CollapsableFrame"""
    with ui.HStack():
        ui.Spacer(width=10)
        ui.Label(title, name="collapsable_name")

        if collapsed:
            image_name = "collapsable_opened"
        else:
            image_name = "collapsable_closed"
        ui.Image(name=image_name, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, width=16, height=16)

class CustomCollsableFrame:
    """The compound widget for color input"""

    def __init__(self, frame_name, collapsed=False):
        with ui.ZStack():
            self.collapsable_frame = ui.CollapsableFrame(
                frame_name, name="group", build_header_fn=build_collapsable_header, collapsed=collapsed)
            with ui.VStack():
                ui.Spacer(height=29)
                with ui.HStack():
                    ui.Spacer(width=20)
                    ui.Image(name="separator", fill_policy=ui.FillPolicy.STRETCH, height=15)
                    ui.Spacer(width=20)


        
