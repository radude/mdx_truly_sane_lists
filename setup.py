import os.path as path
from setuptools import setup


def get_readme(filename):
    if not path.exists(filename):
        return ""

    with open(path.join(path.dirname(__file__), filename)) as readme:
        content = readme.read()
    return content


setup(name="mdx_truly_sane_lists",
      version="0.0",
      author='radude',
      author_email='admin@rentry.co',
      description="Extension for Python-Markdown that makes lists truly sane. Custom indents for nested lists and fix for messy linebreaks.",
      license="MIT",
      keywords="markdown extension",
      url="https://github.com/radude/mdx_truly_sane_lists",
      packages=["mdx_truly_sane_lists"],
      long_description=get_readme("README.md"),
      classifiers=[
          "Topic :: Text Processing :: Markup",
          "Topic :: Utilities",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
      ],
      install_requires=["Markdown>=2.6"],
      test_suite="mdx_truly_sane_lists.tests")
