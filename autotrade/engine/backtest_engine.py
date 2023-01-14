#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time
from time import time as ttime
from typing import Union
from collections import defaultdict
from typing import Any, Callable
import multiprocessing
import random
from itertools import product
from functools import lru_cache
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from deap import creator, base, tools, algorithms

import source.common.sqglobal as sqglobal

from ..common.constant import (
    Direction, Offset, Exchange,
    Interval, Status, EngineType,
    BacktestingMode, STOPORDER_PREFIX, StopOrderStatus
)
from ..common.datastruct import (
    OrderData, TradeData, BacktestTradeData,
    BarData, TickData, StopOrder, ContractData
)
from ..common.utility import extract_full_symbol
from ..strategy.strategy_base import StrategyBase
from ..data import database_manager
from ..trade.portfolio_manager import PositionHolding


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

CtaTemplate = StrategyBase


class OptimizationSetting:
    """
    Setting for runnning optimization.
    """

    def __init__(self):
        """"""
        self.params = {}
        self.target_name = ""

    def add_parameter(
        self, name: str, start: float, end: float = None, step: float = None
    ):
        """"""
        if not end and not step:
            self.params[name] = [start]
            return

        if start >= end:
            print("参数优化起始点必须小于终止点")
            return

        if step <= 0:
            print("参数优化步进必须大于0")
            return

        value = start
        value_list = []

        while value <= end:
            value_list.append(value)
            value += step

        self.params[name] = value_list

    def set_target(self, target_name: str):
        """"""
        self.target_name = target_name

    def generate_setting(self):
        """"""
        keys = self.params.keys()
        values = self.params.values()
        products = list(product(*values))

        settings = []
        for p in products:
            setting = dict(zip(keys, p))
            settings.append(setting)

        return settings

    def generate_setting_ga(self):
        """"""
        settings_ga = []
        settings = self.generate_setting()
        for d in settings:
            param = [tuple(i) for i in d.items()]
            settings_ga.append(param)
        return settings_ga


class BacktestingEngine:
    """"""

    engine_type = EngineType.BACKTESTING
    gateway_name = "BACKTESTING"

    def __init__(self):
        """"""
        self.id = 0
        self.full_symbol = ""
        self.symbol = ""
        self.exchange = None
        self.start = None
        self.end = None
        self.rate = 0
        self.slippage = 0
        self.size = 1
        self.pricetick = 0
        self.capital = 1_000_000
        self.mode = BacktestingMode.BAR

        self.contract = None
        self.holding = None
        self.strategy_class = None
        self.strategy = None
        self.tick: TickData
        self.bar: BarData
        self.datetime = None

        self.interval = None
        self.days = 0
        self.callback = None
        self.historybar_callback = None  # used in tick mode called by strategy load_bar
        self.historytick_callback = None  # used in tick mode called by strategy load_tick
        self.history_data = []
        self.history_data_startix = 0
        self.history_data_endix = 0
        self.history_bar = []  # used in tick mode called by strategy load_bar
        self.history_bar_startix = 0
        self.history_bar_endix = 0
        self.history_tick = []  # used in tick mode called by strategy load_tick
        self.history_tick_startix = 0
        self.history_tick_endix = 0
        self.order_count = 0

        self.stop_order_count = 0
        self.stop_orders = {}
        self.active_stop_orders = {}

        self.limit_order_count = 0
        self.limit_orders = {}
        self.active_limit_orders = {}
        self.strategy_orderid_map = defaultdict(set)

        self.trade_count = 0
        self.trades = {}

        self.logs = []

        self.daily_results = {}
        self.daily_df = None

    def clear_data(self):
        """
        Clear all data of last backtesting.
        """
        self.strategy = None
        self.tick = None
        self.bar = None
        self.datetime = None
        self.holding = None
        self.contract = None

        self.stop_order_count = 0
        self.stop_orders.clear()
        self.active_stop_orders.clear()

        self.limit_order_count = 0
        self.limit_orders.clear()
        self.active_limit_orders.clear()
        self.strategy_orderid_map.clear()

        self.trade_count = 0
        self.trades.clear()

        self.logs.clear()
        self.daily_results.clear()

    def set_parameters(
        self,
        full_symbol: str,
        interval: str,
        start: datetime,
        rate: float,
        slippage: float,
        size: float,
        pricetick: float,
        capital: int = 0,
        end: datetime = None,
        mode: BacktestingMode = BacktestingMode.BAR,
    ):
        """"""       
        self.mode = mode
        self.full_symbol = full_symbol
        if interval == 'tick':
            self.interval = Interval.MINUTE
            self.mode = BacktestingMode.TICK
        else:
            self.interval = Interval(interval)
        self.rate = rate
        self.slippage = slippage
        self.size = size
        self.pricetick = pricetick
        if type(start) == date:
            self.start = datetime(start.year,start.month,start.day)
        else:
            self.start = start

        self.symbol, self.exchange = extract_full_symbol(self.full_symbol)

        if capital:
            self.capital = capital

        if end:
            if type(end) == date:
                self.end = datetime(end.year,end.month,end.day)
            else:
                self.end = end
        else:
            self.end = datetime.now()

        contract = ContractData(
            full_symbol=self.full_symbol,
            size=self.size,
            exchange=self.exchange,
            pricetick=self.pricetick
        )
        self.contract = contract
        self.holding = PositionHolding("PAPER", contract)

    def add_strategy(self, strategy_class: type, setting: dict):
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, self.full_symbol, setting
        )
        # redirect strategy write_log output
        self.strategy.write_log = self.output

    def load_data(self, datasource: str = "DataBase"):
        """"""
        self.output("开始加载历史数据")

        if self.mode == BacktestingMode.BAR:
            if datasource == "DataBase":
                self.history_data = load_bar_data(
                    self.symbol,
                    self.exchange,
                    self.interval,
                    self.start,
                    self.end
                )
                self.history_data_startix = 0
                self.history_data_endix = len(self.history_data)
            elif datasource == "Memory":
                startix = 0
                endix = 0
                totalbarlist = sqglobal.history_bar[self.full_symbol]
                if not totalbarlist:
                    self.output('数据为空，请先读入')
                    return
                totalbars = len(totalbarlist)
                for i in range(totalbars):
                    if totalbarlist[i].datetime < self.start:
                        continue
                    startix = i
                    break
                for i in reversed(range(totalbars)):
                    if totalbarlist[i].datetime > self.end:
                        continue
                    endix = i
                    break
                endix = min(endix + 1, totalbars)
                self.history_data_startix = startix
                self.history_data_endix = endix
                self.history_data = totalbarlist
        else:
            if datasource == "DataBase":
                self.history_data = load_tick_data(
                    self.symbol,
                    self.exchange,
                    self.start,
                    self.end
                )
                self.history_data_startix = 0
                self.history_data_endix = len(self.history_data)
            elif datasource == "Memory":
                startix = 0
                endix = 0
                totalticklist = sqglobal.history_tick[self.full_symbol]
                if not totalticklist:
                    self.output('数据为空，请先读入')
                    return
                totalticks = len(totalticklist)
                for i in range(totalticks):
                    if totalticklist[i].datetime < self.start:
                        continue
                    startix = i
                    break
                for i in reversed(range(totalticks)):
                    if totalticklist[i].datetime > self.end:
                        continue
                    endix = i
                    break
                endix = min(endix + 1, totalticks)
                self.history_data = totalticklist
                self.history_data_startix = startix
                self.history_data_endix = endix

        self.output(
            f"历史数据加载完成，数据量：{self.history_data_endix - self.history_data_startix}")

    def run_backtesting(self):
        """"""
        if not self.history_data or self.history_data_startix == self.history_data_endix:
            self.output('回测数据为空，直接结束回测')
            return

        if self.mode == BacktestingMode.BAR:
            func = self.new_bar
        else:
            func = self.new_tick

        self.strategy.on_init()

        # Use the first [days] of history data for initializing strategy
        # day_count = 0
        # ix = 0

        # using load_bar/tick for  initializing strategy
        if self.historybar_callback:
            for data in self.history_bar[self.history_bar_startix:self.history_bar_endix]:
                self.historybar_callback(data)
        if self.historytick_callback:
            for data in self.history_tick[self.history_tick_startix:self.history_tick_endix]:
                self.historytick_callback(data)

        # for ix, data in enumerate(self.history_data):
        #     if self.datetime and data.datetime.day != self.datetime.day:
        #         day_count += 1
        #         if day_count >= self.days:
        #             break

        #     self.datetime = data.datetime
        #     self.callback(data)

        self.strategy.inited = True
        self.output("策略初始化完成")

        self.strategy.on_start()
        self.strategy.trading = True
        self.output("开始回放历史数据")

        # Use the rest of history data for running backtesting
        for data in self.history_data[self.history_data_startix:self.history_data_endix]:
            func(data)

        self.output("历史数据回放结束")

    def calculate_result(self):
        """"""
        self.output("开始计算逐日盯市盈亏")

        if not self.trades:
            self.output("成交记录为空，无法计算")
            return

        # Add trade data into daily reuslt.
        for trade in self.trades.values():
            d = trade.datetime.date()
            t = trade.datetime.time()
            if t > time(hour=17, minute=0):
                if d.weekday() == 4:
                    d = d + timedelta(days=3)
                else:
                    d = d + timedelta(days=1)
            elif t < time(hour=8, minute=0):  # 周六凌晨算周一
                if d.weekday() == 5:
                    d = d + timedelta(days=2)
            daily_result = self.daily_results[d]
            daily_result.add_trade(trade)

        # Calculate daily result by iteration.
        pre_close = 0
        start_pos = 0

        for daily_result in self.daily_results.values():
            daily_result.calculate_pnl(
                pre_close, start_pos, self.size, self.rate, self.slippage
            )

            pre_close = daily_result.close_price
            start_pos = daily_result.end_pos

        # Generate dataframe
        results = defaultdict(list)

        for daily_result in self.daily_results.values():
            for key, value in daily_result.__dict__.items():
                results[key].append(value)

        self.daily_df = DataFrame.from_dict(results).set_index("date")

        self.output("逐日盯市盈亏计算完成")
        return self.daily_df

    def calculate_statistics(self, df: DataFrame = None, output=True):
        """"""
        self.output("开始计算策略统计指标")

        if not df:
            df = self.daily_df

        if df is None:
            # Set all statistics to 0 if no trade.
            start_date = ""
            end_date = ""
            total_days = 0
            profit_days = 0
            loss_days = 0
            end_balance = 0
            max_drawdown = 0
            max_ddpercent = 0
            total_net_pnl = 0
            daily_net_pnl = 0
            total_commission = 0
            daily_commission = 0
            total_slippage = 0
            daily_slippage = 0
            total_turnover = 0
            daily_turnover = 0
            total_trade_count = 0
            daily_trade_count = 0
            total_return = 0
            annual_return = 0
            daily_return = 0
            return_std = 0
            sharpe_ratio = 0
            return_drawdown_ratio = 0
            winratio = 0
            winloss = 0
        else:
            # Calculate balance related time series data
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(
                df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = (
                df["balance"].rolling(
                    min_periods=1, window=len(df), center=False).max()
            )
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Calculate statistics value
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                sharpe_ratio = daily_return / return_std * np.sqrt(240)
            else:
                sharpe_ratio = 0
            if max_ddpercent:
                return_drawdown_ratio = -total_return / max_ddpercent
            else:
                return_drawdown_ratio = 0

            wincount = 0
            winmoney = 0
            losscount = 0
            lossmoney = 0

            for trade in self.trades.values():
                if trade.offset == Offset.CLOSE:
                    if (trade.long_pnl + trade.short_pnl) > 0:
                        wincount += 1
                        winmoney += trade.long_pnl + trade.short_pnl
                    elif (trade.long_pnl + trade.short_pnl) < 0:
                        losscount += 1
                        lossmoney += abs(trade.long_pnl + trade.short_pnl)
            if (wincount + losscount):
                winratio = wincount / (wincount + losscount)
            else:
                winratio = 0.0
            if wincount and losscount and lossmoney:
                winloss = (winmoney / wincount) / (lossmoney / losscount)
            else:
                winloss = 0.0
        # Output
        if output:
            self.output("-" * 30)
            self.output(f"首个交易日：\t{start_date}")
            self.output(f"最后交易日：\t{end_date}")

            self.output(f"总交易日：\t{total_days}")
            self.output(f"盈利交易日：\t{profit_days}")
            self.output(f"亏损交易日：\t{loss_days}")

            self.output(f"起始资金：\t{self.capital:,.2f}")
            self.output(f"结束资金：\t{end_balance:,.2f}")

            self.output(f"总收益率：\t{total_return:,.2f}%")
            self.output(f"年化收益：\t{annual_return:,.2f}%")
            self.output(f"最大回撤: \t{max_drawdown:,.2f}")
            self.output(f"百分比最大回撤: {max_ddpercent:,.2f}%")

            self.output(f"总盈亏：\t{total_net_pnl:,.2f}")
            self.output(f"总手续费：\t{total_commission:,.2f}")
            self.output(f"总滑点：\t{total_slippage:,.2f}")
            self.output(f"总成交金额：\t{total_turnover:,.2f}")
            self.output(f"总成交笔数：\t{total_trade_count}")

            self.output(f"日均盈亏：\t{daily_net_pnl:,.2f}")
            self.output(f"日均手续费：\t{daily_commission:,.2f}")
            self.output(f"日均滑点：\t{daily_slippage:,.2f}")
            self.output(f"日均成交金额：\t{daily_turnover:,.2f}")
            self.output(f"日均成交笔数：\t{daily_trade_count}")

            self.output(f"日均收益率：\t{daily_return:,.2f}%")
            self.output(f"收益标准差：\t{return_std:,.2f}%")
            self.output(f"Sharpe Ratio：\t{sharpe_ratio:,.2f}")
            self.output(f"收益回撤比：\t{return_drawdown_ratio:,.2f}")

        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "profit_days": profit_days,
            "loss_days": loss_days,
            "capital": self.capital,
            "end_balance": end_balance,
            "max_drawdown": max_drawdown,
            "max_ddpercent": max_ddpercent,
            "total_net_pnl": total_net_pnl,
            "daily_net_pnl": daily_net_pnl,
            "total_commission": total_commission,
            "daily_commission": daily_commission,
            "total_slippage": total_slippage,
            "daily_slippage": daily_slippage,
            "total_turnover": total_turnover,
            "daily_turnover": daily_turnover,
            "total_trade_count": total_trade_count,
            "daily_trade_count": daily_trade_count,
            "total_return": total_return,
            "annual_return": annual_return,
            "daily_return": daily_return,
            "return_std": return_std,
            "sharpe_ratio": sharpe_ratio,
            "return_drawdown_ratio": return_drawdown_ratio,
            "win_ratio": winratio,
            "win_loss": winloss
        }

        return statistics

    def show_chart(self, df: DataFrame = None):
        """"""
        if not df:
            df = self.daily_df

        if df is None:
            return

        plt.figure(figsize=(10, 16))

        balance_plot = plt.subplot(4, 1, 1)
        balance_plot.set_title("Balance")
        df["balance"].plot(legend=True)

        drawdown_plot = plt.subplot(4, 1, 2)
        drawdown_plot.set_title("Drawdown")
        drawdown_plot.fill_between(range(len(df)), df["drawdown"].values)

        pnl_plot = plt.subplot(4, 1, 3)
        pnl_plot.set_title("Daily Pnl")
        df["net_pnl"].plot(kind="bar", legend=False, grid=False, xticks=[])

        distribution_plot = plt.subplot(4, 1, 4)
        distribution_plot.set_title("Daily Pnl Distribution")
        df["net_pnl"].hist(bins=50)

        plt.show()

    def run_optimization(self, optimization_setting: OptimizationSetting, output=True, datasource: str = 'DataBase'):
        """"""
        # Get optimization setting and target
        settings = optimization_setting.generate_setting()
        target_name = optimization_setting.target_name

        if not settings:
            self.output("优化参数组合为空，请检查")
            return

        if not target_name:
            self.output("优化目标未设置，请检查")
            return

        # Use multiprocessing pool for running backtesting with different setting
        pool = multiprocessing.Pool(multiprocessing.cpu_count())

        results = []
        for setting in settings:
            result = (pool.apply_async(optimize, (
                target_name,
                self.strategy_class,
                setting,
                self.full_symbol,
                self.interval,
                self.start,
                self.rate,
                self.slippage,
                self.size,
                self.pricetick,
                self.capital,
                self.end,
                self.mode,
                datasource
            )))
            results.append(result)

        pool.close()
        pool.join()

        # Sort results and output
        result_values = [result.get() for result in results]
        result_values.sort(reverse=True, key=lambda result: result[1])

        if output:
            for value in result_values:
                msg = f"参数：{value[0]}, 目标：{value[1]}"
                self.output(msg)

        return result_values

    def run_ga_optimization(self, optimization_setting: OptimizationSetting, population_size=100, ngen_size=30, output=True, datasource: str = 'DataBase'):
        """"""
        # Get optimization setting and target
        settings = optimization_setting.generate_setting_ga()
        target_name = optimization_setting.target_name

        if not settings:
            self.output("优化参数组合为空，请检查")
            return

        if not target_name:
            self.output("优化目标未设置，请检查")
            return

        # Define parameter generation function
        def generate_parameter():
            """"""
            return random.choice(settings)

        def mutate_individual(individual, indpb):
            """"""
            size = len(individual)
            paramlist = generate_parameter()
            for i in range(size):
                if random.random() < indpb:
                    individual[i] = paramlist[i]
            return individual,

        # Create ga object function
        global ga_target_name
        global ga_strategy_class
        global ga_setting
        global ga_full_symbol
        global ga_interval
        global ga_start
        global ga_rate
        global ga_slippage
        global ga_size
        global ga_pricetick
        global ga_capital
        global ga_end
        global ga_mode

        ga_target_name = target_name
        ga_strategy_class = self.strategy_class
        ga_setting = settings[0]
        ga_full_symbol = self.full_symbol
        ga_interval = self.interval
        ga_start = self.start
        ga_rate = self.rate
        ga_slippage = self.slippage
        ga_size = self.size
        ga_pricetick = self.pricetick
        ga_capital = self.capital
        ga_end = self.end
        ga_mode = self.mode

        # Set up genetic algorithem
        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initIterate,
                         creator.Individual, generate_parameter)
        toolbox.register("population", tools.initRepeat,
                         list, toolbox.individual)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mutate_individual, indpb=1)
        toolbox.register("evaluate", ga_optimize)
        toolbox.register("select", tools.selNSGA2)

        total_size = len(settings)
        # number of individuals in each generation
        pop_size = population_size
        # number of children to produce at each generation
        lambda_ = pop_size
        # number of individuals to select for the next generation
        mu = int(pop_size * 0.8)

        cxpb = 0.95         # probability that an offspring is produced by crossover
        mutpb = 1 - cxpb    # probability that an offspring is produced by mutation
        ngen = ngen_size    # number of generation

        pop = toolbox.population(pop_size)
        hof = tools.ParetoFront()               # end result of pareto front

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        np.set_printoptions(suppress=True)
        stats.register("mean", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        # Multiprocessing is not supported yet.
        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # toolbox.register("map", pool.map)

        # Run ga optimization
        self.output(f"参数优化空间：{total_size}")
        self.output(f"每代族群总数：{pop_size}")
        self.output(f"优良筛选个数：{mu}")
        self.output(f"迭代次数：{ngen}")
        self.output(f"交叉概率：{cxpb:.0%}")
        self.output(f"突变概率：{mutpb:.0%}")

        start = ttime()

        algorithms.eaMuPlusLambda(
            pop,
            toolbox,
            mu,
            lambda_,
            cxpb,
            mutpb,
            ngen,
            stats,
            halloffame=hof
        )

        end = ttime()
        cost = int((end - start))

        self.output(f"遗传算法优化完成，耗时{cost}秒")

        # Return result list
        results = []

        for parameter_values in hof:
            setting = dict(parameter_values)
            target_value = ga_optimize(parameter_values, datasource)[0]
            results.append((setting, target_value, {}))

        return results

    def update_daily_close(self, price: float):
        """"""
        # 每天下午5点结算，晚上算另外一个交易日,周五算到下周一

        d = self.datetime.date()
        t = self.datetime.time()
        if t > time(hour=17, minute=0):
            if d.weekday() == 4:
                d = d + timedelta(days=3)
            else:
                d = d + timedelta(days=1)
        elif t < time(hour=8, minute=0):  # 周六凌晨算周一
            if d.weekday() == 5:
                d = d + timedelta(days=2)
        daily_result = self.daily_results.get(d, None)
        if daily_result:
            daily_result.close_price = price
            self.holding.last_price = price
        else:
            self.daily_results[d] = DailyResult(d, price)
            # 逐日盯市，改变持仓成本价格,需要用结算价（对商品期货是每日加权平均）
            # self.holding.long_price = self.holding.last_price
            # self.holding.short_price = self.holding.last_price
            self.holding.last_price = price

    def new_bar(self, bar: BarData):
        """"""
        self.bar = bar
        self.datetime = bar.datetime

        self.cross_limit_order()
        self.cross_stop_order()
        self.strategy.on_bar(bar)

        self.update_daily_close(bar.close_price)

    def new_tick(self, tick: TickData):
        """"""
        self.tick = tick
        self.datetime = tick.datetime

        self.cross_limit_order()
        self.cross_stop_order()
        self.strategy.on_tick(tick)

        self.update_daily_close(tick.last_price)

    def cross_limit_order(self):
        """
        Cross limit order with last bar/tick data.
        """
        if self.mode == BacktestingMode.BAR:
            long_cross_price = self.bar.low_price
            short_cross_price = self.bar.high_price
            long_best_price = self.bar.open_price
            short_best_price = self.bar.open_price
        else:
            long_cross_price = self.tick.ask_price_1
            short_cross_price = self.tick.bid_price_1
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        rejectedoids = []

        for order in list(self.active_limit_orders.values()):
            # Push order update with status "not traded" (pending).
            # if order.status == Status.SUBMITTING:
            #     order.status = Status.NOTTRADED
            #     self.strategy.on_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                order.direction == Direction.LONG
                and order.price >= long_cross_price
                and long_cross_price > 0
            )

            short_cross = (
                order.direction == Direction.SHORT
                and order.price <= short_cross_price
                and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            if order.offset == Offset.CLOSE:
                noshortpos = (order.direction == Direction.LONG) and (
                    self.holding.short_pos < order.volume)
                nolongpos = (order.direction == Direction.SHORT) and (
                    self.holding.long_pos < order.volume)
                if nolongpos or noshortpos:
                    rejectedoids.append(order.client_order_id)
                    continue

            # Push order udpate with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.on_order(order)

            self.active_limit_orders.pop(order.client_order_id)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
                pos_change = order.volume
            else:
                trade_price = max(order.price, short_best_price)
                pos_change = -order.volume

            turnover = trade_price * order.volume * self.size
            commission = turnover * self.rate
            slippage = order.volume * self.size * self.slippage

            trade = BacktestTradeData(
                full_symbol=order.full_symbol,
                symbol=order.symbol,
                exchange=order.exchange,
                client_order_id=order.client_order_id,
                tradeid=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                turnover=turnover,
                commission=commission,
                slippage=slippage,
                datetime=self.datetime,
                time=self.datetime.strftime("%H:%M:%S"),
                gateway_name=self.gateway_name,
            )
            if trade.offset == Offset.CLOSE:  # 平仓不会影响持仓成本价格
                if trade.direction == Direction.LONG:
                    trade.short_pnl = trade.volume * \
                        (self.holding.short_price - trade.price) * self.size
                else:
                    trade.long_pnl = trade.volume * \
                        (trade.price - self.holding.long_price) * self.size
            self.holding.update_trade(trade)
            trade.long_pos = self.holding.long_pos
            trade.long_price = self.holding.long_price
            trade.short_pos = self.holding.short_pos
            trade.short_price = self.holding.short_price

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

            self.trades[trade.vt_tradeid] = trade

        for oid in rejectedoids:
            order = self.active_limit_orders.pop(oid)
            order.status = Status.REJECTED
            # Push update to strategy.
            self.strategy.on_order(order)

    def cross_stop_order(self):
        """
        Cross stop order with last bar/tick data.
        """
        if self.mode == BacktestingMode.BAR:
            long_cross_price = self.bar.high_price
            short_cross_price = self.bar.low_price
            long_best_price = self.bar.open_price
            short_best_price = self.bar.open_price
        else:
            long_cross_price = self.tick.last_price
            short_cross_price = self.tick.last_price
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        rejectedoids = []

        for stop_order in list(self.active_stop_orders.values()):
            # Check whether stop order can be triggered.
            long_cross = (
                stop_order.direction == Direction.LONG
                and stop_order.price <= long_cross_price
            )

            short_cross = (
                stop_order.direction == Direction.SHORT
                and stop_order.price >= short_cross_price
            )

            if not long_cross and not short_cross:
                continue

            # close order must satisfy conditon that there are enough positions to close.
            if stop_order.offset == Offset.CLOSE:
                noshortpos = (stop_order.direction == Direction.LONG) and (
                    self.holding.short_pos < stop_order.volume)
                nolongpos = (stop_order.direction == Direction.SHORT) and (
                    self.holding.long_pos < stop_order.volume)
                if nolongpos or noshortpos:
                    rejectedoids.append(stop_order.client_order_id)
                    continue

            self.limit_order_count += 1
            stop_order.status = Status.ALLTRADED

            self.limit_orders[stop_order.client_order_id] = stop_order

            # Create trade data.
            if long_cross:
                trade_price = max(stop_order.price, long_best_price)
                pos_change = stop_order.volume
            else:
                trade_price = min(stop_order.price, short_best_price)
                pos_change = -stop_order.volume

            self.trade_count += 1

            turnover = trade_price * stop_order.volume * self.size
            commission = turnover * self.rate
            slippage = stop_order.volume * self.size * self.slippage

            trade = BacktestTradeData(
                full_symbol=stop_order.full_symbol,
                symbol=stop_order.symbol,
                exchange=stop_order.exchange,
                client_order_id=stop_order.client_order_id,
                tradeid=str(self.trade_count),
                direction=stop_order.direction,
                offset=stop_order.offset,
                price=trade_price,
                volume=stop_order.volume,
                turnover=turnover,
                commission=commission,
                slippage=slippage,
                datetime=self.datetime,
                time=self.datetime.strftime("%H:%M:%S"),
                gateway_name=self.gateway_name,
            )
            if trade.offset == Offset.CLOSE:  # 平仓不会影响持仓成本价格
                if trade.direction == Direction.LONG:
                    trade.short_pnl = trade.volume * \
                        (self.holding.short_price - trade.price) * self.size
                else:
                    trade.long_pnl = trade.volume * \
                        (trade.price - self.holding.long_price) * self.size
            self.holding.update_trade(trade)
            trade.long_pos = self.holding.long_pos
            trade.long_price = self.holding.long_price
            trade.short_pos = self.holding.short_pos
            trade.short_price = self.holding.short_price

            self.trades[trade.vt_tradeid] = trade

            # Update stop order.

            self.active_stop_orders.pop(stop_order.client_order_id)

            # Push update to strategy.
            self.strategy.on_stop_order(stop_order)
            self.strategy.on_order(stop_order)

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

        for oid in rejectedoids:
            stop_order = self.active_stop_orders.pop(
                stop_order.client_order_id)
            stop_order.status = Status.REJECTED
            self.limit_order_count += 1
            self.limit_orders[oid] = stop_order
            # Push update to strategy.
            self.strategy.on_stop_order(stop_order)
            self.strategy.on_order(stop_order)

    def load_bar(
        self, full_symbol: str, days: int, interval: Interval, callback: Callable, datasource: str = 'DataBase'
    ):
        """
        called by strategy
        """
        # 以交易日为准，一星期内的时间补上周末二天，大于一周的时间暂不考虑补全额外的交易日
        tradedays = abs(days)
        weekday = self.start.weekday()
        adddays = 2 if (days - weekday > 0) else 0
        if weekday == 6:
            tradedays = days + 1
        else:
            tradedays = days + adddays

        start = self.start - timedelta(days=tradedays)
        end = self.start
        if datasource == 'DataBase':
            self.history_bar = load_bar_data(
                self.symbol,
                self.exchange,
                interval,
                start,
                end
            )
            self.history_bar_startix = 0
            self.history_bar_endix = len(self.history_bar)
        elif datasource == "Memory":
            startix = 0
            endix = 0
            totalbarlist = sqglobal.history_bar[self.full_symbol]
            if not totalbarlist:
                self.output('load_bar数据为空，请先读入')
                return
            totalbars = len(totalbarlist)
            for i in range(totalbars):
                if totalbarlist[i].datetime < start:
                    continue
                startix = i
                break
            for i in reversed(range(totalbars)):
                if totalbarlist[i].datetime > end:
                    continue
                endix = i
                break
            endix = min(endix + 1, totalbars)
            self.history_bar_startix = startix
            self.history_bar_endix = endix
            self.history_bar = totalbarlist

        self.historybar_callback = callback

        # self.days = days
        # self.callback = callback

    def load_tick(self, full_symbol: str, days: int, callback: Callable, datasource: str = 'DataBase'):
        """
        called by strategy
        """
        tradedays = abs(days)
        weekday = self.start.weekday()
        adddays = 2 if (days - weekday > 0) else 0
        if weekday == 6:
            tradedays = days + 1
        else:
            tradedays = days + adddays

        start = self.start - timedelta(days=tradedays)
        end = self.start
        if datasource == 'DataBase':
            self.history_tick = load_tick_data(
                self.symbol,
                self.exchange,
                start,
                end
            )
            self.history_tick_startix = 0
            self.history_tick_endix = len(self.history_tick)

        elif datasource == 'Memory':
            startix = 0
            endix = 0
            totalticklist = sqglobal.history_tick[self.full_symbol]
            if not totalticklist:
                self.output('load_tick数据为空，请先读入')
                return
            totalticks = len(totalticklist)
            for i in range(totalticks):
                if totalticklist[i].datetime < start:
                    continue
                startix = i
                break
            for i in reversed(range(totalticks)):
                if totalticklist[i].datetime > end:
                    continue
                endix = i
                break
            endix = min(endix + 1, totalticks)
            self.history_tick_startix = startix
            self.history_tick_endix = endix
            self.history_tick = totalticklist

        self.historytick_callback = callback

        # self.days = days
        # self.callback = callback

    def send_order(
        self,
        strategy: CtaTemplate,
        req: OrderData
    ):
        """"""

        req.client_order_id = self.order_count
        self.order_count += 1
        req.status = Status.NOTTRADED
        self.limit_order_count += 1
        self.strategy_orderid_map[strategy.strategy_name].add(
            req.client_order_id)
        self.active_limit_orders[req.client_order_id] = req
        self.limit_orders[req.client_order_id] = req

        return req.client_order_id

    def send_stop_order(
        self,
        strategy: CtaTemplate,
        req: OrderData
    ):
        """"""
        req.client_order_id = self.order_count
        self.order_count += 1
        req.status = Status.NEWBORN
        self.stop_order_count += 1
        self.strategy_orderid_map[strategy.strategy_name].add(
            req.client_order_id)
        self.active_stop_orders[req.client_order_id] = req
        self.stop_orders[req.client_order_id] = req

        return req.client_order_id

    def cancel_order(self, strategy: CtaTemplate, orderid: int):
        """
        Cancel order by orderid.
        """
        if orderid in self.active_limit_orders:
            order = self.active_limit_orders.pop(orderid)
            order.status = Status.CANCELLED
            self.strategy.on_order(order)
        elif orderid in self.active_stop_orders:
            stop_order = self.active_stop_orders.pop(orderid)
            stop_order.status = Status.CANCELLED
            self.strategy.on_stop_order(stop_order)

    def cancel_all(self, strategy: CtaTemplate):
        """
        Cancel all orders, both limit and stop.
        """
        orderids = list(self.active_limit_orders.keys())
        for orderid in orderids:
            order = self.active_limit_orders.pop(orderid)
            order.status = Status.CANCELLED
            self.strategy.on_order(order)

        stop_orderids = list(self.active_stop_orders.keys())
        for orderid in stop_orderids:
            stop_order = self.active_stop_orders.pop(orderid)
            stop_order.status = Status.CANCELLED
            self.strategy.on_stop_order(stop_order)

    def write_log(self, msg: str, strategy: CtaTemplate = None):
        """
        Write log message.
        """
        msg = f"{self.datetime}\t{msg}"
        self.logs.append(msg)

    def send_email(self, msg: str, strategy: CtaTemplate = None):
        """
        Send email to default receiver.
        """
        pass

    def get_engine_type(self):
        """
        Return engine type.
        """
        return self.engine_type

    def put_strategy_event(self, strategy: CtaTemplate):
        """
        Put an event to update strategy status.
        """
        pass

    def output(self, msg):
        """
        Output message of backtesting engine.
        """
        print(f"{datetime.now()}\t{msg}")

    def sync_strategy_data(self, strategy: CtaTemplate):
        pass

    def get_position_holding(self, acc: str, full_symbol: str):
        return self.holding

    def get_account(self, accountid):
        pass

    def get_order(self, orderid: int):
        if orderid in self.limit_orders:
            order = self.limit_orders.get(orderid)
            return order
        if orderid in self.stop_orders:
            order = self.stop_orders.get(orderid)
            return order

    def get_tick(self, full_symbol: str):
        pass

    def get_trade(self, vt_tradeid):
        return self.trades.get(vt_tradeid, None)

    def get_all_trades(self):
        return list(self.trades.values())

    def get_position(self, key):
        pass

    def get_contract(self, full_symbol):
        return self.contract

    def get_all_active_orders(self, full_symbol: str = ""):
        active_orders = list(self.active_limit_orders.values())
        active_orders.extend(self.active_stop_orders.values())
        return active_orders

    def get_strategy_active_orderids(self, strategy_name: str):
        active_orderids = set(self.active_limit_orders.keys())
        return active_orderids

    def get_all_orders(self):
        """
        Return all limit order data of current backtesting result.
        """
        return list(self.limit_orders.values())

    def get_all_daily_results(self):
        """
        Return all daily result data.
        """
        return list(self.daily_results.values())


class DailyResult:
    """"""

    def __init__(self, date: date, close_price: float):
        """"""
        self.date = date
        self.close_price = close_price
        self.pre_close = 0

        self.trades = []
        self.trade_count = 0

        self.start_pos = 0
        self.end_pos = 0

        self.turnover = 0
        self.commission = 0
        self.slippage = 0

        self.trading_pnl = 0
        self.holding_pnl = 0
        self.total_pnl = 0
        self.net_pnl = 0

    def add_trade(self, trade: Union[TradeData, BacktestTradeData]):
        """"""
        self.trades.append(trade)

    def calculate_pnl(
        self,
        pre_close: float,
        start_pos: float,
        size: int,
        rate: float,
        slippage: float,
    ):
        """"""
        self.pre_close = pre_close

        # Holding pnl is the pnl from holding position at day start
        self.start_pos = start_pos
        self.end_pos = start_pos
        self.holding_pnl = self.start_pos * \
            (self.close_price - self.pre_close) * size

        # Trading pnl is the pnl from new trade during the day
        self.trade_count = len(self.trades)

        for trade in self.trades:
            if trade.direction == Direction.LONG:
                pos_change = trade.volume
            else:
                pos_change = -trade.volume

            turnover = trade.price * trade.volume * size

            self.trading_pnl += pos_change * \
                (self.close_price - trade.price) * size
            self.end_pos += pos_change
            self.turnover += turnover
            self.commission += turnover * rate
            self.slippage += trade.volume * size * slippage

        # Net pnl takes account of commission and slippage cost
        self.total_pnl = self.trading_pnl + self.holding_pnl
        self.net_pnl = self.total_pnl - self.commission - self.slippage


def optimize(
    target_name: str,
    strategy_class: CtaTemplate,
    setting: dict,
    full_symbol: str,
    interval: str,
    start: datetime,
    rate: float,
    slippage: float,
    size: float,
    pricetick: float,
    capital: int,
    end: datetime,
    mode: BacktestingMode,
    datasource: str = "DataBase"
):
    """
    Function for running in multiprocessing.pool
    """
    engine = BacktestingEngine()

    engine.set_parameters(
        full_symbol=full_symbol,
        interval=interval,
        start=start,
        rate=rate,
        slippage=slippage,
        size=size,
        pricetick=pricetick,
        capital=capital,
        end=end,
        mode=mode
    )

    engine.add_strategy(strategy_class, setting)
    engine.load_data(datasource)
    engine.run_backtesting()
    engine.calculate_result()
    statistics = engine.calculate_statistics(output=False)

    target_value = statistics[target_name]
    return (str(setting), target_value, statistics)


@lru_cache(maxsize=1000000)
def _ga_optimize(parameter_values: tuple, datasource: str = 'DataBase'):
    """"""
    setting = dict(parameter_values)

    result = optimize(
        ga_target_name,
        ga_strategy_class,
        setting,
        ga_full_symbol,
        ga_interval,
        ga_start,
        ga_rate,
        ga_slippage,
        ga_size,
        ga_pricetick,
        ga_capital,
        ga_end,
        ga_mode,
        datasource
    )
    return (result[1],)


def ga_optimize(parameter_values: list, datasource: str = 'DataBase'):
    """"""
    return _ga_optimize(tuple(parameter_values), datasource)


@lru_cache(maxsize=10)
def load_bar_data(
    symbol: str,
    exchange: Exchange,
    interval: Interval,
    start: datetime,
    end: datetime
):
    """"""
    return database_manager.load_bar_data(
        symbol, exchange, interval, start, end
    )


@lru_cache(maxsize=10)
def load_tick_data(
    symbol: str,
    exchange: Exchange,
    start: datetime,
    end: datetime
):
    """"""
    return database_manager.load_tick_data(
        symbol, exchange, start, end
    )


# GA related global value
ga_end = None
ga_mode = None
ga_target_name = None
ga_strategy_class = None
ga_setting = None
ga_full_symbol = None
ga_interval = None
ga_start = None
ga_rate = None
ga_slippage = None
ga_size = None
ga_pricetick = None
ga_capital = None
