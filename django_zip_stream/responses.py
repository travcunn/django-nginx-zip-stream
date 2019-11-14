"""Django zip stream responses."""
import os
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path
from urllib.parse import quote
import binascii


def CRC32_from_file(filename):
    buf = open(filename, 'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08x" % buf


class TransferZipResponse(HttpResponse):
    """Streaming zip response."""

    def __init__(self, filename, files):
        """
        Parameters:
        filename (string) - Name of the zip file to be streamed.
        files (list of (path, system_path, size) tuples) - List of files to
            be transferred.
        """

        content = "\r\n".join(
            [self._build_content(file_info) for file_info in files])

        super(TransferZipResponse, self).__init__(
            content, status=200, content_type="application/zip")

        self["X-Archive-Files"] = 'zip'
        self['Content-Disposition'] = (
            'attachment; filename="{}"'.format(filename))

    @staticmethod
    def _build_content(file_info):
        """Return the content string body of a single file for use upstream.

        Given a file_info tuple (path, system_path, size), this method
        assembles a string containing mod_zip commands for a single file.
        """
        if len(file_info) == 3:
            path, system_path, size = file_info
            single_file_info = "- %s %s %s" % (size, system_path, path)
        elif len(file_info) == 4:
            crc, path, system_path, size = file_info
            single_file_info = "%s %s %s %s" % (crc, size, system_path, path)
        else:
            raise Exception("file_info has to be a 3- or 4-tuple.")
        return single_file_info


class FolderZipResponse(TransferZipResponse):
    """Streaming folder zip response."""

    def __init__(self, folder_path, filename=None, url_prefix=None, add_folder_name=True, add_hash=False):
        """
        Parameters:
        folder_path (string|path): Folder to be transferred.
        filename (string|None): Name of the zip file to be streamed.
                                Default: folder name
        url_prefix (string|None): Prefix for every file url.
                                  Default: STATIC_URL
        add_folder_name (bool): Make the folder name part of sys_path.
                                Default: True
        """

        if url_prefix is None:
            url_prefix = settings.STATIC_URL

        if not url_prefix.endswith('/'):
            url_prefix += '/'

        folder = Path(folder_path)
        files = [f for f in folder.rglob('*') if f.is_file()]
        tuples = []

        if filename is None:
            filename = folder.name
        if not filename.endswith('.zip'):
            filename += '.zip'

        for f in files:
            zip_path = os.path.relpath(str(f), str(folder_path))
            url_path = url_prefix
            if add_folder_name:
                url_path += folder.name + '/'
            url_path += zip_path
            size = f.stat().st_size

            if add_hash:
                crc = CRC32_from_file(str(f))
                tuples.append(
                    (crc, zip_path, quote(url_path), size)
                )
            else:
                tuples.append(
                    (zip_path, quote(url_path), size)
                )

        super(FolderZipResponse, self).__init__(filename, tuples)
