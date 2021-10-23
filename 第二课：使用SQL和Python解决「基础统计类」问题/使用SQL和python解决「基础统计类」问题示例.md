# 第二课：使用SQL和Python解决「基础统计类」问题示例

根据[票选结果](https://docs.qq.com/sheet/DV1dHSFpOU2xIQXpp?tab=BB08J2)，大家最感兴趣的基础统计类问题是：
1. 对局中哪个区域/地点发生的击杀最多？不同分段是否有差异？（可以划分区域，也可以做成热力图）
2. 十分钟对线期结束时，经济领先的一方是否胜率更高

第一个问题，可能不算一个好问题：
- 很难得到简单、清晰的结论（没有好用的benchmark）
- 结论难以应用（或许冰蛙能用上这个结论）

所以，我们以第二个问题为例，讲解**思考过程**和详细实现。

## 数据获取&处理

之前说过，opendota提供了一个[在线写SQL的地方](https://www.opendota.com/explorer)，我们就用这个门槛最低的工具来解答问题。

代码很简单，但我会从0开始讲解**思考过程，本课程关于SQL知识点的讲解就这一次，自学感到非常困难的同学一定要认真了**。
（这里顺便调查一下，有多少不会SQL的人，在第一次上课时候，尝试过自学？）

解题思路
1. 寻找数据源（演示查看表定义，找到需要的字段）
2. 找一场比赛，交叉验证数据（比如dotabuff）
3. 使用Google完成SQL（初学者过程中会遇到各种困难，演示一下如果用搜索引擎解决困难）
4. 获取结果，思考如何报告结论

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

以下，假设我们的样本是随机抽的（后面在其他问题中会涉及到）


## 卡方检验
2219场比赛中，10分钟经验领先方胜率是64.8%，我能否确凿的跟别人说：10分钟经济领先胜率就高？
 - 如果只取了10场比赛，相应胜率是30%，如何解读？
 - 如果取了20w场比赛，相应胜率是60%，如果解读？

你需要学习的东西（如果利用搜索引擎找到自己需要学习的东西？）：
 - 什么是「[卡方检验（chi-squared test）](https://zh.wikipedia.org/wiki/%E5%8D%A1%E6%96%B9%E6%A3%80%E9%AA%8C)」？（学习的时候可以用在线工具，自己完成计算）
 - 什么是「假设检验」？
 - 使用python完成「卡方检验」


## 置信区间

2219场比赛中，10分钟经验领先方胜率是64.8%。 这个64.8%有多可信？我是否需要把样本量扩充到1w？10w？

在线计算器： https://www.statskingdom.com/41_proportion_confidence_interval.html

知识点讲解：https://www.khanacademy.org/math/ap-statistics/xfb5d8e68:inference-categorical-proportions/one-sample-z-interval-proportion/v/conditions-for-valid-confidence-intervals


