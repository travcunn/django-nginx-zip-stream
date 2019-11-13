"""Django zip stream responses."""
import os
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path


class TransferZipResponse(HttpResponse):
    """Streaming zip response."""

    def __init__(self, filename, files):
        """
        Parameters:
        filename (string) - Name of the zip file to be streamed.
        files (list of (path, system_path, size) tuples) - List of files to
            be transferred.
        """

        content = "\n".join(
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
        path, system_path, size = file_info
        single_file_info = "- %s %s %s" % (size, system_path, path)
        return single_file_info


class FolderZipResponse(HttpResponse):
    """Streaming folder zip response."""

    def __init__(self, filename, folder_path, url_prefix=None, add_folder_name=True):
        """
        Parameters:
        filename (string): Name of the zip file to be streamed.
        folder_path (string|path): Folder to be transferred.
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

        for f in files:
            path = os.path.relpath(str(f), str(folder_path))
            system_path = url_prefix
            if add_folder_name:
                system_path += folder.name + '/'
            system_path += path
            size = f.stat().st_size

            tuples.append(
                (path, system_path, size)
            )

    @staticmethod
    def _build_content(file_info):
        """Return the content string body of a single file for use upstream.

        Given a file_info tuple (path, system_path, size), this method
        assembles a string containing mod_zip commands for a single file.
        """
        path, system_path, size = file_info
        single_file_info = "- %s %s %s" % (size, system_path, path)
        return single_file_info
