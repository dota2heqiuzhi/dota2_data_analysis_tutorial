# 第一课：与其感慨路难行，不如马上出发

## 课程运作方式

（×）校园模式：逐一讲解知识点、讲案例、完成作业

（√）自学模式：自己提出问题——票选最有意思的问题——自学知识点——一起完成分析，输出结论

**为什么问题很重要？**

因为学习对大部分人来说，是一件痛苦的事情，一个好的问题可以指引你走下去。（大多数人喜欢美食，但不喜欢做饭、洗碗，自己选的问题吃起来会更香一点）

**为什么主要靠自学？**

背景不一样（有基础尚可的；也有在其他行业基础尚可的），目标不一样，自学效率更高。

## 数据分析师的自我修养

1. **自学能力、搜索引擎使用能力**：遇事不决先Google，最好能科学上网（狂战斧 vs 补刀斧）
2. **获取/处理数据、代码能力**
   * [SQL](https://www.liaoxuefeng.com/wiki/1177760294764384)（结构化查询语言）
   * [python](https://www.liaoxuefeng.com/wiki/1016959663602400)（编程语言），重点学习pandas等数据分析常用lib
   * [jupyter](https://jupyter.org/)（好用的数据分析编程环境）
   * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)（简单爬虫需要掌握的lib）等其他你需要使用的lib
3. **数据分析基本思维**
   * 易读的书籍：《赤裸裸的统计学》、《精益数据分析》
   * 知乎大v的内容：[2018 年中国出生人口有多少？- chenqin的回答](https://www.zhihu.com/question/306388374/answer/571155588)
   * 其他你感兴趣的数据类读物，当故事来看就行，以了解作者的分析思路为主
4. **统计知识和数据分析常用方法**
   * 统计知识可以找一套教程系统学习（可以浅尝辄止，等实际项目用到某个知识点时，再完全吃透这个知识点）[数理统计讲义](https://bookdown.org/hezhijian/book/)、[Probability for Computer Scientists](http://web.stanford.edu/class/cs109/)、[Statistics and probability](https://www.khanacademy.org/math/statistics-probability)

     [视频](https://www.khanacademy.org/math/statistics-probability)\]

   * [因果推断Causal Inference系列博文](https://matheusfacure.github.io/python-causality-handbook/landing-page.html)（强烈推荐）
   * 进阶向：[机器学习免费网课](https://www.coursera.org/learn/machine-learning)
5. **可视化**
   * 作图工具：[tableau](https://www.tableau.com/)
   * 作图思维：[《Storytelling with Data》](http://www.bdbanalytics.ir/media/1123/storytelling-with-data-cole-nussbaumer-knaflic.pdf)（讲可视化最好的一本书，强烈建议看英文原版，简单易读，受益匪浅）
6. **沟通和讲故事的能力**
7. **业务理解能力**，可能是最重要的能力！

## **DOTA2数据源介绍**

你想解决的问题，需要什么样的数据？从哪里获取？



![](https://docimg2.docs.qq.com/image/bimXqzqc9EKfg6yY6GbtlQ.png?w=760&h=681)

### [V社提供的官方API](https://wiki.teamfortress.com/wiki/WebAPI)

简介：有个很老的[使用说明](https://dev.dota2.com/forum/dota-2/spectating/replays/webapi/60177-things-you-should-know-before-starting?t=58317)，几乎没有人在维护了。

使用限制：你必须申请一个[key](https://steamcommunity.com/dev)，速度限制1秒1次

有什么数据？

* 获取公开游戏数据，优势是可以**全量获取**；劣势是只有基本数据（比如游戏时长、击杀数、助攻数等），无法获取详细/复杂数据（比如击杀肉山的次数、插眼次数等需要解析录像才能拿到的数据）
* 英雄基本信息、装备基本信息、选手信息等

### [Opendota网站提供的API](https://www.opendota.com/api-keys)

简介：[API接口文档](https://docs.opendota.com/)

使用限制：免费版（1秒1次，每月50000次）

有什么用处？

* 提供了数据库，可以直接查询对局、英雄等各种信息，这里有[数据表定义](https://github.com/odota/core/blob/master/sql/create_tables.sql)
* 提供了一个线上[写SQL的地方](https://www.opendota.com/explorer?minDate=2021-08-11T04%3A39%3A45.904Z)，新手可以作为练习工具（底层是PostgreSQL）
* 获取部分比赛的**详细/复杂数据**（opendota已经帮你解析了这部分对局的录像）

### 我自己搞的数据库

简介：提供近1个月全量公开对局基本数据（通过官方API获取） 

优势：提供**全量对局**数据，方便抽样（比如随机抽取昨天国服2w场对局）

劣势：单机部署，查询速度较慢

表结构：

```text
CREATE TABLE IF NOT EXISTS match(
    match_id bigint PRIMARY KEY,
    p_date char(8),
    match_seq_num bigint,
    start_time integer,
    duration integer,
    cluster smallint,
    lobby_type smallint,
    leagueid integer,
    game_mode smallint,
    radiant_win smallint,
    radiant_score smallint,
    radiant_pick_hero_ids varchar(30),
    radiant_ban_hero_ids varchar(30),
    dire_score smallint,
    dire_pick_hero_ids varchar(30),
    dire_ban_hero_ids varchar(30),
    human_players smallint,
    player_account_ids varchar(250)
);
```

连接信息：

```text
ip地址：dota2.heqiuzhi.xyz
端口：5432
用户名：dota2_readonly
密码: dota2
数据库： dota2
```

## 一个完整的数据分析例子

背景：DOTA2作为一款dead game，近年来不断被唱衰。但是2021年6月24号推出天陨旦新版本之后，突然有新闻说DOTA2又好起来了，反超csgo重回steam榜首。

### **那么问题来了**

1. 究竟是咋回事？是真的好起来了，还是自媒体搞事情？
2. 如果确实有大幅增长，那么增长是哪些地区带来的？国服的数据怎么样？

### **获取数据/处理数据**

* 通过第三方网站（[steamdb](https://steamdb.info/graph/?compare=570,730)），可以获取steam游戏每日用户同时在线峰值
* 通过steam官方api可以获取每日对局总数，同时能拿到对局的详细信息\(包含服务器信息），通过服务器就可以知道各地区的对局数变化趋势

有些问题很简单，看一眼[数据](https://steamdb.info/graph/?compare=570,730)就知道答案：并没有啥可观的增长，不过是同行衬托而以——CSGO暴跌了。

有些数据获取很容易。你看到自媒体的文章之后，是直接就信了，还是愿意花时间去找一下数据？

有些数据的获取比较麻烦，比如获取每日国服DOTA2游戏场次，需要解决如下问题：

* 使用python调用V社提供的官方API，每次可以获取100场比赛，限制速度每秒1次
* 想要更快，就得上IP代理+多个key并发调用API
* 想要每日例行化获取数据，可以学习Linux，搞个自己的cvm不间断运行
* 比赛信息里面的cluster字段和服务器（eg. 中国-华中电信）如何对应？找不到最新的配置表，就需要自己从dotabuff爬取

经过一番努力，我们终于把数据都获取下来了。结果很顺利：「从第三方网站获取的DOTA2每日用户同时在线峰值」和「通过steam官方api获取的每日对局总数」是能够对应上的。

![](https://docimg2.docs.qq.com/image/0NoFr6o5kdhzof91NRziSA.png?w=766&h=403)

### **通过数据分析输出结论**

通过写[代码](https://github.com/dota2heqiuzhi/dota2_data_analysis_tutorial/blob/d25525f51d4d2806df425c52022ab1c50bb10bf6/%E7%AC%AC%E4%B8%80%E8%AF%BE/%E5%A4%A9%E9%99%A8%E6%97%A6%E4%B8%8A%E7%BA%BF%E5%90%8E%E5%9B%BD%E6%9C%8D%E6%95%B0%E6%8D%AE%E5%8F%98%E5%8C%96.ipynb)把国服的数据和非国服的数据分开，对比两者的变化趋势可以发现：主要增长是由非国服地区带来的。

## 课后作业

10月2号之前，提交一个你最感兴趣的、并且想自己动手解决的DOTA2数据问题。示例：

1. 如何量化英雄组合？我发现dotamax上的英雄组合推荐很一般，应该有更好的算法
2. 我有一个朋友打影魔真的很菜，又菜又爱玩，我得用数据告诉他到底哪里菜，让他心服口服
3. 我想用SQL查询出最近一周天梯吸枫哥分最多的选手是谁

**注意：如果10月3号我没有收到你的问题，那我们的故事就结束了。**

提交方式：容我想想。

## 破冰&问答环节

有问题可以问，也可以单纯介绍下你自己。

