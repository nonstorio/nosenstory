from setuptools import find_packages, setup
from scripts.stubs import StubsCommand

setup(
    name = 'nosenstory',
    packages = find_packages(),
    description = 'NosenStory API, client-agnostic interface for maintaining NosenStory\'s game process across multiple chat platforms.',
    url = 'https://github.com/nosenstory/nosenstory',
    cmdclass = {
        'stubs': StubsCommand
    }
)
