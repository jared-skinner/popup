from setuptools import setup, find_packages

setup(
    name='popup',
    version='0.1',
    author="Jared Skinner",
    author_email="jaredds66@gmail.com",
    packages = setuptools.find_packages(),
    python_requires = ">=3.8",
    install_requires=[
        "pickleDB==0.9.2",
        "validators==0.20.0",
        "requests==2.31.0"
    ],
    entry_points={
        'console_scripts': ['popup=popup.__main__:main']
    },
)
