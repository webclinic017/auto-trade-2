import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait

import akshare as ak
import pandas as pd

import stock_constant as sc

"""
python 量化提速
"""

async def _task_io2():
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, ak.stock_zh_a_hist, '000001', 'daily', '20150101', '20221202', 'qfq')
    response = await future
    # print(f"请求回来了 {response.empty}")


async def _read_csw():
    return pd.read_csv(sc.config_path)


def _task_io():
    pd.read_csv(sc.config_path)


def _task_cpu():
    return sum(i * i for i in range(10 ** 5))


async def async_thread_pool(is_io, total, cpu_count):
    executor = ThreadPoolExecutor(cpu_count)
    loop = asyncio.get_event_loop()
    t1 = time.time()
    tt = [loop.run_in_executor(executor, _task_io if is_io else _task_cpu) for _ in range(total)]
    await asyncio.wait(tt)
    print(f'async_thread_pool  耗时：{time.time() - t1} 任务量：{total}  {"io 任务" if is_io else "cpu 任务"}')


async def async_process_pool(is_io, total, cpu_count):
    executor = ProcessPoolExecutor(cpu_count)
    loop = asyncio.get_event_loop()
    t1 = time.time()
    tt = [loop.run_in_executor(executor, _task_io if is_io else _task_cpu) for _ in range(total)]
    await asyncio.wait(tt)
    print(f'async_process_pool 耗时：{time.time() - t1} 任务量：{total}  {"io 任务" if is_io else "cpu 任务"}')


def thread_pool(is_io, total, cpu_count):
    executor = ThreadPoolExecutor(cpu_count)
    t1 = time.time()
    futures = [executor.submit(_task_io if is_io else _task_cpu) for _ in range(total)]
    wait(futures)
    print(f'thread_pool        耗时：{time.time() - t1} 任务量：{total}  {"io 任务" if is_io else "cpu 任务"}')


def process_pool(is_io, total, cpu_count):
    executor = ProcessPoolExecutor(cpu_count)
    t1 = time.time()
    futures = [executor.submit(_task_io if is_io else _task_cpu) for _ in range(total)]
    wait(futures)
    print(f'process_pool       耗时：{time.time() - t1} 任务量：{total}  {"io 任务" if is_io else "cpu 任务"}')


def main(total, cpu_count):
    print(f'cpu：{cpu_count} 个')
    asyncio.run(async_thread_pool(True, total, cpu_count))
    asyncio.run(async_process_pool(True, total, cpu_count))
    thread_pool(True, total, cpu_count)
    process_pool(True, total, cpu_count)

    print('--------------------------------------')

    asyncio.run(async_thread_pool(False, total, cpu_count))
    asyncio.run(async_process_pool(False, total, cpu_count))
    thread_pool(False, total, cpu_count)
    process_pool(False, total, cpu_count)
    print('=========================================')


def coroutine(total):
    t1 = time.time()
    tasks = [asyncio.ensure_future(_task_io2()) for _ in range(total)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f'coroutine       耗时：{time.time() - t1} 任务量：{total}')


if __name__ == '__main__':
    total = 1000
    cpu_count = 1
    main(total, cpu_count)
    total = 10000
    main(total, cpu_count)

    total = 1000
    cpu_count = int(os.cpu_count() / 2)
    main(total, cpu_count)
    total = 10000
    main(total, cpu_count)

    cpu_count = int(os.cpu_count())
    total = 1000
    main(total, cpu_count)
    total = 10000
    main(total, cpu_count)

    # 修改成异步来执行
    cpu_count = int(os.cpu_count())
    start_time = time.time()
    pool = ProcessPoolExecutor()
    total = 5000
    futures = []
    for part in range(cpu_count):
        future = pool.submit(coroutine, int(total / cpu_count))
        futures.append(future)
    pool.shutdown(wait=True)
    print(f'5k 次股票请求耗时: {time.time() - start_time}')