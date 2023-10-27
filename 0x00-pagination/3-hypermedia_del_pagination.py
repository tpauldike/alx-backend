#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """The goal here is that if between two queries, certain rows are
        removed from the dataset, the user does not miss items from
        dataset when changing page.

        Args:
            index (int, optional): current start index of the return page.
            Defaults to None.
            page_size (int, optional): the current page size. Defaults to 10.

        Returns:
            Dict: dictionary containing the following key-value pairs
            --> index, next_index, page_size, data
        """
        max_index = len(self.dataset())
        assert type(index) is int and index < max_index
        gap = 0

        for idx in range(index, max_index):
            if self.indexed_dataset().get(idx):
                break
            gap += 1

        next_index = idx + page_size
        data = self.dataset()[idx:next_index]

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }
