import os
import string
import random
import sys
import json
import locale
import winreg
import re

#########
# RDR2 & GTA5 Legacy 的模板
#########
rdo_startup_meta_template = '''<?xml version="1.0" encoding="UTF-8"?>
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
</CDataFileMgr__ContentsOfDataFileXml>===PasswordHere==='''

gta5_startup_meta_template = '''<?xml version="1.0" encoding="UTF-8"?>
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
       <filename>platform:/data/cdimages/scaleform_frontend.rpf</filename>
       <fileType>RPF_FILE_PRE_INSTALL</fileType>
      </Item>
     </dataFiles>
    <contentChangeSets itemType="CDataFileMgr__ContentChangeSet" />
    <dataFiles itemType="CDataFileMgr__DataFile" />
    <patchFiles />
</CDataFileMgr__ContentsOfDataFileXml>                     
<!--===PasswordHere===-->'''
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
            "prompt_continue": "\nPress Enter to continue...",
            "auto_detected_games": "Auto-detected games:",
            "manual_input": "Manual input",
            "select_game_prompt": "Please select a game (0 for manual input): ",
            "invalid_choice": "Invalid choice. Please try again.",
            "manual_path_input": "Manual path input:",
            "or": "or",
            "game_detected": "Game detected: ",
            "current_game": "Current game: "
        }
T = load_translations()

# 自动检测游戏路径
def auto_detect_games():
    detected_games = []
    
    # 检测 Steam 游戏
    try:
        steam_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(steam_key, "SteamPath")
        winreg.CloseKey(steam_key)
        
        # Steam库文件夹
        libraryfolders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        steam_paths = [os.path.join(steam_path, "steamapps", "common")]
        
        # 读取额外的Steam库路径
        if os.path.exists(libraryfolders_path):
            try:
                with open(libraryfolders_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    paths = re.findall(r'"path"\s*"([^"]+)"', content)
                    for path in paths:
                        steam_paths.append(os.path.join(path.replace("\\\\", "\\"), "steamapps", "common"))
            except:
                pass
        
        # 检查Steam游戏
        for steam_common in steam_paths:
            # GTA5
            gta5_steam = os.path.join(steam_common, "Grand Theft Auto V")
            if os.path.exists(gta5_steam) and os.path.exists(os.path.join(gta5_steam, "x64", "data")):
                detected_games.append((os.path.join(gta5_steam, "x64", "data"), "GTA5", "Steam"))
            
            # RDR2
            rdr2_steam = os.path.join(steam_common, "Red Dead Redemption 2")
            if os.path.exists(rdr2_steam) and os.path.exists(os.path.join(rdr2_steam, "x64", "data")):
                detected_games.append((os.path.join(rdr2_steam, "x64", "data"), "RDR2", "Steam"))
    except:
        pass
    
    # 检测 Epic Games
    try:
        epic_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher")
        epic_path, _ = winreg.QueryValueEx(epic_key, "AppDataPath")
        winreg.CloseKey(epic_key)
        
        # Epic Games 清单文件路径
        manifests_path = os.path.join(os.path.dirname(epic_path), "UnrealEngineLauncher", "LauncherInstalled.dat")
        if os.path.exists(manifests_path):
            try:
                with open(manifests_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data.get("InstallationList", []):
                        install_path = item.get("InstallLocation", "")
                        app_name = item.get("AppName", "")
                        
                        if "rdr2" in app_name.lower() and os.path.exists(os.path.join(install_path, "x64", "data")):
                            detected_games.append((os.path.join(install_path, "x64", "data"), "RDR2", "Epic"))
                        elif "gta" in app_name.lower() and os.path.exists(os.path.join(install_path, "x64", "data")):
                            detected_games.append((os.path.join(install_path, "x64", "data"), "GTA5", "Epic"))
            except:
                pass
    except:
        pass
    
    # 检测 Rockstar Games Launcher
    try:
        rockstar_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Rockstar Games")
        subkeys = []
        try:
            i = 0
            while True:
                subkey = winreg.EnumKey(rockstar_key, i)
                subkeys.append(subkey)
                i += 1
        except WindowsError:
            pass
        winreg.CloseKey(rockstar_key)
        
        for subkey in subkeys:
            try:
                game_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SOFTWARE\\WOW6432Node\\Rockstar Games\\{subkey}")
                install_path, _ = winreg.QueryValueEx(game_key, "InstallFolder")
                winreg.CloseKey(game_key)
                
                if os.path.exists(os.path.join(install_path, "x64", "data")):
                    if "gta" in subkey.lower() or "grand theft auto" in subkey.lower():
                        detected_games.append((os.path.join(install_path, "x64", "data"), "GTA5", "Rockstar"))
                    elif "red dead" in subkey.lower() or "rdr" in subkey.lower():
                        detected_games.append((os.path.join(install_path, "x64", "data"), "RDR2", "Rockstar"))
            except:
                continue
    except:
        pass
    
    return detected_games

# 获取游戏路径和类型
def get_game_path():
    # 尝试自动检测
    detected_games = auto_detect_games()
    
    if detected_games:
        print(f"\n{T['auto_detected_games']}")
        for i, (path, game_type, platform) in enumerate(detected_games, 1):
            game_name = "Grand Theft Auto V" if game_type == "GTA5" else "Red Dead Redemption 2"
            print(f"  {i}. {game_name} ({platform})")
        print(f"  0. {T['manual_input']}")
        
        while True:
            try:
                choice = input(f"{T['select_game_prompt']}")
                if choice == "0":
                    break
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(detected_games):
                    return detected_games[choice_idx][0], detected_games[choice_idx][1]
                else:
                    print(f"{T['invalid_choice']}")
            except ValueError:
                print(f"{T['invalid_choice']}")
    
    # 手动输入路径
    print(f"\n{T['manual_path_input']}")
    while True:
        game_path = input(f'{T['path_input']}{os.path.join('C:',os.sep,'Program Files','Steam','steamapps','common','Grand Theft Auto V')} {T['or']} {os.path.join('C:',os.sep,'Program Files','Epic Games','RedDeadRedemption2')}\n> ')
        
        # 检查是否为有效的游戏路径
        data_path = os.path.join(game_path, "x64", "data")
        if os.path.isdir(game_path) and os.path.isdir(data_path):
            # 判断游戏类型
            if any(keyword in game_path.lower() for keyword in ["grand theft auto", "gtav", "gta5", "gta v"]):
                game_type = "GTA5"
            elif any(keyword in game_path.lower() for keyword in ["red dead", "rdr2"]):
                game_type = "RDR2"
            else:
                # 通过检查特定文件来判断游戏类型
                if any(os.path.exists(os.path.join(game_path, exe)) for exe in ["GTA5.exe", "GTAVLauncher.exe", "PlayGTAV.exe"]):
                    game_type = "GTA5"
                elif any(os.path.exists(os.path.join(game_path, exe)) for exe in ["RDR2.exe", "RedDeadRedemption2.exe"]):
                    game_type = "RDR2"
                else:
                    game_type = "UNKNOWN"
            
            return data_path, game_type
        else:
            print(f'{T['path_invalid_mes']}')
    

# 创建startup.meta
def create_meta_file(target_path, password, game_type):
    # 根据给定的密码和游戏类型，在目标路径创建 startup.meta 文件。
    
    # 根据游戏类型选择模板
    if game_type == "GTA5":
        template = gta5_startup_meta_template
    else:  # RDR2 或其他
        template = rdo_startup_meta_template
    
    # 将模板中的占位符替换为实际密码
    content = template.replace("===PasswordHere===", password)
    file_path = os.path.join(target_path, "startup.meta")

    try:
        # 使用 'with open' 可以确保文件被正确关闭，即使发生错误
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        game_name = "Grand Theft Auto V" if game_type == "GTA5" else "Red Dead Redemption 2"
        print(f"{T['startup_meta_file_created']}\n{file_path}")
        print(f"{T['game_detected']}{game_name}")
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
    print(f" {T['rs_lobby_manager_title']} {T['ver']}v1.2 (CLI) ")
    print(f" {T['supported_games']}RDR2 Online (RDO) & GTA5 Online ")
    print(f" {T['check_for_updates']}https://github.com/hugsyf/RSLobbyManager ")
    print("==============================================")

    game_data_path, game_type = get_game_path()

    while True:
        game_name = "Grand Theft Auto V" if game_type == "GTA5" else "Red Dead Redemption 2"
        print(f"\n{T['current_game']}{game_name}")
        print(f"\n{T['option_list_title']}")
        print(T['option_1_solo'])
        print(T['option_2_private'])
        print(T['option_3_disable'])
        print(T['option_4_exit'])

        choice = input(T['prompt_choice'])

        if choice == '1':
            # 生成一个12位的随机字母和数字密码
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            create_meta_file(game_data_path, password, game_type)
        elif choice == '2':
            password = input(T['prompt_password'])
            if password:
                create_meta_file(game_data_path, password, game_type)
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