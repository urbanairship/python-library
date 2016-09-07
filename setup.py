try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__about__ = {}

with open("wallet/__about__.py") as fp:
    exec(fp.read(), None, __about__)

setup(
    name="wallet",
    version=__about__["__version__"],
    author="Urban Airship",
    author_email="support@urbanairship.com",
    url="http://urbanairship.com/",
    description="Python package for using the Urban Airship Wallet API",
    long_description=open('README.rst').read(),
    packages=["wallet"],
    license='BSD License',
    classifiers=[
        'Development Status :: Beta',
        'Environment :: Client Side REST Interface',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests>=2.7',
        'six'
    ],
)
