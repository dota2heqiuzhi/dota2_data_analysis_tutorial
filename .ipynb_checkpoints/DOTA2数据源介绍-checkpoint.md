## [V社提供的官方API](https://wiki.teamfortress.com/wiki/WebAPI)

简介：有个很老的[使用说明](https://dev.dota2.com/forum/dota-2/spectating/replays/webapi/60177-things-you-should-know-before-starting?t=58317)，几乎没有人在维护了。

使用限制：你必须申请一个[key](https://steamcommunity.com/dev)，速度限制1秒1次

一般用来做什么：
 - 获取公开比赛基本数据，优势是可以**全量获取**；劣势是只有对局的基本数据（比如对局基本维度、赛后的KDA等），无法获取通过录像解析得到的详细/复杂数据（比如击杀肉山的次数、插眼次数等）
 - 英雄基本信息、装备基本信息

## [Opendota网站提供的API](https://www.opendota.com/api-keys)

简介：[API接口文档](https://docs.opendota.com/)

使用限制：免费版（1秒1次，每月50000次）

一般用来做什么：
 - 提供了数据库，可以直接查询对局、英雄等各种信息，这里有[数据表定义](https://github.com/odota/core/blob/master/sql/create_tables.sql)
 - 提供了一个线上[写SQL的地方](https://www.opendota.com/explorer?minDate=2021-08-11T04%3A39%3A45.904Z)，可以用来练习（底层是PostgreSQL）
 - 优势是opendota已经帮你解析了一部分对局的录像，可以**获取对局的详细/复杂数据**

## 我自己做的数据库

简介：提供近1个月全量公开所有对局基本数据（通过官方API获取）

优势：提供**全量对局**数据，方便抽样（比如随机抽取昨天国服2w场对局）；劣势：单机部署，速度较慢

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