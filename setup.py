from setuptools import setup, find_packages

setup(
    name='nlp_toolbox',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
        'nltk',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'nlp_toolbox=nlp_toolbox.cli:main'
        ]
    }
)
