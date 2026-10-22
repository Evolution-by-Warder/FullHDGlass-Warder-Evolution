"""Read existing 7z PNG assets through the operating system's libarchive."""
import ctypes
import ctypes.util
from pathlib import Path


def png_files(path):
    lib = ctypes.CDLL(ctypes.util.find_library('archive'))
    lib.archive_read_new.restype = ctypes.c_void_p
    for name in ('archive_read_support_filter_all', 'archive_read_support_format_all', 'archive_read_free'):
        getattr(lib, name).argtypes = [ctypes.c_void_p]
    lib.archive_read_open_filename.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
    lib.archive_read_next_header.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
    lib.archive_entry_pathname.argtypes = [ctypes.c_void_p]
    lib.archive_entry_pathname.restype = ctypes.c_char_p
    lib.archive_entry_size.argtypes = [ctypes.c_void_p]
    lib.archive_entry_size.restype = ctypes.c_longlong
    lib.archive_read_data.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    lib.archive_read_data.restype = ctypes.c_ssize_t
    lib.archive_error_string.argtypes = [ctypes.c_void_p]
    lib.archive_error_string.restype = ctypes.c_char_p
    archive = lib.archive_read_new()
    lib.archive_read_support_filter_all(archive)
    lib.archive_read_support_format_all(archive)
    try:
        assert lib.archive_read_open_filename(archive, str(Path(path)).encode(), 10240) == 0
        entry = ctypes.c_void_p()
        while True:
            status = lib.archive_read_next_header(archive, ctypes.byref(entry))
            if status == 1:
                break
            if status < 0:
                raise ValueError(lib.archive_error_string(archive))
            name = lib.archive_entry_pathname(entry).decode()
            size = lib.archive_entry_size(entry)
            if not name.lower().endswith('.png'):
                continue
            assert 0 < size < 16 * 1024 * 1024
            assert '..' not in Path(name).parts and not Path(name).is_absolute()
            output = bytearray()
            buffer = ctypes.create_string_buffer(65536)
            while True:
                count = lib.archive_read_data(archive, buffer, len(buffer))
                if count == 0:
                    break
                if count < 0:
                    raise ValueError(lib.archive_error_string(archive))
                output.extend(buffer.raw[:count])
            assert len(output) == size
            yield Path(name).name, bytes(output)
    finally:
        lib.archive_read_free(archive)
