import os
from PIL import Image

def convert_icons():
    icons = ['pass_logo.png', 'copy.png', 'create_btn.png', 'eye.png', 
             'password_generator.png', 'master_password.png']
    icons_dir = os.path.join("src", "assets", "icons")
    
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
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
            print(f"Файл иконки {png_path} не найден!")
            success = False
            
    return success

if __name__ == "__main__":
    if convert_icons():
        print("\nВсе иконки успешно конвертированы!")
    else:
        print("\nПри конвертации некоторых иконок произошли ошибки!") 