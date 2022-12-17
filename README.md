# MaCron
![GitHub issues](https://img.shields.io/github/issues/Ma-Ko-Dev/MaCron?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/Ma-Ko-Dev/MaCron?style=plastic)
![GitHub all releases](https://img.shields.io/github/downloads/Ma-Ko-Dev/MaCron/total?style=plastic)
![GitHub contributors](https://img.shields.io/github/contributors/Ma-Ko-Dev/Macron?style=plastic)

MaCron is a simple, lightweight utility for scheduling tasks on Windows systems. With MaCron, you can easily automate tasks such as backups, system maintenance, and data processing.

## Features

- Easy to use: MaCron uses a simple, intuitive GUI for defining tasks and schedules.
- Flexible scheduling: MaCron supports a wide range of scheduling times, including fixed intervals, and manual triggering.

- Error handling: MaCron provides robust error handling and notification features to ensure that your tasks run smoothly.

## Getting started

To install MaCron, simply download the latest build from the release section.<br>
Keep in mind that you need to have Python installed on your Machine. If the Scripts you are Scheduling with MaCron need non Built-In Modules, make sure that they are installed.

## Known Issues
For the moment, MaCron has no multiprocessing which means all scheduled scripts will run after each other. This can lead to some problems when the scheduled scripts take a long time to run. Please keep in mind that every sleep or delay in a script might freeze the GUI.<br>
But don't worry, multiprocessing will be added soon.<br>
The provided test scripts in the test_scripts folder might need additional Modules that are not listed in the requirements.txt file.

## Contributions

We welcome contributions to MaCron! If you have an idea for a new feature or a bug fix, please open an issue or a pull request. Before contributing, please read our contributor guidelines.

## License

MaCron is released under the MIT license.

## Credits:
- Menubar Icons by [Yusuke Kamiyamane.](https://p.yusukekamiyamane.com/)
- Window Icon (The 2 Macarons) [Macaron stickers created by Gohsantosadrive - Flaticon](https://www.flaticon.com/free-stickers/macaron)</a>

