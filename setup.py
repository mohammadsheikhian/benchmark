import os.path
import re

from setuptools import setup, find_packages


with open(
    os.path.join(os.path.dirname(__file__), 'benchmark', '__init__.py')
) as v_file:
    package_version = \
        re.compile(r'.*__version__ = \'(.*?)\'', re.S) \
        .match(v_file.read()) \
        .group(1)


dependencies = [
	'argcomplete',
	'requests',
    'easycli',
]


setup(
    name='benchmark',
    version=package_version,
    author='Mohammad Sheikhian',
    author_email='mohammadsheikhian70@gmail.com',
    url='https://github.com/mohammadsheikhian/benchmark',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    install_requires=dependencies,
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'benchmark = benchmark.cli:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ]
)

