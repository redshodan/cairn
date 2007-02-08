from distutils.core import setup, Extension


setup(name='volumeid', version='0.1',
      author='James Newton', author_email='baron@codepunks.org',
      url='http://www.cairn-project.org/',
      ext_modules=[
      	Extension('volumeid',
				  ['volumeid.c'],
				  extra_link_args=['../../../build/lib/libvolumeid.a'],
				  extra_compile_args=['-g', '-Wall', "-Ivolume_id"])
      ])
