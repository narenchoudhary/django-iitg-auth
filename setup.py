from setuptools import find_packages, setup

import iitgauth

try:
    readme = open('README.rst').read()
except IOError:
    readme = ''

setup(
    name='django-iitg-auth',
    version='.'.join(str(i) for i in iitgauth.VERSION),
    description='``django-iitg-auth`` is a reusable Django application for '
                'which provides a custom authencation backend for '
                'authenticating with IIT Guwahati webmail servers, a login '
                'form and a utility view.',
    long_description=readme,
    packages=find_packages(exclude=('tests', 'docs', 'example', )),
    author='Narendra Choudhary',
    author_email='narendralegha.mail@gmail.com',
    url='https://github.com/narenchoudhary/django-iitg-auth',
    install_requires=['Django>=1.7'],
    license='BSD 3-Clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django library development authentication',
    zip_safe=False,
)
