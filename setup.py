from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wavinfo',
      version='1.3.1',
      author='Jamie Hardt',
      author_email='jamiehardt@me.com',
      description='Probe WAVE Files for iXML, Broadcast-WAVE and other metadata.',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/iluvcapra/wavinfo',
      project_urls={
          'Source':
              'https://github.com/iluvcapra/wavinfo',
          'Documentation':
              'https://wavinfo.readthedocs.io/',
          'Issues':
              'https://github.com/iluvcapra/wavinfo/issues',
      },
      classifiers=['Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Multimedia',
          'Topic :: Multimedia :: Sound/Audio',
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7"],
      packages=['wavinfo'],
      keywords='waveform metadata audio ebu smpte avi library film tv editing editorial',
      install_requires=['lxml']
      )
