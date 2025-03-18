import os
import shutil
import subprocess
import sys
import re
from pathlib import Path

def get_pyqt_path():
    import PyQt5
    return os.path.dirname(PyQt5.__file__)

def get_app_version():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    about_dialog_path = os.path.join(root_dir, "src", "gui", "widgets", "about_dialog.py")
    
    try:
        with open(about_dialog_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Ищем строку с версией
        version_match = re.search(r'version\s*=\s*QLabel\("GenPass\s+v\.?([0-9.]+)', content)
        if version_match:
            return version_match.group(1)
        else:
            print("Предупреждение: Версия не найдена в about_dialog.py, используем версию по умолчанию.")
            return "1.0.0"
    except Exception as e:
        print(f"Ошибка при чтении версии из about_dialog.py: {e}")
        return "1.0.0"

def clean_build():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        dir_path = os.path.join(root_dir, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    for pattern in files_to_clean:
        for file in Path(root_dir).glob(pattern):
            file.unlink()

def build_exe(arch):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Получаем версию приложения
    version = get_app_version()
    
    # Формируем имя выходного файла с версией
    output_name = f"GenPass_v{version}_{arch}"
    
    icon_path = os.path.join(root_dir, "src", "assets", "icons", "pass_logo.ico")
    
    assets_path = os.path.join(root_dir, "src", "assets")
    
    pyqt_path = get_pyqt_path()
    qt_bin_path = os.path.join(pyqt_path, "Qt5", "bin")
    qt_plugins_path = os.path.join(pyqt_path, "Qt5", "plugins")
    
    os.chdir(root_dir)
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--onefile",
        f"--distpath=dist/{arch}",
        f"--workpath=build/{arch}",
        f"--name={output_name}",
        f"--icon={icon_path}",
        "--add-data", f"{assets_path};src/assets",
        "--hidden-import=PyQt5.sip",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtWidgets.QApplication",
        "--hidden-import=PyQt5.QtWidgets.QMainWindow",
        "--add-binary", f"{qt_bin_path}\\Qt5Core.dll;.",
        "--add-binary", f"{qt_bin_path}\\Qt5Gui.dll;.",
        "--add-binary", f"{qt_bin_path}\\Qt5Widgets.dll;.",
        "--add-binary", f"{qt_bin_path}\\Qt5Network.dll;.",
        "--add-binary", f"{qt_bin_path}\\Qt5DBus.dll;.",
        "--add-binary", f"{qt_bin_path}\\libEGL.dll;.",
        "--add-binary", f"{qt_bin_path}\\libGLESv2.dll;.",
        "--add-binary", f"{qt_bin_path}\\opengl32sw.dll;.",
        "--add-binary", f"{qt_bin_path}\\D3DCompiler_47.dll;.",
        "--add-binary", f"{qt_plugins_path}\\platforms\\qwindows.dll;platforms",
        "--add-binary", f"{qt_plugins_path}\\styles\\qwindowsvistastyle.dll;styles",
        "--add-binary", f"{qt_plugins_path}\\imageformats\\qico.dll;imageformats",
        "--add-binary", f"{qt_plugins_path}\\imageformats\\qjpeg.dll;imageformats",
        "--add-binary", f"{qt_plugins_path}\\imageformats\\qsvg.dll;imageformats",
        "--noupx",
        "--target-arch", arch,
        "src/main.py"
    ]
    
    try:
        print(f"Сборка версии {version} для архитектуры {arch}...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Предупреждения:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Ошибка сборки:")
        print(e.stdout)
        print(e.stderr)
        raise

def main():
    clean_build()
    
    version = get_app_version()
    print(f"\nНачинаем сборку GenPass версии {version}")
    
    architectures = ['x86', 'x64']
    
    for arch in architectures:
        print(f"\nСборка для {arch}...")
        try:
            build_exe(arch)
            print(f"Сборка для {arch} успешно завершена!")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при сборке для {arch}: {e}")
            continue

    print("\nПроцесс сборки завершен!")

if __name__ == "__main__":
    main() 