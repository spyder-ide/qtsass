from cx_Freeze import setup, Executable

build_exe_options = {
    'include_msvcr': True,
    'bin_includes': ['msvcp120.dll'],  # Force msvcp120 to be included (libsass dependency, not copied by include_mscvr)
    'optimize': 2
}

setup(
    name="qtsass",
    description="Compile a SCSS file to a valid Qt CSS.",
    executables=[Executable("qtsass/qtsass.py")],
    options={'build_exe': build_exe_options},
    requires=['libsass', 'cx_Freeze', 'watchdog'],
)
