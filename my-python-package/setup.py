from setuptools import setup, find_packages

setup(
    name="mypackage",                # The name of your package
    version="0.1",                   # Package version
    description="A simple Python package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",              # Your name or organization
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my-python-package",  # GitHub URL
    packages=find_packages(),        # Automatically discover all packages
    install_requires=[               # List of dependencies
        'numpy',
        'requests'
    ],
    classifiers=[                    # Metadata classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',          # Minimum Python version required
)
