from setuptools import find_packages, setup


with open("README.rst") as fobj:
    long_description = fobj.read()


setup(
    author="Eduardo Cuducos",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
    description="Clean-up inactive accounts and bots from your Twitter",
    entry_points="[console_scripts]\ntwitter-cleanup=twitter_cleanup.__main__:cli",
    install_requires=[
        "arrow>=0.13.0",
        "click>=7.0",
        "botometer>=1.3",
        "python-decouple>=3.1",
        "tweepy>=3.7.0",
    ],
    keywords="twitter, bots, social network",
    license="GPLv3",
    long_description=long_description,
    name="twitter-cleanup",
    packages=find_packages(),
    py_modules=["twitter_cleanup"],
    url="https://github.com/cuducos/twitter-cleanup",
    version="0.0.5",
    zip_safe=False,
)
