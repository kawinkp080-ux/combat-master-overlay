"""DLL injector stub used for the optional in-process ESP path."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from pathlib import Path

from loguru import logger

PROCESS_ALL_ACCESS = 0x1F0FFF


class Injector:
    def __init__(self, pid: int, dll_path: Path) -> None:
        self.pid = pid
        self.dll_path = dll_path

    def inject(self) -> None:
        k32 = ctypes.windll.kernel32
        handle = k32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        if not handle:
            raise OSError(f"OpenProcess failed for pid {self.pid}")
        try:
            addr = k32.VirtualAllocEx(handle, None, 4096, 0x3000, 0x40)
            path_bytes = str(self.dll_path).encode("utf-16-le")
            written = wintypes.SIZE_T(0)
            k32.WriteProcessMemory(handle, addr, path_bytes, len(path_bytes),
                                   ctypes.byref(written))
            thread = k32.CreateRemoteThread(handle, None, 0, addr, None, 0, None)
            if not thread:
                raise OSError("CreateRemoteThread failed")
            logger.success("injected {} into pid {}", self.dll_path.name, self.pid)
        finally:
            k32.CloseHandle(handle)