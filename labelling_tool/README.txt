# README
- 环境
1. sox
2. python2.7

1\安装brew uby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2\brew install sox

- 操作说明
1. 单击<选择音频>按钮，添加待标注音频路径
2. 自动完成加载音频
3. 单击<开始>按钮,开始标注
4. 单击左边栏音频可以播放
5. 单击<重播>按钮可以重听
6. 单击<上一首>/<下一首>按钮可以切换音频
7. 单击<安静小BIU>按钮标注为“安静小BIU”
8. 单击<噪声小BIU>按钮标注为“噪声小BIU”
9. 单击<其他音频>按钮可以标注为“其他音频”
10. 单击<结束>结束标注。
11. 标注文件存放在新建的log目录中

注意：
- 每次播放完一首后才能播放下一首，否则会有交叠
- 首次运行软件标注必须点击<开始>按钮
- 结束标注一定要点击<结束>按钮
- 关闭软件点击左上角的叉叉关闭
- 右下角显示栏会显示提示和状态

build mac app
python2 setup.py py2app
修改labelling.app/Contents/Resources/config.ini
导出labelling.app/Contents/Resources/log 中的日志(标注结果)
