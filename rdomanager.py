import os
import string
import random
import sys

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

# 获取游戏路径
def get_game_path():
    # 提示用户输入路径
    while True:
        rdr_path = input('请输入RDR2游戏路径，示例：C:\\Program Files\\Epic Games\\RedDeadRedemption2')
        # rdr_path是路径 以及 其下有x64和data
        if os.path.isdir(rdr_path) and os.path.isdir(os.path.join(rdr_path, "x64", "data")):
            # 返回路径
            return os.path.join(rdr_path, "x64", "data")
        else:
            print('路径无效！')

# 创建startup.meta
def create_meta_file(target_path, password):

    # 根据给定的密码，在目标路径创建 startup.meta 文件。

    # 将模板中的占位符替换为实际密码
    content = rdo_startup_meta_template.replace("===PasswordHere===", password)
    file_path = os.path.join(target_path, "startup.meta")

    try:
        # 使用 'with open' 可以确保文件被正确关闭，即使发生错误
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"成功！已在以下路径创建 startup.meta 文件：\n{file_path}")
        print(f"当前战局密码为: {password}")
        return True
    except IOError as e:
        print(f"错误：无法写入文件！请检查权限。错误详情: {e}")
        return False

def disable_solo_mode(target_path):

    # 重命名 startup.meta 文件来禁用单人战局模式。

    original_file = os.path.join(target_path, "startup.meta")
    renamed_file = os.path.join(target_path, "startup.meta.disabled")

    if not os.path.exists(original_file):
        print("提示：未找到 startup.meta 文件，无需禁用。")
        return

    try:
        # 已存在一个 disabled 文件，先删除
        if os.path.exists(renamed_file):
            os.remove(renamed_file)
        os.rename(original_file, renamed_file)
        print(f"成功！已将 startup.meta 重命名为 startup.meta.disabled。")
        print("单人战局模式已关闭，游戏将正常联网。")
    except IOError as e:
        print(f"错误：操作失败！请检查权限。错误详情: {e}")

def main():

    # 程序主函数，显示菜单并处理用户输入。

    print("==============================================")
    print(" RDR2 Online 单人战局小工具 v1.0 (CLI) ")
    print("==============================================")

    game_data_path = get_game_path()

    while True:
        print("\n请选择要执行的操作:")
        print("  1. 开启【单人】战局 (随机密码)")
        print("  2. 开启【密码】战局 (与好友联机)")
        print("  3. 【关闭】单人模式 (恢复正常游戏)")
        print("  4. 退出")

        choice = input("请输入你的选择 (1-4): ")

        if choice == '1':
            # 生成一个12位的随机字母和数字密码
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            create_meta_file(game_data_path, password)
        elif choice == '2':
            password = input("请输入你想用的密码 (请确保好友使用相同的密码): ")
            if password:
                create_meta_file(game_data_path, password)
            else:
                print("错误：密码不能为空！")
        elif choice == '3':
            disable_solo_mode(game_data_path)
        elif choice == '4':
            print("感谢使用")
            sys.exit()
        else:
            print("无效的输入，请输入 1 到 4 之间的数字。")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()