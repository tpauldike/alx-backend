#!/usr/bin/env python3
"""Simple helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """helper function

    Args:
        page (int): page index
        page_size (int): _description_

    Returns:
        Tuple: containing start-index and end-index
    """
    end_index = page * page_size
    return ((end_index - page_size, end_index))
