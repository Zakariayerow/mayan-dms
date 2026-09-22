from django.utils.translation import gettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency, PythonDependency
from mayan.apps.dependencies.environments import environment_production

from .backends.python import pdfinfo_path, pdftoppm_path
from .classes import libreoffice_path

BinaryDependency(
    environments=(environment_production,), label=_(message='LibreOffice'),
    module=__name__, name='libreoffice', path=libreoffice_path
)
BinaryDependency(
    environments=(environment_production,), label=_(message='PDF Info'),
    help_text=_(
        message='Utility from the poppler-utils package used to inspect PDF '
        'files.'
    ), module=__name__, name='pdfinfo', path=pdfinfo_path
)
BinaryDependency(
    environments=(environment_production,), label=_(message='PDF to PPM'),
    help_text=_(
        message='Utility from the popper-utils package used to extract '
        'pages from PDF files into PPM format images.'
    ), module=__name__, name='pdftoppm', path=pdftoppm_path
)

PythonDependency(
    attribute_copyright='PIL.__doc__',
    environments=(environment_production,), module=__name__, name='Pillow',
    version_string='==12.3.0'
)
PythonDependency(
    environments=(environment_production,), module=__name__, name='pypdf',
    version_string='==6.16.1'
)
PythonDependency(
    environments=(environment_production,), module=__name__, name='qrcode',
    version_string='==8.2'
)
