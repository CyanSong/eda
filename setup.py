from setuptools import setup
setup(
      name="xspice",
      version="1.0",
      description="My test module",
      author="Cyan Song",
      url="https://github.com/CyanSong/eda",
      license="LGPL",
      packages= ['xspice','xspice.command','xspice.device','xspice.syntax'],
      package_data={'': ['*.md', '*.sp','unit_test.py']},
      install_requires=[
          "numpy",
          "lark-parser"
      ]
      )