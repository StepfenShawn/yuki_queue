from setuptools import setup, find_packages

setup(
    name="yuki_queue",
    version="0.0.1",
    author="Stepfen Shawn",
    author_email="m18824909883@163.com",
    description="A tiny but powerful distributed task queue for python.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)