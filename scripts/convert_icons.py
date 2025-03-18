import os
from PIL import Image

def convert_icons():
    # Получаем путь к корневой директории проекта (на один уровень выше директории scripts)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    icons = [
        'pass_logo.png', 'copy.png', 'create_btn.png', 'eye.png', 
        'password_generator.png', 'master_password.png', 'settings_icon.png',
        'uuid_icon.png', 'exit_icon.png', 'info_icon.png', 'lock.png',
        'save_icon.png'
    ]
    
    # Абсолютный путь к директории с иконками
    icons_dir = os.path.join(root_dir, "src", "assets", "icons")
    
    print(f"Путь к директории с иконками: {icons_dir}")
    
    if not os.path.exists(icons_dir):
        print(f"Директория {icons_dir} не существует! Создаем...")
        os.makedirs(icons_dir, exist_ok=True)
    
    success = True
    for icon in icons:
        png_path = os.path.join(icons_dir, icon)
        ico_path = os.path.join(icons_dir, icon.replace('.png', '.ico'))
        
        if os.path.exists(png_path):
            try:
                img = Image.open(png_path)
                # Создаем набор иконок разных размеров
                icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
                img.save(ico_path, format='ICO', sizes=icon_sizes)
                print(f"Иконка {icon} успешно конвертирована в ICO")
            except Exception as e:
                print(f"Ошибка при конвертации {icon}: {e}")
                success = False
        else:
            print(f"Файл иконки не найден: {png_path}")
            success = False
            
    return success

if __name__ == "__main__":
    print("Начинаем конвертацию иконок из PNG в ICO формат...")
    if convert_icons():
        print("\nВсе иконки успешно конвертированы!")
    else:
        print("\nПри конвертации некоторых иконок произошли ошибки!") 