import os
from urllib.parse import unquote
from gi.repository import Nautilus, GObject
from typing import List
import subprocess

class OpenNvimExtension(GObject.GObject, Nautilus.MenuProvider):
    def _open_nvim(self, file: Nautilus.FileInfo) -> None:
        filename = unquote(file.get_uri()[7:])
        subprocess.Popen(["kitty", "nvim", filename])

    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_nvim(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_nvim(file)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]
        if file.is_directory() or file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="NautilusPython::opennvim_file_item",
            label="Open In Nvim",
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        # Do not show 'Open In Nvim' for background (folders)
        return []
