from setuptools import setup, find_packages

__about__ = {}

with open("urbanairship/__about__.py") as fp:
    exec(fp.read(), None, __about__)

setup(
    name="urbanairship3",
    version=__about__["__version__"],
    author="Adam Lowry",
    author_email="adam@urbanairship.com",
    url="http://urbanairship.com/",
    description="Python package for using the Urban Airship API",
    long_description=open('README.rst').read(),
    # packages=["urbanairship", "urbanairship.push", "urbanairship.devices", "urbanairship.tests"],
    packages=find_packages(),
    license='BSD License',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests>=1.2',
    ],
    use_2to3=True,
)
