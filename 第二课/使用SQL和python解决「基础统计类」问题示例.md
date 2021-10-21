# 第二课：使用SQL和Python解决「基础统计类」问题示例

感觉大家的[票选结果](https://docs.qq.com/sheet/DV1dHSFpOU2xIQXpp?tab=BB08J2)，大家最感兴趣的基础统计类问题是：
1. 对局中哪个区域/地点发生的击杀最多？不同分段是否有差异？（可以划分区域，也可以做成热力图）
2. 十分钟对线期结束时，经济领先的一方是否胜率更高

第一个问题，可能不算一个好问题：
- 很难得到简单、清晰的结论（没有好用的benchmark）
- 结论难以应用（或许冰蛙能用上这个结论）

所以，我们以第二个问题为例，讲解**思考过程**和详细实现。

## 数据获取&处理

之前说过，opendota提供了一个[在线写SQL的地方](https://www.opendota.com/explorer)，我们就用这个门槛最低的工具来解答问题。

代码很简单，但我会从0开始讲解**思考过程，本课程关于SQL知识点的讲解就这一次，自学感到非常困难的同学一定要认真了**。
```
SELECT
    count(match_id) as match_count,
    count(DISTINCT match_id) as distinct_match_count,
    sum(is_gold_adv_camp_win) as gold_adv_10_min_camp_win_match_count
from 
(SELECT
    match_id, 
    radiant_win,
    game_mode,
    duration,
    radiant_gold_adv[11] as radiant_gold_adv_10,
    CASE WHEN radiant_gold_adv[11] > 0 THEN 'radiant' else 'dire' END as gold_adv_camp,
    CASE WHEN (
        ((radiant_gold_adv[11] > 0) and (radiant_win is True)) or
        ((radiant_gold_adv[11] < 0) and (radiant_win is False))
    ) THEN 1 else 0  end as is_gold_adv_camp_win
FROM matches
where game_mode = 2  and start_time >= 1630425600) t_a
```


未完成...

## 卡方检验


## 置信区间


https://www.statskingdom.com/41_proportion_confidence_interval.html


