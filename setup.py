from setuptools import setup

f = open('LICENSE.txt', 'r')
l = f.read()

setup(
    name='InterAPI',
    version='0.0.6',
    packages=['InterAPI'],
    url='https://github.com/btmluiz/InterAPI',
    license=l,
    author='btmluiz',
    author_email='luiz@selectbrasil.com.br',
    description='API para integração com banco inter',
    install_requires=[
        'requests>=2.24.0'
    ],
    python_requires='>=3'
)

f.close()
