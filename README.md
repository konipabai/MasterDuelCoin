# Master Duel Coin
一款Master Duel识别硬币正反面并统计次数的插件。



**你是否有过这种想法（当然也可能只有我有过这种想法）：**

**①** 我感觉我后手怎么这么多，Fxxx KO**MI，这硬币正反面压根不接近1:1啊！

**②** Fxxx KO**MI，今天就打三四把，怎么全是后手！

**③** 我打一天了，有点想知道今天的先后手究竟都有多少把。（特别是DC杯准备上大分的大佬们）

这时候你就需要一个能自动帮你统计输赢硬币情况的东西了，所以插件制作经验不多的我就参考了他人的开源代码并制作出了现在这款插件，在这里要感谢一下制作 **[MasterDuelSimpleTranslateTool](https://github.com/PatchouliTC/MasterDuelSimpleTranslateTool)** 的 [PatchouliTC](https://github.com/PatchouliTC) 大佬。



## **目前拥有的功能**

**①** 全自动识别硬币输赢的情况，不需要你点击上面的加减按钮，他会自主识别并在对应的硬币情况上加一。

![Coin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/show1.png)

**②** 可自主修改硬币的情况，为的是防止识别错误以及防止漏掉某一次的硬币结果，要注意这不是让你用来乱修改硬币结果的。



## **目前存在的问题**

**①** ~~识别的对象只是选硬币时的英文，所以这并不适用与所有玩家，后续会改。~~（新版本增加了简体中文，这个方法更不适用了）<font color="green">（已解决改成了识别硬币）</font>

![HeadCoin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/headCoin.png)



![tailCoin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/tailCoin.png)

**②** 插件启动时会生成拿来对比的两个硬币图片，关闭插件的时候会自动删除，所以如果在同时打开两个此插件的时候关闭插件一，插件二会因为插件一关闭时删除了拿来对比的两个硬币图片而无法正常运行。<font color="red">（虽然可以通过不生成图片（这样就不会出现上面的情况），直接读取本地图片来对比，但目前发现有部分使用者使用我提供的本地图片文件来运行程序会识别遗漏，他们自己生成的图片就不会遗漏，所以不打算改，有知道是什么原因造成的大佬可以跟我反馈一下）</font>

**③** 如果在丢硬币的界面关闭游戏，插件很有可能报错，或者不报错，但后续不再自动识别硬币情况。<font color="red">（不打算改，不会有正常玩家特地去进行这种操作，正常玩家碰到这种情况也是少数，如果改了，基本上只会方便拔线狗）</font>



## **后续有时间的话可能会添加的东西（虽然大概率没时间）**

**①** 将识别的对象改成硬币，方便更多人能使用上该插件。<font color="green">（已完成）</font>

**②** 自动记忆插件的窗口位置以及窗口大小，让用户不用每次打开插件都要拖拉到对应位置以及调整大小。<font color="green">（已完成）</font>

**③** 添加调节字体大小的功能。<font color="green">（已完成）</font>

**④** 添加是否置顶的功能。<font color="green">（已完成）</font>

**⑤** 添加重置硬币情况的功能。

**⑥** 修改外观（大概率不会改了，功能实用就已经满足绝大部分用户了）。

**⑦** 添加统计胜场，负场，最高连胜，最高连败功能。

**⑧** 添加一个X乘X的方格，每打完一把就把带颜色的 <font color="green">胜</font> 或者 <font color="red">负</font> 字填上去，方便一眼丁真。

**⑨** 添加显示赢硬币率，输硬币率，最近X局输赢硬币数。

**⑩** 添加将硬币情况写入本地新创建的 txt 文件功能（以写入时的时间为文件名，例：2023-03-16=17：04：01.txt）。



## TIPS

**①** 使用插件时有可能被识别成病毒，如果你是从我提供的下载地址下载的，那就可以信任他并放心使用，这也是比较常见的问题了，实在不放心可以检查源码，运行源码，自己手动打包成 exe。

**②** 使用的识别方式为直接对游戏界面进行截图对比，不读内存。

**③** 使用管理员身份启动，插件的路径不要含有中文。

**④** 识别不是百分百识别到，插件本身并不完善，还是会存在识别遗漏以及识别错误的情况的。

**⑤** 开源协议：**[MIT](https://github.com/konipabai/MasterDuelCoin/blob/main/LICENSE)**

**⑥** 插件制作经验不多，所以代码写得不是很好，使用过程中占用电脑资源可能比较多，可能产生卡顿，因为识别频率设置得有点高，在游戏中硬币的出现就一瞬间，识别频率不高很可能漏识别。

**⑦** 如果程序识别率特别低，或者不自动识别了，都可以试着重开插件，重开游戏，两者都不能改善的时候就来github或者B站反馈吧~。

**⑧** 假设有一天官方明确表明不能进行获取游戏界面的操作，请立即停止使用本插件。

**⑨** 如果同时打开了两个插件，关闭其中一个，另一个不会正常运行，需要两个都关闭再打开一个才能正常运行。

**⑩** 本人大学生萌新，接触的相关插件不多，对github的使用也不多，如有何处冒犯或者更好的建议，可以直接[issue](https://github.com/konipabai/MasterDuelCoin/issues)或[B站](https://space.bilibili.com/29666002)联系，记得带上涉及问题的截图。

最后感谢你的支持！可以的话为我点个 Star 吧！
