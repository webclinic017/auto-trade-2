"""
General utility functions.
"""

import json
from pathlib import Path
from typing import Callable

from .constant import Exchange


def extract_full_symbol(full_symbol: str):
    """
    :return: (symbol, exchange)
    """
    tmp = full_symbol.split(' ')
    if len(tmp) < 4:
        return "unknwonsymbol", Exchange.SHFE
    symbol = tmp[2] + tmp[3]
    exchange_str = tmp[0]
    ex = Exchange(exchange_str)
    if ex in [Exchange.SHFE, Exchange.DCE, Exchange.INE]:
        symbol = symbol.lower()
    return symbol, ex


# from ctp symbol to full symbol
def generate_full_symbol(exchange: Exchange, symbol: str, type: str = 'F'):
    product = ''
    contractno = ''
    fullsym = symbol
    if symbol:
        if type == 'F' or type == 'O':
            for count, word in enumerate(symbol):
                if word.isdigit():
                    break
            product = symbol[:count]
            contractno = symbol[count:]
            fullsym = exchange.value + ' ' + type + ' '\
                + product.upper() + ' ' + contractno
        elif type == 'S':
            combo = symbol.split(' ', 1)[1]
            symbol1 = combo.split('&')[0]
            symbol2 = combo.split('&')[1]
            for count, word in enumerate(symbol1):
                if word.isdigit():
                    break
            product = symbol1[:count]
            contractno = symbol1[count:]
            for count, word in enumerate(symbol2):
                if word.isdigit():
                    break
            product += ('&' + symbol2[:count])
            contractno += ('&' + symbol2[count:])
            fullsym = exchange.value + ' ' + type + ' '\
                + product.upper() + ' ' + contractno
    return fullsym


def extract_vt_symbol(vt_symbol: str):
    """
    :return: (symbol, exchange)
    """
    symbol, exchange_str = vt_symbol.split('.')
    return symbol, Exchange(exchange_str)


def generate_vt_symbol(symbol: str, exchange: Exchange):
    return f'{symbol}.{exchange.value}'


def _get_trader_dir(temp_name: str):
    """
    Get path where trader is running in.
    """
    cwd = Path.cwd()
    temp_path = cwd.joinpath(temp_name)

    # If .StarQuant folder exists in current working directory,
    # then use it as trader running path.
    if temp_path.exists():
        return cwd, temp_path

    # Otherwise use home path of system.
    home_path = Path.home()
    temp_path = home_path.joinpath(temp_name)

    # Create .StarQuant folder under home path if not exist.
    if not temp_path.exists():
        temp_path.mkdir()

    return home_path, temp_path


TRADER_DIR, TEMP_DIR = _get_trader_dir(".StarQuant")


def get_file_path(filename: str):
    """
    Get path for temp file with filename.
    """
    return TEMP_DIR.joinpath(filename)


def get_folder_path(folder_name: str):
    """
    Get path for temp folder with folder name.
    """
    folder_path = TEMP_DIR.joinpath(folder_name)
    if not folder_path.exists():
        folder_path.mkdir()
    return folder_path


def get_icon_path(filepath: str, ico_name: str):
    """
    Get path for icon file with ico name.
    """
    ui_path = Path(filepath).parent
    icon_path = ui_path.joinpath("ico", ico_name)
    return str(icon_path)


def load_json(filename: str):
    """
    Load data from json file in temp path.
    """
    filepath = get_file_path(filename)

    if filepath.exists():
        with open(filepath, mode='r') as f:
            data = json.load(f)
        return data
    else:
        save_json(filename, {})
        return {}


def save_json(filename: str, data: dict):
    """
    Save data into json file in temp path.
    """
    filepath = get_file_path(filename)
    with open(filepath, mode='w+') as f:
        json.dump(data, f, indent=4)


def round_to_pricetick(price: float, pricetick: float):
    """
    Round price to price tick value.
    """
    rounded = round(price / pricetick, 0) * pricetick
    return rounded


def round_to(value: float, target: float):
    """
    Round price to price tick value.
    """
    rounded = int(round(value / target)) * target
    return rounded


def virtual(func: Callable):
    """
    mark a function as "virtual", which means that this function can be override.
    any base class should use this or @abstractmethod to decorate all functions
    that can be (re)implemented by subclasses.
    """
    return func