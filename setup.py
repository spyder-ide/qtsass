from cx_Freeze import setup, Executable

build_exe_options = {
    'include_msvcr': True,
    'optimize': 2
}

setup(
    name="qtsass",
    description="Compile a SCSS file to a valid Qt CSS.",
    executables=[Executable("qtsass/qtsass.py")],
    options={'build_exe': build_exe_options},
    requires=['libsass', 'cx_Freeze'],
)
