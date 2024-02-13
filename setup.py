from cx_Freeze import setup, Executable

setup(
    name='Limbos32',
    version='0.1',
    description='Limbos32',
    executables=[Executable('server.py'), Executable('focus.py')]
)