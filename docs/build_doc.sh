#!/bin/bash

sphinx-apidoc --ext-githubpages --ext-viewcode --ext-coverage --ext-doctest --ext-autodoc \
	-R "1.0.1" -A "NLeSC" -F -M -e -d 8 \
	-o . \
	../pymicmac

