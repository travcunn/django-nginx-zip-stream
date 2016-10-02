""" Django zip stream. """
from django.http import HttpResponse


class TransferZipResponse(HttpResponse):
    """ Streaming zip response. """

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
        """
        Builds the content string body of a single file to send upstream to
        Nginx.
        """
        path, system_path, size = file_info
        single_file_info = "- %s %s %s" % (path, system_path, size)
        return single_file_info
