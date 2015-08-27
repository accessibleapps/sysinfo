from setuptools import setup, find_packages

setup(
 name = 'sysinfo',
 version = 0.2,
 description = """Return various data about the host system including hardware, software, and interpreter information""",
 py_modules = ['sysinfo',],
 install_requires=['psutil==2.2.1',],
)
