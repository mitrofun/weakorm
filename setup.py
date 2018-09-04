import sys

from setuptools import setup, find_packages
from os.path import join, dirname

if not sys.version_info[0] == 3 and sys.version_info[0] == 6:
    sys.exit("Sorry, need Python >= 3.6")

setup(
    name='weakorm',
    version='0.1.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/mitrofun/weakorm',
    description='Simple ORM for sqlite.',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='orm sqlite',
    author='Dmitry Shesterkin',
    author_email='mitri4@bk.ru',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-flake8', 'flake8', 'pytest-mccabe'],
    test_suite='tests',
    python_requires='>=3.6',
    zip_safe=False
)
