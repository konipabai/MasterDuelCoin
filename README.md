# Master Duel Coin
一款Master Duel识别硬币正反面并统计次数的插件。



**你是否有过这种想法（当然也可能只有我有过这种想法）：**

**①** 我感觉我后手怎么这么多，Fxxx KO**MI，这硬币正反面压根不接近1:1啊！

**②** Fxxx KO**MI，今天就打三四把，怎么全是后手！

**③** 我打一天了，有点想知道今天的先后手究竟都有多少把。

这时候你就需要一个能自动帮你统计输赢硬币情况的东西了，所以插件制作经验不多的我就参考了他人的开源代码并制作出了现在这款插件，在这里要感谢一下制作 **[MasterDuelSimpleTranslateTool](https://github.com/PatchouliTC/MasterDuelSimpleTranslateTool)** 的 [PatchouliTC](https://github.com/PatchouliTC) 大佬。



## **目前拥有的功能**

**①** 全自动识别硬币输赢的情况，不需要你点击上面的加减按钮，他会自主识别并在对应的硬币情况上加一。

![Coin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/show1.png)

**②** 可自主修改硬币的情况，为的是防止识别错误以及防止漏掉某一次的硬币结果，要注意这不是让你用来乱修改硬币结果的。



## **目前存在的问题**

**①** 识别的对象只是选硬币时的英文，所以这并不适用与所有玩家，后续会改。（新版本增加了简体中文，这个方法更不适用了）

![HeadCoin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/headCoin.png)



![tailCoin](https://raw.githubusercontent.com/konipabai/MasterDuelCoin/main/image/tailCoin.png)

**②** 会生成两个图片再删除，如果直接放桌面使用会有点影响感观。



## **后续有时间的话可能会添加的东西（虽然大概率没时间）**

**①** 将识别的对象改成硬币，方便更多人能使用上该插件。（加急制作中）

**②** 自动记忆插件的窗口位置，让用户不用每次打开插件都要拖拉到对应位置。

**③** 添加调节字体大小的功能。

**④** 添加是否置顶的功能。

**⑤** 添加重置硬币情况的功能。

**⑥** 修改外观（大概率不会改了，功能实用就已经满足绝大部分用户了）。

**⑦** 添加统计胜场，负场，最高连胜，最高连败功能。

**⑧** 添加一个X乘X的方格，每打完一把就把带颜色的 <font color="green">胜</font> 或者 <font color="red">负</font> 字填上去，方便一眼丁真。



## TIPS

**①** 使用插件时有可能被识别成病毒，如果你是从我提供的下载地址下载的，那就可以信任他并放心使用，这也是比较常见的问题了，实在不放心可以检查源码，运行源码，自己手动打包成 exe。

**②** 使用的识别方式为直接对游戏界面进行截图对比，不读内存。

**③** 使用管理员身份启动，插件的路径不要含有中文。

**④** 如果想直接将 exe 文件放在桌面使用，尽量新建一个快捷方式来指向该 exe 文件，或者将该 exe 文件放在一个文件夹中，因为插件运行时会生成两张图片，如果 exe 文件直接放桌面则会在桌面生成，当然，程序结束的时候会自动删除这两张图片。

**⑤** 开源协议：**[MIT](https://github.com/konipabai/MasterDuelCoin/blob/main/LICENSE)**

**⑥** 本人接触的相关插件不多，对github的使用也不多，如有何处冒犯或者更好的建议，可以直接issue。



最后感谢你的支持！
