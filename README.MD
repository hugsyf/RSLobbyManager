[简体中文](#rs-lobby-manager) | [English](#rs-lobby-manager-english)

---

## R星游戏战局管理器 (RS Lobby Manager) <a name="rs-lobby-manager"></a>

这是一个简单的 Python 命令行工具，旨在帮助 PC 版《荒野大镖客：救赎2》和《侠盗猎车手V》（GTAV）在线模式的玩家轻松进入单人战局或与朋友的私密战局，从而避开公共战局中泛滥的外挂，获得更纯粹的游戏体验。

### 目录

- [项目简介](#项目简介)
- [工作原理](#工作原理)
- [主要功能](#主要功能)
- [如何使用](#如何使用)
- [未来计划](#未来计划)
- [许可证](#许可证)
- [免责声明](#免责声明)

### 项目简介

众所周知，PC 版的 RDOL 公共战局环境不佳，常常会遇到使用外挂的作弊者，影响正常游戏。本工具通过一个早已被社区验证的安全方法，让玩家可以被分配到一个只有自己的战局中。同时，此方法也支持让使用相同密码的朋友们进入到同一个私密战局中。

本工具为命令行界面（CLI）。

### 工作原理

本工具的原理是在相应的游戏数据目录 (例如：`RedDeadRedemption2\x64\data`) 中创建一个名为 `startup.meta` 的特殊文件。R星服务器在进行匹配时，会校验这个文件的内容。

- 当你使用一个**独一无二**的内容（由随机密码生成）时，服务器找不到其他拥有相同文件的玩家，因此会将你分配到一个独立的战局中。
- 当你和你的朋友使用**完全相同**的内容（由你们约定的密码生成）时，服务器会将你们匹配到同一个战局中。
- 当删除或重命名此文件时，游戏恢复默认的匹配机制，你将进入公共战局。

这个方法从游戏登陆 PC 平台以来一直有效且被认为是安全的。

### 主要功能

- **一键开启单人战局**：自动生成一个随机密码，创建 `startup.meta` 文件，让你进入一个只有你自己的世界。
- **创建私人密码战局**：允许你输入自定义密码，方便与同样设置了此密码的朋友联机。
- **恢复普通战局**：通过重命名 `startup.meta` 文件来安全地禁用此功能，让你随时能回到热闹（或混乱）的公共战局。
- **简单易用**：纯命令行交互，根据提示选择即可，无需手动编辑任何文件。

### 支持的游戏

- 《荒野大镖客：救赎2》（以及Online）
- 《GTAV 传承版》
### 如何使用

#### 1. 环境要求
- 已安装 [Python 3](https://www.python.org/downloads/)。需要将 Python 添加到路径（`Add Python to PATH`）

#### 2. 获取项目
**A：使用 Git**
```bash
git clone https://github.com/hugsyf/RSLobbyManager.git
```
**B：下载 ZIP**
直接在 GitHub 仓库页面点击 `Code` -> `Download ZIP`，然后解压到任意文件夹。

#### 3. 运行脚本
1. 使用命令行工具（如 `cmd` 或 `PowerShell`）运行脚本，或直接双击运行。
2. 程序启动后，会首先提示你输入 RDR2 的游戏安装根目录。
3. 之后按照菜单提示选择相应的功能即可。

### 未来计划

本项目仍处于早期阶段，未来的（也许会做）改进计划：

- [◐] **路径自动检测**：尝试通过读取 Windows 注册表等方式，自动查找 RDR2 的安装位置。
- [◐] **扩展支持其他R星游戏**：GTA5 (传承版以及扩展和增强版)
- [ ] **GUI**：图形界面

### 许可证

本项目采用 [MIT 许可证](LICENSE)。

### 免责声明

- 本工具是一个第三方项目，与 Rockstar Games 或 Take-Two Interactive 没有任何关联。
- 使用本工具修改游戏行为可能存在违反游戏最终用户许可协议（EULA）的**潜在风险**。尽管此方法被广泛使用且未见导致封禁的案例，但风险依然存在。
- **请自行承担使用本工具带来的一切风险**。开发者不对任何可能造成的游戏账号问题（如封禁等）负责。

---

## RS Lobby Manager (English) <a name="rs-lobby-manager-english"></a>

This is a simple Python command-line tool designed to help PC players of Red Dead Online (RDO) and GTAOL easily get into solo or private, friend-only sessions. This allows for a purer gaming experience by avoiding the prevalence of cheaters in public lobbies.

### Table of Contents

- [Introduction](#introduction)
- [How It Works](#how-it-works)
- [Features](#features)
- [How to Use](#how-to-use)
- [Future Plans](#future-plans)
- [License](#license)
- [Disclaimer](#disclaimer)

### Introduction

As many know, the environment in public lobbies on the PC version of RDOL is often poor, with frequent encounters with cheaters that disrupt normal gameplay. This tool utilizes a community-verified safe method to place you in a session by yourself. This method also supports allowing friends who use the same password to join the same private session.

This tool currently features a command-line interface (CLI).

### How It Works

The tool works by creating a special file named `startup.meta` in the game data directory (Example: `RedDeadRedemption2\x64\data`). When matchmaking, the Rockstar Games server checks the content of this file.

- When you use **unique** content (generated via a random password), the server cannot find any other players with an identical file, so it places you in a solo session.
- When you and your friends use **identical** content (from a password you agree upon), the server matches you all into the same session.
- When this file is deleted or renamed, the game reverts to its default matchmaking behavior, and you will join public lobbies.

This method has been effective and is considered safe since the game's launch on PC.

### Features

- **One-Click Solo Session**: Automatically generates a random password and creates the `startup.meta` file to place you in a world of your own.
- **Create Private Password Session**: Allows you to enter a custom password, making it easy to connect with friends who use the same password.
- **Restore Normal Lobbies**: Safely disables the feature by renaming the `startup.meta` file, allowing you to return to lively (or chaotic) public lobbies at any time.
- **Simple and Easy to Use**: Purely command-line based; just follow the prompts to make your selection without needing to manually edit any files.

### Supported Games

- Red Dead Redemption 2 (& Online)
- Grand Theft Auto V Legacy

### How to Use

#### 1. Prerequisites
- [Python 3](https://www.python.org/downloads/) must be installed. Ensure you select `Add Python to PATH` during installation.

#### 2. Getting the Project
**A: Using Git**
```bash
git clone https://github.com/hugsyf/RSLobbyManager.git
```
**B: Download ZIP**
Click `Code` -> `Download ZIP` on the main GitHub repository page, then extract it to any folder.

#### 3. Running the Script
1. Run the script using a command-line tool (like `cmd` or `PowerShell`), or by double-clicking it directly.
2. When the program starts, it will first prompt you to enter the root installation directory of your RDR2 game.
3. Afterward, simply follow the menu prompts to select the desired function.

### Future Plans

This project is still in its early stages. Potential future improvements include:

- [◐] **Automatic Path Detection**: Attempting to automatically find the RDR2 installation location by reading the Windows Registry or other methods.
- [◐] **Extend Support to Other Rockstar Games**: Grand Theft Auto V (Legacy, Extended & Enhanced versions).
- [ ] **GUI**: A graphical user interface.

### License

This project is licensed under the [MIT License](LICENSE).

### Disclaimer

- This tool is a third-party project and is not affiliated with Rockstar Games or Take-Two Interactive in any way.
- Using this tool to modify game behavior carries a **potential risk** of violating the End-User License Agreement (EULA). Although this method is widely used and no cases of bans have been reported, the risk still exists.
- **You assume all risks associated with using this tool**. The developer is not responsible for any potential account issues (such as bans, etc.) that may arise.