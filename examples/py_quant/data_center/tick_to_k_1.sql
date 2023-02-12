-- chatgpt
-- clickhouse 全局字典 tick 数据

-- ClickHouse 的全局字典是一种存储数据的特殊结构，它可以高效地存储枚举类型数据，并可以在整个数据库中共享。

-- 如果你想使用 ClickHouse 的全局字典存储和读取 tick 数据，你需要使用 ClickHouse 字典表。这些字典表包含预先定义的数据类型，每个数据类型都有一个特定的编码。

-- 下面是使用字典表存储 tick 数据的示例代码：

CREATE TABLE ticks (
  symbol String,
  price Float64,
  volume UInt64
) ENGINE = MergeTree(date, (symbol, price, volume), 8192);

CREATE DICTIONARY dictionary_symbol (
  symbol String,
  id UInt64
) PRIMARY KEY symbol
  SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' PASSWORD '' DBNAME 'test' TABLE 'symbol_dictionary'))
  LIFETIME(MIN 1 MONTH 1);

ALTER TABLE ticks ADD COLUMN symbol_id UInt64;

CREATE MATERIALIZED VIEW ticks_symbol_id TO ticks AS
  SELECT symbol_id, price, volume
  FROM (
    SELECT symbol_id, price, volume, symbol
    FROM ticks
    JOIN dictionary_symbol
    USING symbol
  );

INSERT INTO ticks (symbol, price, volume)
VALUES ('AAPL', 100, 1000), ('MSFT', 90, 500), ('GOOG', 120, 200), ('AAPL', 105, 800), ('MSFT', 95, 400);

SELECT symbol_id, avg(price) avg_price, sum(volume) sum_volume
FROM ticks_symbol_id
GROUP BY symbol_id
