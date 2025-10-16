import os
from urllib.parse import unquote
from gi.repository import Nautilus, GObject
from typing import List
import subprocess



class OpenVSCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    def _open_vscode(self, file: Nautilus.FileInfo) -> None:
        filename = unquote(file.get_uri()[7:])
        # Open Visual Studio Code in the selected directory or file
        subprocess.Popen(["code", filename])

    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_vscode(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_vscode(file)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="NautilusPython::openvscode_file_item",
            label="Open In VSCode",
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        item = Nautilus.MenuItem(
            name="NautilusPython::openvscode_file_item2",
            label="Open In VSCode",
        )
        item.connect("activate", self.menu_background_activate_cb, current_folder)

        return [
            item,
        ]
