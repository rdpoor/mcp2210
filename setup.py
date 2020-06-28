#!/usr/bin/env python

from setuptools import setup

setup(name="mcp2210",
      version="0.1.6",
      description="Python interface for the MCP2210 USB-SPI interface",
      author="Robert Poor",
      author_email="rdpoor@gmail.com",
      url="https://github.com/rdpoor/mcp2210/",
      packages=["mcp2210"],
      install_requires=["hidapi>=0.7.99"])
