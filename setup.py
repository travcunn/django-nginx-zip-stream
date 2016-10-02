"""A setuptools based setup module to install django-zip-stream."""
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    """Test command that runs tox."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox  # import here, cause outside the eggs aren't loaded.
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()
VERSION = "0.7.1"

setup(
    name='django-zip-stream',
    version=VERSION,
    description='Django extension to assemble ZIP archives dynamically.',
    long_description=README,
    author='Travis Cunningham',
    author_email='tcunningham@smartfile.com',
    url='https://github.com/travcunn/django-zip-stream',
    license='MIT',
    packages=['django_zip_stream'],
    package_dir={'django_zip_stream': 'django_zip_stream'},
    install_requires=[
        'Django>=1.7',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    extras_require={'test': ['tox']}, )
