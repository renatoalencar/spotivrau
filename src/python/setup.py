from setuptools import setup

setup(
    name='spotivrau',
    packages=['spotivrau'],
    include_package_data=True,
    install_requires=[
        'flask',
        'mongoengine',
        'redis',
        'ffmpeg-python',
    ],
)
