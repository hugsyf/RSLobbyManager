import os
import string
import random
import sys
import json
import locale

#########
# TODO 模板拆分到其它文件里，便于将来区分GTA5和RDR2？
#########
rdo_startup_meta_template = '''
<?xml version="1.0" encoding="UTF-8"?>
<CDataFileMgr__ContentsOfDataFileXml>
 <disabledFiles />
 <includedXmlFiles itemType="CDataFileMgr__DataFileArray" />
 <includedDataFiles />
 <dataFiles itemType="CDataFileMgr__DataFile">
  <Item>
   <filename>platform:/data/cdimages/scaleform_platform_pc.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/data/ui/value_conversion.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/data/ui/widgets.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/textures/ui/ui_photo_stickers.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/textures/ui/ui_platform.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/data/ui/stylesCatalog</filename>
   <fileType>aWeaponizeDisputants</fileType> <!-- collision -->
  </Item>
  <Item>
   <filename>platform:/data/cdimages/scaleform_frontend.rpf</filename>
   <fileType>RPF_FILE_PRE_INSTALL</fileType>
  </Item>
  <Item>
   <filename>platform:/textures/ui/ui_startup_textures.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
  <Item>
   <filename>platform:/data/ui/startup_data.rpf</filename>
   <fileType>RPF_FILE</fileType>
  </Item>
 </dataFiles>
 <contentChangeSets itemType="CDataFileMgr__ContentChangeSet" />
 <patchFiles />
</CDataFileMgr__ContentsOfDataFileXml>===PasswordHere===
'''
# i18n

## 获取系统语言
def get_system_language():
    # 弃用locale.getdefaultlocale()
    # lang_code, _ = locale.getdefaultlocale()
    try:
        # 初始化 locale 设置
        locale.setlocale(locale.LC_ALL, '')
            
        # 获取当前 locale 
        lang_code, encoding = locale.getlocale()
        return lang_code
    
    except:
        # 出错返回默认值
        return 'en_US'



## 加载翻译文件
def load_translations():
    # 获取系统语言
    lang_code = get_system_language()

    # 加载相应语言
    if lang_code == None:
        lang_file_name = 'en_US.json'
        # Win 11 Pro 24H2 zh 返回了 Chinese (Simplified)_China 而不是zh_CN，麻了
    elif lang_code.startswith('zh') or 'chinese' in lang_code.lower():
        lang_file_name = 'zh_CN.json'
    else:
        lang_file_name = 'en_US.json'

    file_path = os.path.join('lang', lang_file_name)

    try:
        # 打开本地化文件
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        # 打开失败
    except FileNotFoundError:
        print(f"Warning: Language file not found at '{file_path}'. Defaulting to English.")
        # 返回安全的默认值
        # 把英文的字典文件复制一份在这保证安全
        return {
            "path_input": "Please enter game path, e.g.: ",
            "path_invalid_mes": "Invalid path!",
            "startup_meta_file_created": "Successfully created startup.meta file at the following path: ",
            "current_password": "Current private session password is: ",
            "IOError": "Error: Operation failed. Details: ",
            "startup_meta_file_notfound": "startup.meta file not found, no action needed.",
            "startup_meta_file_disabled": "Renamed startup.meta to startup.meta.disabled.",
            "solo_mode_off": "Solo session mode disabled. The game will now connect normally.",
            "rs_lobby_manager_title": "RS Lobby Manager",
            "ver": "Version: ",
            "supported_games": "Supported Games: ",
            "check_for_updates": "Check for updates: ",
            "option_list_title": "Please select an option: ",
            "option_1_solo": "  1. Enable [SOLO] Session (random password)",
            "option_2_private": "  2. Enable [PRIVATE] Session (to play with friends)",
            "option_3_disable": "  3. [DISABLE] Solo Mode (restore normal game)",
            "option_4_exit": "  4. Exit",
            "prompt_choice": "Please enter your choice (1-4): ",
            "prompt_password": "Please enter the password you want to use (ensure friends use the same one): ",
            "error_password_empty": "Error: Password cannot be empty!",
            "exit_message": "Thanks for using, goodbye!",
            "error_invalid_choice": "Invalid input. Please enter a number between 1 and 4.",
            "prompt_continue": "\nPress Enter to continue..."
        }
T = load_translations()

# 获取游戏路径
def get_game_path():
    # 提示用户输入路径
    while True:
        rdr_path = input(f'{T['path_input']}{os.path.join('C:',os.sep,'Program Files','Epic Games','RedDeadRedemption2')}')
        # rdr_path是路径 以及 其下有x64和data
        if os.path.isdir(rdr_path) and os.path.isdir(os.path.join(rdr_path, "x64", "data")):
            # 返回路径
            return os.path.join(rdr_path, "x64", "data")
        else:
            print(f'{T['path_invalid_mes']}')
    
    

# 创建startup.meta
def create_meta_file(target_path, password):

    # 根据给定的密码，在目标路径创建 startup.meta 文件。
    #########
    # TODO 根据路径判断游戏，选择是GTA5模板或RDR2模板
    #########

    # 将模板中的占位符替换为实际密码
    content = rdo_startup_meta_template.replace("===PasswordHere===", password)
    file_path = os.path.join(target_path, "startup.meta")

    try:
        # 使用 'with open' 可以确保文件被正确关闭，即使发生错误
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{T['startup_meta_file_created']}\n{file_path}")
        print(f"{T['current_password']}{password}")
        return True
    except IOError as e:
        print(f"{T['IOError']}{e}")
        return False

def disable_solo_mode(target_path):

    # 重命名 startup.meta 文件来禁用单人战局模式。

    original_file = os.path.join(target_path, "startup.meta")
    renamed_file = os.path.join(target_path, "startup.meta.disabled")

    if not os.path.exists(original_file):
        print(f"{T['startup_meta_file_notfound']}")
        return

    try:
        # 已存在一个 disabled 文件，先删除
        if os.path.exists(renamed_file):
            os.remove(renamed_file)
        os.rename(original_file, renamed_file)
        print(f"{T['startup_meta_file_disabled']}\n{T['solo_mode_off']}")
    except IOError as e:
        print(f"{T['IOError']}{e}")

def main():

    # 程序主函数，显示菜单并处理用户输入。

    print("==============================================")
    print(f" {T['rs_lobby_manager_title']} {T['ver']}v1.1 (CLI) ")
    print(f" {T['supported_games']}RDR2 Online (RDO) ")
    print(f" {T['check_for_updates']}https://github.com/hugsyf/RSLobbyManager ")
    print("==============================================")

    game_data_path = get_game_path()

    while True:
        print(f"\n{T['option_list_title']}")
        print(T['option_1_solo'])
        print(T['option_2_private'])
        print(T['option_3_disable'])
        print(T['option_4_exit'])

        choice = input(T['prompt_choice'])

        if choice == '1':
            # 生成一个12位的随机字母和数字密码
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            create_meta_file(game_data_path, password)
        elif choice == '2':
            password = input(T['prompt_password'])
            if password:
                create_meta_file(game_data_path, password)
            else:
                print(T['error_password_empty'])
        elif choice == '3':
            disable_solo_mode(game_data_path)
        elif choice == '4':
            print(T['exit_message'])
            sys.exit()
        else:
            print(T['error_invalid_choice'])
        
        input(T['prompt_continue'])


if __name__ == "__main__":
    main()