"""Assemble ZIP archives dynamically using Nginx."""
import pkg_resources


#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__.replace('-', '_')) \
                           .version
