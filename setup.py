from setuptools import setup, find_packages

setup(
    name="package",
    version="0.1",
    description="A description of your Python package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/HemapriyaM23/github_poc",
    packages=find_packages(where='package'),  # Make sure to look inside 'my-python-package'
    package_dir={'': 'package'},  # Set package directory
    install_requires=[
        'numpy',  # Example dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
