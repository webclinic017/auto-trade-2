-- chatgpt
-- clickhouse 全局字典 tick 数据, 并合成 1 分钟 k 线

-- 使用 clickhouse 全局字典来存储 tick 数据，可以先创建一个全局字典的表，并使用它存储 tick 数据，例如：
CREATE TABLE tick_data (
    date Date,
    time Time,
    code String,
    price Float32,
    volume Float32
) ENGINE = MergeTree(date, (time, code), 8192);

CREATE DICTIONARY dict_code (
    code String,
    id UInt32
) PRIMARY KEY code
    SOURCE(CLICKHOUSE(HOST '127.0.0.1' PORT 9000 USER 'default' PASSWORD '' DB 'default' TABLE 'dict_code'))
    LIFETIME(MINUTE, 1);

INSERT INTO dict_code (code) VALUES ('AAPL'), ('MSFT'), ('GOOG'), ('AMZN'), ('FB');

ALTER TABLE tick_data
    UPDATE code
    SET code = dictGetString('dict_code', 'code', code);


-- 然后，使用物化视图将 tick 数据按照一分钟的频率进行聚合，合成 1 分钟 k 线，例如：
CREATE MATERIALIZED VIEW min1_data TO min1_data AS
SELECT
    date,
    floor(toMinute(time) / 1) * 1 AS minute,
    code,
    max(price) AS high,
    min(price) AS low,
    sum(volume) AS volume,
    avg(price) AS close
FROM tick_data
GROUP BY date, code, minute
ORDER BY date, code, minute;

--这样，就可以在 min1_data 表中读取到合成的 1 分钟 k 线数据。



