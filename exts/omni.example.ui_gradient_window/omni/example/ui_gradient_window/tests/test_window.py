# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["TestWindow"]

from omni.example.ui_gradient_window import PropertyWindowExample
from omni.ui.tests.test_base import OmniUiTest
from pathlib import Path
import omni.kit.app
import omni.kit.test


EXTENSION_FOLDER_PATH = Path(omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__))
TEST_DATA_PATH = EXTENSION_FOLDER_PATH.joinpath("data/tests")


class TestWindow(OmniUiTest):
    async def test_general(self):
        """Testing general look of section"""
        window = PropertyWindowExample("Test")
        await omni.kit.app.get_app().next_update_async()
        await self.docked_test_window(
            window=window,
            width=450,
            height=600,
        )

        # Wait for images
        for _ in range(20):
            await omni.kit.app.get_app().next_update_async()

        await self.finalize_test(golden_img_dir=TEST_DATA_PATH, golden_img_name="window.png")
