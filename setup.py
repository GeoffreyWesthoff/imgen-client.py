"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='imgen-client.py',
      author='Geoffrey Westhoff',
      url='https://dankmemer.services',
      project_urls={
          "GitHub": "https://github.com/Dank-Memer/imgen-client.py",
          "Imgen-Server": "https://github.com/Dank-Memer/meme-server"
      },
      license='MIT',
      description='A python wrapper for the Dank Memer Imgen API',
      install_requires=requirements,
      python_requires='>=3.5.3')
