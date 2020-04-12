#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Shane R. Spencer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# SPDX-License-Identifier: MIT

# Author: Shane R. Spencer <spencersr@gmail.com>

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

# kw

kwargs = {}

# "Safe" version read
with open("wap_mms_encoder/__init__.py") as f:
    ns = {}
    exec(f.read(), ns)
    kwargs["version"] = ns["version"]

with open("README.rst") as f:
    kwargs["long_description"] = f.read()

if setuptools is not None:
    python_requires = ">= 3.8"
    kwargs["python_requires"] = python_requires

setup(
    name="wap_mms_encoder",
    packages=["wap_mms_encoder"],
    author="Shane R. Spencer",
    author_email="spencersr@gmail.com",
    url="https://github.com/whardier/wap-mms-encoder",
    license="MIT",
    project_urls={
        "Funding": "https://github.com/sponsors/whardier",
        "Source": "https://github.com/whardier/wap-mms-encoder",
    },
    description=("Extremely simple encoder for application/vnd.wap.mms-message payloads"),
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Topic :: Communications :: Telephony",
        "Intended Audience :: Telecommunications Industry",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    **kwargs
)
