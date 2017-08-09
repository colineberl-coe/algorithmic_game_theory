#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class Auction(object):

    """A class to represent a theoretical mechanism as described in AGT"""

    def __init__(self, auction_type='second_price', reserve_price=None,
                 bidders=None, bids=None, bids_and_bidders=None, **kwargs):
        """An auction has a type, a reserve price, bids, bidders

        Args:
            auction_type (str): type of auction; i.e. how winner is resolved
            reserve_price (float): the minimum price for good allocation
            bidders (iterable): the agents in the auction
            bids (iterable): the bids of the agents in the auction
            bids_and_bidders (dict): mapping of bidder -> bid. If not specified,
                bidders and bids will be zipped and passed to dict() constructor
            **kwargs: arbitrary keyword arguments

        Methods:
            _set_attributes: parse kwargs into class attributes
        """
        self._auction_type = auction_type
        self._reserve_price = 0.0 if reserve_price is None else reserve_price
        self._bidders = () if bidders is None else tuple(bidders)
        self._b = () if bids is None else tuple(bids)
        self._x = np.zeros_like(bids)  # allocation vector
        self._p = np.zeros_like(bids)  # payment vector
        self._any_nonzero_bids = self._b.count(0) < len(self._b)
        self.bids_and_bidders = bids_and_bidders if bids_and_bidders is not \
            None else dict(zip(bidders, bids))  # map of agents -> valuations
        self._resolved = False
        self._set_attributes(kwargs)

    def _set_attributes(self, kwargs):
        """Attach passed keyword-arguments to class namespace

        Args:
            kwargs (dict): key-word arguments passed to __init__

        Returns:
            (None): updates instance namespace
        """
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @classmethod
    def second_largest(numbers):
        """https://stackoverflow.com/a/16226255
        """
        count = 0
        m1 = m2 = float('-inf')
        for x in iter:
            count += 1
            if x > m2:
                if x >= m1:
                    m1, m2 = x, m1
                else:
                    m2 = x
        return m2 if count >= 2 else None

    def _resolve_auction(self):
        """Stores the index of the top two bids in self._b,
        stores the bid value at the winning index in self._p
        """
        # auction only resolves once
        if self._resolved:
            pass

        if not self._any_nonzero_bids:
            print "This auction has no non-zero bids. There is no winner"
            self._resolved = True
            return
        self._index_highest_bid = np.argmax(self._b)
        self._index_second_highest_bid = np.argpartition(self._b, -2)[-2]
        # Put a 1 in the index of the winning agent
        np.put(a=self._x, ind=self._index_highest_bid, v=1)
        if self._auction_type == 'first_price':
            np.put(a=self._p, ind=self._index_highest_bid,
                   v=self._b[self._index_highest_bid])
        elif self._auction_type == 'second_price':
            # Modify this for special rules e.g. SP + $0.01
            np.put(a=self._p, ind=self._index_highest_bid,
                   v=self._b[self._index_second_highest_bid] + 0.01)
        self._resolved = True