from setuptools import setup

setup(
    name='dockerfile-requirements',
    packages=['dockerfile_requirements'],
    platforms='any',
    version='0.0.4',
    description='Inlining requirements.txt files into Dockerfiles for better caching.',
    author='H. Chase Stevens',
    author_email='chase@chasestevens.com',
    url='https://github.com/hchasestevens/dockerfile-requirements',
    license='MIT',
    install_requires=[
        'gitpython>=3.1.0',
        'jinja2>=2.10.1',
    ],
    entry_points={
        'console_scripts': [
            'dockerfile-requirements = dockerfile_requirements:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ]
)

