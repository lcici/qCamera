from distutils.core import setup
import qcamera

long_description = \
"""qCamera is a unified camera interface meant to be used in
experimental control systems such as qControl. It is designed to have
commands for cameras be as generic as possible to the user, that way
swapping out physical cameras should require little more than changing
a line of code to reflect the new hardware."""

setup(
    name='qCamera',
    version=qcamera.__version__,
    author='Michael V. DePalatis',
    author_email='depalatis@phys.au.dk',
    url='http://phys.au.dk/forskning/forskningsomraader/amo/the-ion-trap-group/',
    description='Unified camera interface for qControl and other experimental control systems.',
    long_description=long_description,
    platforms="Windows",
    license="GNU LGPLv3",
    packages=['qcamera'],
    package_data={'qcamera': ['props/*.json']},
    requires=[
        'numpy (>=1.6.0)',
        'tables (>=3.0.0)'
    ]
)
