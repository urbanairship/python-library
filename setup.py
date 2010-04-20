from distutils.core import setup


setup(
    name="urbanairship",
    version="0.3",
    author="Adam Lowry",
    author_email="adam@urbanairship.com",
    url="http://urbanairship.com/",
    description="Python module for using the Urban Airship API",
    long_description=open('README.rst').read(),
    py_modules=["urbanairship"],
    license='BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ],
)
