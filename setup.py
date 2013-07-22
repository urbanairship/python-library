from distutils.core import setup


setup(
    name="urbanairship",
    version=open('VERSION.txt').read().strip(),
    author="Adam Lowry",
    author_email="adam@urbanairship.com",
    url="http://urbanairship.com/",
    description="Python package for using the Urban Airship API",
    long_description=open('README.rst').read(),
    packages=["urbanairship", "urbanairship.push", "urbanairship.devices"],
    license='BSD License',
    classifiers=[
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
)
