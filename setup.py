from setuptools import setup

setup(
    name='DarijaTranslatorAssistant',
    version='1.0.0',
    description='A library for assisting in translating Darija to English. It provides a list of potential translations for a given darija word. It also supports translation of full sentences using LLMs (e.g., OpenAI).',
    author='Aissam Outchakoucht',
    author_email='aissam.outchakoucht@gmail.com',
    url='https://github.com/aissam-out/DarijaTranslatorAssistant',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['DarijaTranslatorAssistant'],
    include_package_data=True,
    install_requires=[
        'DarijaDistance==1.0.8',
        'openai==1.43.0',
        'requests==2.32.3',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
