from distutils.core import setup, Extension


setup(name='klogctl', version='0.1',
      author='James Newton', author_email='baron@codepunks.org',
      url='http://www.cairn-project.org/',
      ext_modules=[
      	Extension('klogctl',
				  ['klogctl.c'],
				  extra_compile_args=['-Wall'])
      ])
