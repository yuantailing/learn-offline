# Learn-Offline

## 概述

用于把清华大学网络学堂上有权限查看的课程公告、文件等下载下来。

## 用法

1. 解压 bin 文件夹下符合您的设备的包，运行 learn.exe。若安装了 python，也可以在 src 文件夹下运行 `python learn.py`。
2. 输入用于登录网络学堂的用户名和密码。
3. 如果登录成功，会列出所有支持下载的课程（不支持新版网络学堂）。
4. 输入要下载的课程的 course_id（每行第一个数字）。
5. 等待下载完成。
6. 打开下载的文件夹，文件名与网络学堂页面有如下对应关系

    | 文件名           | 对应页面 |
    | ---------------- | -------- |
    | note_list.html   | 课程公告 |
    | course_info.html | 课程信息 |
    | download.html    | 课程文件 |
    | ware_list.html   | 教学资源 |
    | homework.html    | 课程作业 |
    | talk_list.html   | 课程讨论 |

7. download 文件夹是所有课程文件
8. homework/attachment 是所有课程作业的附件

## 功能

- 有下载课程公告、课程信息、课程文件、教学资源、课程作业、课程讨论离线保存的功能。
- 课程公告含每个公告的内容，课程作业含每次作业的文字、上传文字和附件，讨论含每个帖子及其回复。
- 不含课程答疑、自由讨论区。
- 不含课程讨论区帖子的附件。
- 保留了原网页的大部分信息，而不只是文件本身。
- 正确处理了一部分样式表和图片资源。
- 可以更改 learn.config.ini 中 download_note_list 的值，1 表示下载课程公告，0 表示不下载用户公告。其它选项类似，有如下对应关系：

    | 键                     | 对应页面 |
    | ---------------------- | -------- |
    | download_course_locate | 课程首页 |
    | download_note_list     | 课程公告 |
    | download_course_info   | 课程信息 |
    | download_download      | 课程文件 |
    | download_ware_list     | 教学资源 |
    | download_homework      | 课程作业 |
    | download_bbs_list      | 课程答疑 |
    | download_talk_list     | 课程讨论 |

  其中，课程首页由于大部分浏览器的本地文件安全策略而无法正常显示；课程答疑不支持下载，即使设为 1 也不会下载。

## 说明

- 为了减少登录次数，cookie 保存在本机，在公共场所使用后请清理。
- 如果对输入密码不放心，可以手动在浏览器上登录，然后将浏览器上的 learn.tsinghua.edu.cn 域的 cookie 复制到 cookie.txt（Netscape HTTP Cookie File格式）。
- 您需要知道，网络学堂的安全防护措施较差，有可能受到 xss 注入等攻击。
- 使用本软件请遵守相关政策法规，如果不被允许，请立即停止使用本软件，并按要求删除有关数据。
