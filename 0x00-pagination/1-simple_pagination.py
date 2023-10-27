#!/usr/bin/env python3
"""Implement simple pagination"""
import csv
import math
from typing import List, Tuple


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get_page

        Args:
            page (int, optional): page. Defaults to 1.
            page_size (int, optional): page_size. Defaults to 10.

        Returns:
            List[List]: list of items
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        self.dataset()

        if self.__dataset is None:
            return []

        idx_range = index_range(page, page_size)
        data = self.__dataset[idx_range[0]:idx_range[1]]
        return data
