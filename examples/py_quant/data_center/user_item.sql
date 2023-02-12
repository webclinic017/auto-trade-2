-- 物化视图的进阶使用
--  上面是物化视图的一个简单case，主要针对一些单日志的固化场景处理，减少数据量级，提高查询效率。

-- 背景
--  其实在实际使用的场景下，经常会遇到一个维度关联的问题，比如将物品的类别带入，用户的画像信息带入等场景。

--  这里简单列举下在clickhouse中做维度补全的操作。主要用到了用户维度数据和物品维度数据两个本地表，基于这两个本地表去生成内存字典，通过内存字典去做关联(字典有很多种存储结构，这里主要列举hashed模式)。

-- 字典处理过程
--  通过离线导入将数据写入了ods.user_dim_local和ods.item_dim_local两个本地表，然后通过查询dim.user_dim_dis和dim.item_dim_dis两个表提供完整数据(这里只是单机列举案例，集群模式同理)。

--  通过从clickhouse查询数据写入到内存字典中，创建字典的sql如下:

--创建user字典
CREATE DICTIONARY dim.dict_user_dim on cluster cluster (
 uid UInt64 ,
 platform String default '' ,
 country String default '' ,
 province String default '' ,
 isp String default '' ,
 app_version String default '' ,
 os_version String default '',
 mac String default '' ,
 ip String default '',
 gender String default '',
 age Int16 default -1
) PRIMARY KEY uid 
SOURCE(
  CLICKHOUSE(
    HOST 'localhost' PORT 9000 USER 'default' PASSWORD '' DB 'dim' TABLE 'user_dim_dis'
  )
) LIFETIME(MIN 1800 MAX 3600) LAYOUT(HASHED());

--创建item字典
CREATE DICTIONARY dim.dict_item_dim on cluster cluster (
 item_id UInt64 ,
 type_id UInt32 default 0,
 price UInt32 default 0
) PRIMARY KEY item_id 
SOURCE(
  CLICKHOUSE(
    HOST 'localhost' PORT 9000 USER 'default' PASSWORD '' DB 'dim' TABLE 'item_dim_dis'
  )
) LIFETIME(MIN 1800 MAX 3600) LAYOUT(HASHED())

-- 如果使用clickhouse查询分布式表提供字典数据来源，建议Host为一个查询代理，避免对某个节点产生负面效应。

-- DB和table也可以使用view封装一段sql实现。

-- 字典的数据是冗余在所有节点的，默认字典的加载方式是惰性加载，
-- 也就是需要至少一次查询才能将字典记载到内存，避免一些不使用的字典对集群带来影响。
-- 也可以通过hash分片的方式将用户指定到某个shard，那么字典也可以实现通过hash分片的方式存储在每个节点，
-- 间接实现分布式字典，减少数据存储，篇幅有限不展开介绍。

-- 在创建字典之后，可以有两种模式使用字典，一种是通过dictGet，另外一种方式是通过join，
-- 如果只查询一个key建议通过dictGet使用，代码复杂可读性高，
-- 同时字典查的value可以作为另一个查询的key，
-- 如果查多个key，可以通过dictGet或者join。

-- 类似于 select 1 as a,a+1 as b,b+1 as c from system.one这样。

--单value方法1：
SELECT
    dictGet('dim.dict_user_dim', 'platform', toUInt64(uid)) AS platform,
    uniqCombined(uid) AS uv
FROM dws.action_001_dis
WHERE day = '2021-06-05'
GROUP BY platform

-- Query id: 52234955-2dc9-4117-9f2a-45ab97249ea7

-- ┌─platform─┬───uv─┐
-- │ android  │ 9624 │
-- │ ios      │ 4830 │
-- └──────────┴──────┘

-- 2 rows in set. Elapsed: 0.009 sec. Processed 49.84 thousand rows, 299.07 KB (5.37 million rows/s., 32.24 MB/s.)

--多value方法1：
SELECT
    dictGet('dim.dict_user_dim', 'platform', toUInt64(uid)) AS platform,
    dictGet('dim.dict_user_dim', 'gender', toUInt64(uid)) AS gender,
    uniqCombined(uid) AS uv
FROM dws.action_001_dis
WHERE day = '2021-06-05'
GROUP BY
    platform,
    gender

-- Query id: ed255ee5-9036-4385-9a51-35923fef6e48

-- ┌─platform─┬─gender─┬───uv─┐
-- │ ios      │ 男     │ 2236 │
-- │ android  │ 女     │ 4340 │
-- │ android  │ 未知   │  941 │
-- │ android  │ 男     │ 4361 │
-- │ ios      │ 女     │ 2161 │
-- │ ios      │ 未知   │  433 │
-- └──────────┴────────┴──────┘

-- 6 rows in set. Elapsed: 0.011 sec. Processed 49.84 thousand rows, 299.07 KB (4.70 million rows/s., 28.20 MB/s.)

--单value方法2:
SELECT
    t2.platform AS platform,
    uniqCombined(t1.uid) AS uv
FROM dws.action_001_dis AS t1
INNER JOIN dim.dict_user_dim AS t2 ON toUInt64(t1.uid) = t2.uid
WHERE day = '2021-06-05'
GROUP BY platform

-- Query id: 8906e637-475e-4386-946e-29e1690f07ea

-- ┌─platform─┬───uv─┐
-- │ android  │ 9624 │
-- │ ios      │ 4830 │
-- └──────────┴──────┘

-- 2 rows in set. Elapsed: 0.011 sec. Processed 49.84 thousand rows, 299.07 KB (4.55 million rows/s., 27.32 MB/s.)

--多value方法2:
SELECT
    t2.platform AS platform,
    t2.gender AS gender,
    uniqCombined(t1.uid) AS uv
FROM dws.action_001_dis AS t1
INNER JOIN dim.dict_user_dim AS t2 ON toUInt64(t1.uid) = t2.uid
WHERE day = '2021-06-05'
GROUP BY
    platform,
    gender

-- Query id: 88ef55a6-ddcc-42f8-8ce3-5e3bb639b38a

-- ┌─platform─┬─gender─┬───uv─┐
-- │ ios      │ 男     │ 2236 │
-- │ android  │ 女     │ 4340 │
-- │ android  │ 未知   │  941 │
-- │ android  │ 男     │ 4361 │
-- │ ios      │ 女     │ 2161 │
-- │ ios      │ 未知   │  433 │
-- └──────────┴────────┴──────┘

-- 6 rows in set. Elapsed: 0.015 sec. Processed 49.84 thousand rows, 299.07 KB (3.34 million rows/s., 20.07 MB/s.)

-- 从查询结果来看，dictGet要更快一些，同时在代码可读性上也要更好一些，可以结合场景使用。

-- 业务场景
-- 产品随着分析的不断深入，提了一个新的诉求，希望增加1个维度(通过字典获得)，1个指标(这里只是列举下物化视图的维度和指标的添加过程)。

-- 维度：gender

-- 指标: 曝光时长中位数

-- 创建过程
-- 因为涉及到新增维度和指标，所以需要对原表进行ddl操作。

-- 首先新增维度，新增维度比较麻烦一些，因为不光需要新增字段，还可能需要将新增的字段加到索引里面提高查询效率。

-- 操作sql如下:

--新增维度并添加到索引
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists gender String comment '性别' after item_id,modify order by 
(day,hour,platform,ver,item_id,gender);
alter table dwm.mainpage_stat_mv_local on cluster cluster modify column if exists gender String default '未知' comment '性别' after item_id;
alter table dws.mainpage_stat_mv_dis on cluster cluster add column if not exists gender String comment '性别' after item_id;

--新增指标
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists show_time_median AggregateFunction(medianExact,UInt32) comment '曝光时长中位数';
alter table dws.mainpage_stat_mv_dis on cluster cluster add column if not exists show_time_median AggregateFunction(medianExact,UInt32) comment '曝光时长中位数';

-- 修改物化视图计算逻辑
drop TABLE dwm.mv_main_page_stat_mv_local on cluster cluster;
CREATE MATERIALIZED VIEW dwm.mv_main_page_stat_mv_local on cluster cluster to dwm.mainpage_stat_mv_local (
day Date comment '数据分区-天'
,hour DateTime comment '数据时间-小时(DateTime)'
,platform String comment '平台 android/ios'
,ver String comment '版本'
,item_id UInt32 comment '物品id'
,gender String  comment '性别'
,shown_uv AggregateFunction(uniqCombined,UInt32) comment '曝光人数'
,shown_cnt SimpleAggregateFunction(sum,UInt64) comment '曝光次数'
,click_uv AggregateFunction(uniqCombined,UInt32) comment '点击人数'
,click_cnt SimpleAggregateFunction(sum,UInt64) comment '点击次数'
,show_time_sum  SimpleAggregateFunction(sum,UInt64) comment '总曝光时间/秒'
,show_time_median AggregateFunction(medianExact,UInt32) comment '曝光时长中位数'
)
AS 
 SELECT day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,dictGet('dim.dict_user_dim', 'gender',toUInt64(uid)) as gender
     ,uniqCombinedStateIf(uid,a.show_cnt>0) as shown_uv
     ,sum(a.show_cnt) as show_cnt
     ,uniqCombinedStateIf(uid,a.click_cnt>0) as click_uv
     ,sum(a.click_cnt) as click_cnt
     ,sum(toUInt64(show_time/1000)) as show_time_sum
     ,medianExactState(toUInt32(show_time/1000)) as show_time_median
from ods.action_001_local as a
group by
      day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,gender


-- 物化视图的再进阶
-- 本文在创建log的时候创建了2个log，在上面的case中只用到了一个，接下来的case主要讲一个物化视图的进一步用法。

-- 背景
-- 很多时候，我们的日志上报并不是在一个日志中的，比如上文中创建的action_001和action_002，
-- 一个是主页物品的曝光和点击，一个是点击进行物品详情的其他行为。

-- 这个时候，产品提了一个诉求，希望可以知道曝光到点击，点击到某个更一步的行为的用户转换率。

-- 我们最常规的方法是，使用join去将结果关联，这里只是两个log，那么后续有非常多的log，写起join来就会相当麻烦，甚至会有上千行代码去作逻辑处理，效率上也会差很多。

-- 所以就衍生了接下来主要讲的用法，基于物化视图实现有限join场景。
-- 主要是多个不同日志指标的合并。其实更应该理解为union all max。

-- 可行性分析
-- 物化视图在每批次写入数据之后，后台会按照聚合key进行merge操作，将相同维度的数据的记录聚合在一起，降低数据量，提高查询效率。

-- 如果在这一批数据，没有满足条件的列(if组合器)或者并没有写这一指标(指定字段写)，
-- 那么指标会怎么存，如果下一批数据写入数据，那么这两批数据的这个指标，会怎么样？
-- 答案是存可迭代的空数据(注意这里的不写，存的数据不能理解为null)，
-- 同时可以和其他批数据进行合并，没有数据的行会被忽略。

-- 举个例子:
CREATE TABLE test.mv_union_max
(
    `id` UInt32,
    `m1` AggregateFunction(uniqCombined, UInt32),
    `m2` AggregateFunction(sum, UInt32)
)
ENGINE = AggregatingMergeTree
ORDER BY id

-- Query id: 20dcd6cb-e336-4da8-9033-de42527d2bf0

-- Ok.

-- 0 rows in set. Elapsed: 0.103 sec.

-- # 写入数据(这里需要注意指定字段写)
INSERT INTO test.mv_union_max (id, m1) SELECT
    id,
    uniqCombinedState(uid) AS m1
FROM
(
    SELECT
        a1.1 AS id,
        toUInt32(a1.2) AS uid
    FROM system.one
    ARRAY JOIN [(1, 10001), (2, 10002), (3, 10003), (3, 10001)] AS a1
)
GROUP BY id

-- Query id: f04953f6-3d8a-40a6-bf7e-5b15fe936488

-- Ok.

-- 0 rows in set. Elapsed: 0.003 sec.

SELECT *
FROM test.mv_union_max

-- Query id: af592a63-b17d-4764-9a65-4ab33e122d81

-- ┌─id─┬─m1──┬─m2─┐
-- │  1 │ l��
--                │    │
-- │  2 │ $a6� │    │
-- │  3 │ ��Gwl��
--                  │    │
-- └────┴─────┴────┘

-- 3 rows in set. Elapsed: 0.002 sec.


-- 在写入m1指标后显示有3条记录，其中m2为空数据（这里需要注意的是，m2不是null)，如下：
SELECT isNotNull(m2)
FROM test.mv_union_max

-- Query id: b1ac77df-af77-4f2e-9368-2573a7214c99

-- ┌─isNotNull(m2)─┐
-- │             1 │
-- │             1 │
-- │             1 │
-- └───────────────┘

-- 3 rows in set. Elapsed: 0.002 sec.

SELECT toTypeName(m2)
FROM test.mv_union_max

-- Query id: fcb15349-4a33-4253-bf64-37f5dc7078ea

-- ┌─toTypeName(m2)─────────────────┐
-- │ AggregateFunction(sum, UInt32) │
-- │ AggregateFunction(sum, UInt32) │
-- │ AggregateFunction(sum, UInt32) │
-- └────────────────────────────────┘

-- 3 rows in set. Elapsed: 0.002 sec.


-- 这个时候再写入m2指标，不写入m1指标，那么会发生什么情况。
SELECT *
FROM test.mv_union_max

-- Query id: 7eaa2d42-c50e-4467-9dca-55a0b5eab579

-- ┌─id─┬─m1──┬─m2─┐
-- │  1 │ l��
--                │    │
-- │  2 │ $a6� │    │
-- │  3 │ ��Gwl��
--                  │    │
-- └────┴─────┴────┘
-- ┌─id─┬─m1─┬─m2─┐
-- │  1 │    │ �   │
-- │  2 │    │ '  │
-- │  3 │    │ '  │
-- └────┴────┴────┘

-- 6 rows in set. Elapsed: 0.003 sec.

-- 存了6条记录，分别上两次写入的数据。


-- 在手动触发merge之前先确认下，查询的数据是否是正确的。
SELECT
    id,
    uniqCombinedMerge(m1) AS m1,
    sumMerge(m2) AS m2
FROM test.mv_union_max
GROUP BY id

-- Query id: 3f92106a-1b72-4d86-ab74-59c7ac53c202

-- ┌─id─┬─m1─┬────m2─┐
-- │  3 │  2 │ 10001 │
-- │  2 │  1 │ 10001 │
-- │  1 │  1 │  2003 │
-- └────┴────┴───────┘

-- 3 rows in set. Elapsed: 0.003 sec.

-- 数据完全正确，首先可以确认的是，就算不后台merge，查询数据是完全符合需求的。
OPTIMIZE TABLE test.mv_union_max FINAL

-- Query id: 62465025-da30-4df0-a597-18c0c4eb1b2f

-- Ok.

-- 0 rows in set. Elapsed: 0.001 sec.


SELECT *
FROM test.mv_union_max

-- Query id: f7fb359f-3860-4598-b766-812ac2f65755

-- ┌─id─┬─m1──┬─m2─┐
-- │  1 │ l��
--                │ �   │
-- │  2 │ $a6� │ '  │
-- │  3 │ ��Gwl��
--                  │ '  │
-- └────┴─────┴────┘

-- 3 rows in set. Elapsed: 0.002 sec.

SELECT
    id,
    uniqCombinedMerge(m1) AS m1,
    sumMerge(m2) AS m2
FROM test.mv_union_max
GROUP BY id

-- Query id: 2543a145-e540-43dc-8754-101ebb294b5d

-- ┌─id─┬─m1─┬────m2─┐
-- │  3 │  2 │ 10001 │
-- │  2 │  1 │ 10001 │
-- │  1 │  1 │  2003 │
-- └────┴────┴───────┘

-- 3 rows in set. Elapsed: 0.003 sec.

-- 数据是可以后台merge在一起的。

-- 所以说通过这个case能简单了解到实现原理和可行性。
-- 通过这种方式就可以避免了两个 log 之间的查询关联，
-- 可以通过一个物化视图存储表组织好维度和指标，查询基于一张宽表实现。
-- 众所周知，clickhouse的单表性能非常强，能不join就尽量不join，
-- 这个场景可以减少一部分join的场景(维度补全通过字典，如果维度基数特别大，可以借用flink或者redis字典或者高并发接口补全，这里不做细述)，
-- 便于使用和上层平台的查询规范，
-- 另一方面这样也可以减少存储占用，将相同维度的数据尽可能压在一起。


-- 业务场景 
-- 随着需求的进一步细化，上报了新的action_002，用来分析用户在进入商品页面后的行为。
-- 产品希望可以实现基础指标统计和用户的漏斗分析，(简化一下，对维度没有发生变化)。

-- 结合对需求的了解，对原有的物化视图增加了一些指标。
-- 这里uv，pv，bitmap3个场景都进行了列举，bitmap也可以实现uv，但是效率上慢一些。

-- 新增指标：

-- 指标名 指标解释

-- acta_uv 行为A用户数

-- acta_cnt 行为A记录数

-- actb_uv 行为B用户数

-- actb_cnt 行为B记录数

-- actc_uv 行为C用户数

-- actc_cnt 行为C记录数

-- show_bm 曝光Bitmap 

-- click_bm 点击Bitmap

-- acta_bm 行为A Bitmap

-- actb_bm 行为B Bitmap

-- actc_bm 行为C Bitmap

-- actd_bm 行为D Bitmap


-- action_002 从生成逻辑上假设了一条用户交互路径。

-- a->b->c->d

-- action_001从生成逻辑上假设了一条用户路径。

-- show->click

-- 但是为了降低代码复杂度 click->a并没有强制关联(主要讲方法，这个细节忽略)。

-- 操作过程
-- 需要对原有物化视图存储表新增上述所有指标，同时对物化视图计算表001新增 show_bm、click_bm，
-- 物化视图计算表 002 为新建的计算表，都会写入到最开始建的物化视图存储表中。

-- 操作过程如下(sql有些长):
--物化视图存储表新增指标
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists acta_uv AggregateFunction(uniqCombined,UInt32) comment 'acta_uv';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists acta_cnt SimpleAggregateFunction(sum,UInt64) comment 'acta_cnt';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actb_uv AggregateFunction(uniqCombined,UInt32) comment 'actb_uv';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actb_cnt SimpleAggregateFunction(sum,UInt64) comment 'actb_cnt';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actc_uv AggregateFunction(uniqCombined,UInt32) comment 'actc_uv';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actc_cnt SimpleAggregateFunction(sum,UInt64) comment 'actc_cnt';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists show_bm AggregateFunction(groupBitmap,UInt32) comment 'show_bm';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists click_bm AggregateFunction(groupBitmap,UInt32) comment 'click_bm';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists acta_bm AggregateFunction(groupBitmap,UInt32) comment 'acta_bm';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actb_bm AggregateFunction(groupBitmap,UInt32) comment 'actb_bm';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actc_bm AggregateFunction(groupBitmap,UInt32) comment 'actc_bm';
alter table dwm.mainpage_stat_mv_local on cluster cluster add column if not exists actd_bm AggregateFunction(groupBitmap,UInt32) comment 'actd_bm';
--物化视图计算表重建 因为medianExact 耗时较大，接下来的case里去掉了。
drop TABLE dwm.mv_main_page_stat_mv_local on cluster cluster;
CREATE MATERIALIZED VIEW dwm.mv_main_page_stat_mv_001_local on cluster cluster to dwm.mainpage_stat_mv_local (
day Date comment '数据分区-天'
,hour DateTime comment '数据时间-小时(DateTime)'
,platform String comment '平台 android/ios'
,ver String comment '版本'
,item_id UInt32 comment '物品id'
,gender String  comment '性别'
,shown_uv AggregateFunction(uniqCombined,UInt32) comment '曝光人数'
,shown_cnt SimpleAggregateFunction(sum,UInt64) comment '曝光次数'
,click_uv AggregateFunction(uniqCombined,UInt32) comment '点击人数'
,click_cnt SimpleAggregateFunction(sum,UInt64) comment '点击次数'
,show_time_sum  SimpleAggregateFunction(sum,UInt64) comment '总曝光时间/秒'
,show_bm AggregateFunction(groupBitmap,UInt32) comment 'show_bm'
,click_bm AggregateFunction(groupBitmap,UInt32) comment 'click_bm'
)
AS 
 SELECT day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,dictGet('dim.dict_user_dim', 'gender',toUInt64(uid)) as gender
     ,uniqCombinedStateIf(uid,a.show_cnt>0) as shown_uv
     ,sum(a.show_cnt) as show_cnt
     ,uniqCombinedStateIf(uid,a.click_cnt>0) as click_uv
     ,sum(a.click_cnt) as click_cnt
     ,sum(toUInt64(show_time/1000)) as show_time_sum
     ,groupBitmapStateIf(uid,a.show_cnt>0) as show_bm
     ,groupBitmapStateIf(uid,a.click_cnt>0) as click_bm
from ods.action_001_local as a
group by
      day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,gender

drop table dwm.mv_main_page_stat_mv_002_local on cluster cluster;
CREATE MATERIALIZED VIEW dwm.mv_main_page_stat_mv_002_local on cluster cluster to dwm.mainpage_stat_mv_local (
day Date comment '数据分区-天'
,hour DateTime comment '数据时间-小时(DateTime)'
,platform String comment '平台 android/ios'
,ver String comment '版本'
,item_id UInt32 comment '物品id'
,gender String  comment '性别'
,acta_uv AggregateFunction(uniqCombined,UInt32) comment 'acta_uv'
,acta_cnt SimpleAggregateFunction(sum,UInt64) comment 'acta_cnt'
,actb_uv AggregateFunction(uniqCombined,UInt32) comment 'actb_uv'
,actb_cnt SimpleAggregateFunction(sum,UInt64) comment 'actb_cnt'
,actc_uv AggregateFunction(uniqCombined,UInt32) comment 'actc_uv'
,actc_cnt SimpleAggregateFunction(sum,UInt64) comment 'actc_cnt'
,acta_bm AggregateFunction(groupBitmap,UInt32) comment 'acta_bm'
,actb_bm AggregateFunction(groupBitmap,UInt32) comment 'actb_bm'
,actc_bm AggregateFunction(groupBitmap,UInt32) comment 'actc_bm'
,actd_bm AggregateFunction(groupBitmap,UInt32) comment 'actd_bm'
)
AS 
 SELECT day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,dictGet('dim.dict_user_dim', 'gender',toUInt64(uid)) as gender
     ,uniqCombinedStateIf(uid,a.action_a_cnt>0) as acta_uv
     ,sum(a.action_a_cnt) as acta_cnt
     ,uniqCombinedStateIf(uid,a.action_b_cnt>0) as actb_uv
     ,sum(a.action_b_cnt) as actb_cnt
     ,uniqCombinedStateIf(uid,a.action_c_cnt>0) as actc_uv
     ,sum(a.action_c_cnt) as actc_cnt
     ,groupBitmapStateIf(uid,a.action_a_cnt>0) as acta_bm
     ,groupBitmapStateIf(uid,a.action_b_cnt>0) as actb_bm
     ,groupBitmapStateIf(uid,a.action_c_cnt>0) as actc_bm
     ,groupBitmapStateIf(uid,a.action_d_sum>0) as actd_bm
from ods.action_002_local as a
group by
      day
     ,hour
     ,platform
     ,ver
     ,item_id
     ,gender

-- 操作完成之后就得到了一个物化视图的指标宽表(假设它很宽)。就可以用它来解决一些查询场景。

-- 查询场景1：多个日志指标的合并
SELECT
    day,
    gender,
    uniqCombinedMerge(shown_uv) AS shown_uv,
    uniqCombinedMerge(click_uv) AS click_uv,
    uniqCombinedMerge(acta_uv) AS acta_uv,
    uniqCombinedMerge(actb_uv) AS actb_uv,
    uniqCombinedMerge(actc_uv) AS actc_uv
FROM dws.mainpage_stat_mv_dis
WHERE day = '2021-06-06'
GROUP BY
    day,
    gender

-- Query id: 5d4eed47-78f1-4c22-a2cd-66a6a4db14ab

-- ┌────────day─┬─gender─┬─shown_uv─┬─click_uv─┬─acta_uv─┬─actb_uv─┬─actc_uv─┐
-- │ 2021-06-06 │ 男     │     6845 │     6157 │    6845 │    5824 │    4826 │
-- │ 2021-06-06 │ 未知   │     1421 │     1277 │    1421 │    1232 │    1029 │
-- │ 2021-06-06 │ 女     │     6734 │     6058 │    6733 │    5776 │    4826 │
-- └────────────┴────────┴──────────┴──────────┴─────────┴─────────┴─────────┘

-- 3 rows in set. Elapsed: 0.025 sec. Processed 48.70 thousand rows, 24.23 MB (1.98 million rows/s., 983.52 MB/s.)

--如果使用join的话 这里因为没有分开创建物化视图，只列举语法，所以也不对性能进行对比。
SELECT
    t1.day,
    t1.gender,
    shown_uv,
    click_uv,
    acta_uv,
    actb_uv,
    actc_uv
FROM
(
    SELECT
        day,
        dictGet('dim.dict_user_dim', 'gender', toUInt64(uid)) AS gender,
        uniqCombinedIf(uid, a.show_cnt > 0) AS shown_uv,
        uniqCombinedIf(uid, a.click_cnt > 0) AS click_uv
    FROM dws.action_001_dis AS a
    WHERE day = '2021-06-06'
    GROUP BY
        day,
        gender
) AS t1
LEFT JOIN
(
    SELECT
        day,
        dictGet('dim.dict_user_dim', 'gender', toUInt64(uid)) AS gender,
        uniqCombinedIf(uid, a.action_a_cnt > 0) AS acta_uv,
        uniqCombinedIf(uid, a.action_b_cnt > 0) AS actb_uv,
        uniqCombinedIf(uid, a.action_c_cnt > 0) AS actc_uv
    FROM dws.action_002_dis AS a
    GROUP BY
        day,
        gender
) AS t2 USING (day, gender)

-- Query id: 2ab32451-e373-4757-9e25-f089aef1e9f4

-- ┌────────day─┬─gender─┬─shown_uv─┬─click_uv─┬─acta_uv─┬─actb_uv─┬─actc_uv─┐
-- │ 2021-06-06 │ 男     │     6845 │     6209 │    6845 │    5824 │    4826 │
-- │ 2021-06-06 │ 未知   │     1421 │     1283 │    1421 │    1232 │    1029 │
-- │ 2021-06-06 │ 女     │     6734 │     6096 │    6733 │    5776 │    4826 │
-- └────────────┴────────┴──────────┴──────────┴─────────┴─────────┴─────────┘

-- 3 rows in set. Elapsed: 0.032 sec. Processed 360.36 thousand rows, 5.85 MB (11.11 million rows/s., 180.47 MB/s.)


-- 查询场景2：基于bitmap的用户行为分析。
SELECT
    day,
    gender,
    bitmapCardinality(groupBitmapMergeState(show_bm)) AS shown_uv,
    bitmapAndCardinality(groupBitmapMergeState(show_bm), groupBitmapMergeState(click_bm)) AS show_click_uv,
    bitmapAndCardinality(groupBitmapMergeState(show_bm), bitmapAnd(groupBitmapMergeState(click_bm), groupBitmapMergeState(acta_bm))) AS show_click_a_uv,
    bitmapAndCardinality(groupBitmapMergeState(show_bm), bitmapAnd(bitmapAnd(groupBitmapMergeState(click_bm), groupBitmapMergeState(acta_bm)), groupBitmapMergeState(actb_bm))) AS show_click_ab_uv,
    bitmapAndCardinality(groupBitmapMergeState(show_bm), bitmapAnd(bitmapAnd(bitmapAnd(groupBitmapMergeState(click_bm), groupBitmapMergeState(acta_bm)), groupBitmapMergeState(actb_bm)), groupBitmapMergeState(actc_bm))) AS show_click_abc_uv,
    bitmapAndCardinality(groupBitmapMergeState(show_bm), bitmapAnd(bitmapAnd(bitmapAnd(bitmapAnd(groupBitmapMergeState(click_bm), groupBitmapMergeState(acta_bm)), groupBitmapMergeState(actb_bm)), groupBitmapMergeState(actc_bm)), groupBitmapMergeState(actd_bm))) AS show_click_abcd_uv
FROM dws.mainpage_stat_mv_dis
WHERE day = '2021-06-06'
GROUP BY
    day,
    gender

-- Query id: b79de70f-6091-4d0a-9a33-12af8f210931

-- ┌────────day─┬─gender─┬─shown_uv─┬─show_click_uv─┬─show_click_a_uv─┬─show_click_ab_uv─┬─show_click_abc_uv─┬─show_click_abcd_uv─┐
-- │ 2021-06-06 │ 男     │     6845 │          6157 │            6157 │             5244 │              4341 │
--   4341 │
-- │ 2021-06-06 │ 未知   │     1421 │          1277 │            1277 │             1113 │               928 │
--    928 │
-- │ 2021-06-06 │ 女     │     6734 │          6058 │            6057 │             5211 │              4367 │
--   4367 │
-- └────────────┴────────┴──────────┴───────────────┴─────────────────┴──────────────────┴───────────────────┴────────────────────┘

-- 3 rows in set. Elapsed: 0.052 sec. Processed 48.70 thousand rows, 54.89 MB (944.42 thousand rows/s., 1.06 GB/s.)

-- 还有一些其他用法篇幅有限不展开了，大家自由探索。

-- 因为bitmap函数只支持同时输入两个bitmap，所以层级越深需要不断进行合并。
-- 不过这个也整合到一个指标，会对基于superset这样的上层平台，配置指标时方便许多，
-- 不用通过join实现，也不需要非常多的子查询了，从查询性能上，存储上，都是一个很友好的方案。

-- 同时不管是多log分开写多个指标，也可以进行合并写在一个指标，都可以很方便的进行指标整合。

-- 总结
-- 物化视图是clickhouse一个非常重要的功能，同时也做了很多优化和函数扩展，
-- 虽然在某些情况可能会带来一定的风险（比如增加错误字段导致写入失败等问题），
-- 但是也是可以在使用中留意避免的，不能因噎废食。

-- 本文主要讲解了
-- 1. 物化视图的创建、新增维度和指标，聚合函数的使用和一些注意事项；
-- 2. 物化视图结合字典的使用；
-- 3. 通过物化视图组合指标宽表。