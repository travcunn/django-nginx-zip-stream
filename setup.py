"""A setuptools based setup module to install django-zip-stream."""
from setuptools import setup

try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

setup(
    name='django-zip-stream',
    version='0.7.0',
    description='Django extension to assemble ZIP archives dynamically.',
    long_description=LONG_DESCRIPTION,
    author='Travis Cunningham',
    author_email='tcunningham@smartfile.com',
    url='https://github.com/travcunn/django-zip-stream',
    license='MIT',
    packages=['django_zip_stream'],
    package_dir={'django_zip_stream': 'django_zip_stream'},
    install_requires=[
        'Django>=1.7',
    ], )
