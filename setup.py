import io
import os
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read(
    os.path.join(os.path.dirname(__file__), 'README.rst'),
    os.path.join(os.path.dirname(__file__), 'CHANGES'),
)


# Additional Hooks
# ----------------------------
# Integrate py.test with setup.py:
# http://pytest.org/latest/goodpractises.html#integration-with-setuptools-test-commands

class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='Rhetoric',
    version='0.2.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Django>=1.4,<1.8',
        'venusian>=1.0',
        'six',
    ],
    test_suite='tests',
    tests_require=['pytest', 'coverage'],
    package_data={
        # If any package contains *.txt or *.rst files, include them
        '': ['*.txt', '*.rst',]
    },
    include_package_data=True,
    cmdclass={
        'test': PyTest,
    },
    # PyPI metadata
    # Read more at http://docs.python.org/distutils/setupscript.html#meta-data
    author="Maxim Avanov",
    author_email="maxim.avanov@gmail.com",
    maintainer="Maxim Avanov",
    maintainer_email="maxim.avanov@gmail.com",
    description="Pyramid-like routes for Django projects",
    long_description=long_description,
    license="MIT",
    url="https://github.com/avanov/Rhetoric",
    download_url="https://github.com/avanov/Rhetoric",
    keywords="pyramid django routes",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
