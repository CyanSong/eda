from setuptools import setup, find_packages
setup(
      name="Xspice",
      version="1.0",
      description="My test module",
      author="Cyan Song",
      url="https://github.com/CyanSong/eda",
      license="LGPL",
      packages= find_packages(exclude=["*tests.*"]),
      scripts=["src/network.py"],
      install_requires=[
          "numpy",
           "matplotlib",
          "pyqt",
          "lark-parser"
      ]
      )