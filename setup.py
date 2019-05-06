import setuptools


setuptools.setup(name='miscellaneous',
      version="1.0.0",
      url = "https//www.github.com/NostrumBioDiscovery/miscellaneous", 
      description='Miscellaneous of python scripts for drug discovery',
      author='Daniel Soler',
      author_email='daniel.soler@nostrumbiodiscovery.com',
      install_requires=["tqdm", "numpy"],
      packages=setuptools.find_packages(),
      classifiers=[
         "Programming Language :: Python3",
         "License :: OSI Approved :: MIT"
         "Operating System :: Linux" ]
     )
