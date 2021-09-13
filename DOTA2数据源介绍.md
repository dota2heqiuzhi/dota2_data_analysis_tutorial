## [V社提供的官方API](https://wiki.teamfortress.com/wiki/WebAPI)

简介：有个很老的[使用说明](https://dev.dota2.com/forum/dota-2/spectating/replays/webapi/60177-things-you-should-know-before-starting?t=58317)，几乎没有人在维护了。

使用限制：你必须申请一个[key](https://steamcommunity.com/dev)，速度限制1秒1次

有什么数据？
 - 获取公开游戏数据，优势是可以**全量获取**；劣势是只有基本数据（比如游戏时长、击杀数、助攻数等），无法获取详细/复杂数据（比如击杀肉山的次数、插眼次数等需要解析录像才能拿到的数据）
 - 英雄基本信息、装备基本信息、选手信息等

## [Opendota网站提供的API](https://www.opendota.com/api-keys)

简介：[API接口文档](https://docs.opendota.com/)

使用限制：免费版（1秒1次，每月50000次）

有什么用处？
 - 提供了数据库，可以直接查询对局、英雄等各种信息，这里有[数据表定义](https://github.com/odota/core/blob/master/sql/create_tables.sql)
 - 提供了一个线上[写SQL的地方](https://www.opendota.com/explorer?minDate=2021-08-11T04%3A39%3A45.904Z)，新手可以作为练习工具（底层是PostgreSQL）
 - 获取部分比赛的**详细/复杂数据**（opendota已经帮你解析了这部分对局的录像）

## 我自己搞的数据库

简介：提供近1个月全量公开对局基本数据（通过官方API获取）
优势：提供**全量对局**数据，方便抽样（比如随机抽取昨天国服2w场对局）；劣势：单机部署，查询速度较慢

表结构：
```
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
```
ip地址：dota2.heqiuzhi.xyz
端口：5432
用户名：dota2_readonly
密码: dota2
数据库： dota2
```