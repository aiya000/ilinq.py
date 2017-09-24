#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides Linq class, which is a python version of linq like c#.
"""

from collections import defaultdict
from functools import reduce
import itertools


class Linq(list):
    """  Class for handling Linq like C# """
    def where(self, cond_f=None):
        """
        Return the Linq instance filtered by cond_f.
        And if cond_f is None, return all items.

        >>> Linq(range(10 + 1)).where(lambda n: n % 5 == 0)
        Linq<0, 5, 10>
        """
        list_ = self[:]
        return Linq([
            item for item in list_
            if cond_f is None or cond_f(item)])

    def where_in(self, list_, select_f=None):
        """
        Return items which the condition that select_f(item) in list_

        >>> Linq([1, 3, 5, 100]).where_in([1, 2, 3])
        Linq<1, 3>
        >>> Linq([1, 3, 5, 100]).where_in(
        ...     [1, 2, 3],
        ...     select_f=lambda x: x % 2)
        Linq<1, 3, 5>
        """
        return self.where(
            lambda x: x in list_ if select_f is None else
            select_f(x) in list_)

    def select(self, select_f=None):
        """
        Return the linq instance selected by select_f.

        >>> Linq(range(10 + 1)).select(lambda n: n % 3)
        Linq<0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1>
        """
        return Linq([
            item if select_f is None else
            select_f(item) for item in self[:]])

    def select_i(self, select_f=None):
        """
        Return the linq instance selected_by select_f with index parameter.

        >>> linq = Linq(range(5)).reverse()
        >>> linq.select_i(lambda i, x: x ** i)
        Linq<1, 3, 4, 1, 0>
        """
        return Linq([
            (
                item if select_f is None else
                select_f(i, item)
            ) for i, item in enumerate(self)])

    def select_many(self, select_f=None):
        """
        Return the linq instance selected by select_f and flatten.

        >>> linq = Linq([
        ...     {"name": "yassu", "ids": (12, 13)},
        ...     {"name": "aiya",  "ids": (20, 21)}])
        >>> linq.select_many(lambda obj: obj["ids"])
        (12, 13, 20, 21)
        """
        return Linq(reduce(
            lambda x, y: x + y, [
                (
                    item if select_f is None
                    else select_f(item)
                )for item in self[:]]))

    def select_many_i(self, select_f=None):
        """
        Return selected flatten list by select_f

        >>> linq = Linq([[9, 8, 7, 6], [5, 4, 3, 2, 1, 0]])
        >>> linq.select_many_i()
        Linq<9, 8, 7, 6, 5, 4, 3, 2, 1, 0>
        >>> linq.select_many_i(lambda i, x: i**x)
        Linq<0, 1, 128, 729, 1024, 625, 216, 49, 8, 1>
        """
        return self.select_many().select_i(select_f)

    def take(self, num):
        """
        Return first num numbers of this object.

        >>> linq = Linq(range(10))
        >>> linq.take(4)
        Linq<0, 1, 2, 3>
        >>> linq.take(100)
        Linq<0, 1, 2, 3, 4, 5, 6, 7, 8, 9>
        """
        return Linq([self[j] for j in range(min(num, len(self)))])

    def take_while(self, cond_f=None):
        """
        Return Linq object consisted by first some elements such that
        ``cond_f(item)``.

        >>> Linq(range(10)).take_while(lambda x: x < 5)
        Linq<0, 1, 2, 3, 4>
        """

        if cond_f is None:
            return self.copy()

        list_ = list()
        for j in range(self.count()):
            if cond_f(self[j]):
                list_.append(self[j])
            else:
                return Linq(list_)
            j += 1
        return Linq(list_)

    def take_while_i(self, cond_f=None):
        """
        Return Linq object consisted by first some elements such that
        ``cond_f(index, item)``.

        >>> linq = Linq(range(10)).concat(Linq(range(10)).reverse())
        >>> linq
        Linq<0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0>
        >>> linq.take_while_i(lambda i, x: i * x <= 10)
        Linq<0, 1, 2, 3>
        """
        if cond_f is None:
            return self

        list_ = list()
        for i in range(self.count()):
            if cond_f(i, self[i]):
                list_.append(self[i])
            else:
                break
        return Linq(list_)

    def skip(self, num):
        """
        Return the linq skipped first ``num`` elements.

        >>> Linq(range(10)).reverse().skip(3)
        Linq<6, 5, 4, 3, 2, 1, 0>
        """
        if self.count() >= num:
            return self[num:]
        else:
            raise IndexError('Linq: {} is so short.'.format(self))

    def skip_while(self, cond_f=None):
        """
        Return the linq skipped first some elements such that ``cond_f(item)``.

        >>> Linq([5, 4, 3, 100, 2, 101, 1, 102]).skip_while(lambda x: x < 50)
        Linq<100, 2, 101, 1, 102>
        """
        res = itertools.dropwhile(
            lambda x: False is cond_f if cond_f is None else cond_f(x),
            self)
        return Linq(res)

    def skip_while_i(self, cond_f=None):
        """
        Return the linq skipped first some elements such
        that ``cond_f(i, item)``.

        >>> Linq(range(10)).skip_while_i(lambda i, x: i * x < 10)
        Linq<4, 5, 6, 7, 8, 9>
        """
        if cond_f is None:
            return self

        j = 0
        while j < self.count() and cond_f(j, self[j]):
            j += 1
        return self[j:]

    def concat(self, *linqs):
        """
        >>> linq = Linq(range(4))
        >>> linq.concat(Linq(range(5)).select(lambda x: x*x))
        Linq<0, 1, 2, 3, 0, 1, 4, 9, 16>

        >>> linq1 = Linq(range(5))
        >>> linq2 = Linq(range(4)).select(lambda x: x * x)
        >>> linq3 = Linq(range(3)).select(lambda x: x * x * x)
        >>> linq1.concat(linq2, linq3)
        Linq<0, 1, 2, 3, 4, 0, 1, 4, 9, 0, 1, 8>
        """
        res = self
        for linq in linqs:
            res = Linq(res.to_list() + linq.to_list())
        return res

    def default_if_empty(self, default=None):
        """
        if self is empty, return Linq([default]) else self.

        >>> Linq(range(3)).default_if_empty()
        Linq<0, 1, 2>
        >>> Linq(range(3)).default_if_empty("default")
        Linq<0, 1, 2>

        >>> Linq([]).default_if_empty()
        Linq<None>
        >>> Linq([]).default_if_empty("default")
        Linq<default>
        """
        list_ = Linq(self[:]).take(1)
        if len(list_) == 1:
            return Linq(self[:])
        else:
            return Linq([default])

    @staticmethod
    def repeat(obj, num):
        """
        Return Linq instance which has num objs.

        >>> Linq.repeat('Hello', 5)
        Linq<Hello, Hello, Hello, Hello, Hello>
        """
        return Linq([obj] * num)

    def distinct(self, key_f=None):
        """
        Return self deleted duplicates

        >>> linq1 = Linq(range(4))
        >>> linq2 = Linq(range(5)).select(lambda x: x * x)
        >>> linq1.concat(linq2).distinct()
        Linq<0, 1, 2, 3, 4, 9, 16>
        """
        list_ = list()
        val_list = list()
        for item in self[:]:
            val = item if key_f is None else key_f(item)
            if val not in val_list:
                list_.append(item)
                val_list.append(val)
        return Linq(list_)

    def except_(self, other, key_f=None):
        """
        If key_f is None, return self values except for other values.

        >>> Linq(range(10)).except_(Linq(range(4)))
        Linq<4, 5, 6, 7, 8, 9>

        If key_f is not None, return self values with condition that
        key_f(item) doesn't contain key_f(other_item) items.

        >>> linq1 = Linq([1, 2, -3, -4, -5])
        >>> linq2 = Linq([2, 3, 5, 7, 6])
        >>> linq1.except_(linq2, key_f=lambda x: abs(x))
        Linq<1, -4>
        """
        res = list()
        for item in self[:]:
            val = item if key_f is None else key_f(item)
            if val not in other:
                res.append(item)
        return Linq(res)

    def intersect(self, other):
        """
        Return the intersection set of self and other.

        >>> linq1 = Linq([2.0, -2.0, 2.1, -2.2, 2.3, 2.4, 2.5, 2.3])
        >>> linq2 = Linq([2.1, 2.2])
        >>> linq1.intersect(linq2)
        Linq<2.1>
        """
        return Linq([item for item in self if item in other])

    def union(self, other):
        """
        return Linq object of the union set.

        >>> Linq([1, 2, 2, 3]).union([3, 4, 5, 6])
        Linq<1, 2, 3, 4, 5, 6>
        """
        list_ = self.distinct()
        for item in other:
            if item not in list_:
                list_.append(item)
        return list_

    def zip(self, other, zip_f):
        """
        collect self_items and other_items by zip_f.

        >>> Linq([1, 2, 3]).zip(Linq([4, 5, 6]), lambda x, y: (x, y))
        Linq<(1, 4), (2, 5), (3, 6)>
        >>> Linq([1, 2, 3]).zip(Linq([4, 5]), lambda x, y: (x, y))
        Linq<(1, 4), (2, 5)>
        >>> Linq([1, 2]).zip(Linq([4, 5, 6]), lambda x, y: (x, y))
        Linq<(1, 4), (2, 5)>
        """
        return Linq([
            zip_f(self[i], other[i]) for i in range(
                min(len(self), len(other)))])

    def reverse(self):
        """
        Return reversed Linq object.

        Note that this method is overrited from list class.

        >>> linq = Linq(range(6))
        >>> linq
        Linq<0, 1, 2, 3, 4, 5>
        >>> linq.reverse()
        Linq<5, 4, 3, 2, 1, 0>
        """
        linq = self
        list.reverse(linq)
        return linq

    def order_by(self, key_f=None, desc=False):
        """
        If desc=False and key_f=None, sort in ascending order.

        >>> Linq([1.1, 2.3, -2, 5.3, 1.3]).order_by()
        Linq<-2, 1.1, 1.3, 2.3, 5.3>

        If desc=True, sort in descending order

        >>> Linq([1.1, 2.3, -2, 5.3, 1.3]).order_by(desc=True)
        Linq<5.3, 2.3, 1.3, 1.1, -2>

        If key_f is not None, sort by result of key_f

        >>> linq = Linq([
        ...     {"name": "person1", "age": 23},
        ...     {"name": "person2", "age": 25},
        ...     {"name": "person3", "age": 21}])
        >>> linq.order_by(key_f=lambda person: person["age"])
        Linq<
            {'name': 'person3', 'age': 21},
            {'name': 'person1', 'age': 23},
            {'name': 'person2', 'age': 25}>
        """
        return Linq(sorted(self[:], key=key_f, reverse=desc))

    def inject(self, initial_value, func, last_f=None):
        """
        Return the result of
        func(func(func(initial_value, self[0]), self[1]) .. self[length - 1])
        filtered by last_f.

        >>> Linq(range(100 + 1)).inject(0, lambda res, x: res + x)
        5050
        >>> Linq(range(100 + 1)).inject(
        ...     0,
        ...     lambda res, x: res + x,
        ...     last_f=lambda x: x + 100)
        5150
        """
        res = initial_value
        for item in self[:]:
            res = func(res, item)
        return res if last_f is None else last_f(res)

    def count(self, cond_f=None):
        """
        Return the length with condition that cond_f(item).

        >>> Linq(range(10)).count()
        10
        >>> Linq(range(10)).count(lambda x: x >= 8)
        2
        """
        return len(self.where(
            cond_f if cond_f is not None else
            lambda x: True))

    def first(self, cond_f=None):
        """
        Return the first element with cond_f(item)

        >>> Linq([3, 2, 5, 8]).first()
        3
        >>> Linq([3, 2, 5, 8]).first(cond_f=lambda x: x % 2 == 0)
        2
        """
        for item in self[:]:
            if cond_f is None or cond_f(item):
                return item
        raise IndexError('This linq with condition is Empty.')

    def first_or_default(self, cond_f=None, default=None,):
        """
        Return the first element with cond_f(item) and default value
        is default.

        >>> Linq([3, 2, 5, 8]).first_or_default()
        3
        >>> Linq([3, 2, 5, 8]).first_or_default(
            cond_f=lambda x: x % 2 == 0)
        2
        >>> Linq([3, 2, 5, 8]).first_or_default(
        ...     cond_f=lambda x: x > 100,
        ...     default=100)
        100
        """
        for item in self:
            if cond_f is None or cond_f(item):
                return item
        return default

    def single(self, cond_f=None):
        """
        If this object consists of one object, return this object.
        Otherwise, error is occured.

        >>> Linq([]).single()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 95, in
          single @staticmethod
        IndexError: This linq with condition is empty.
        >>> Linq([12]).single()
        12
        >>> Linq([12, 15]).single()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 97, in
        single
        IndexError: This linq with condition is more long.
        """
        obj = self.where(cond_f)
        if obj.count() == 0:
            raise IndexError('This linq with condition is empty.')
        elif obj.count() == 2:
            raise IndexError('This linq with condition is more long.')
        return obj[0]

    def single_or_default(self, default=None, cond_f=None):
        """
        If this obj consists only one object, return this object.

        If this obj is empty, return default.

        If this obj consists more than one objects, error is occured.

        >>> Linq([]).single_or_default(16)
        16
        >>> Linq([32]).single_or_default()
        32
        >>> Linq([12, 35]).single_or_default()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 104, in
        single_or_default
            \"\"\"
          File "/Users/yuki_yasuda/dev/ilinq.py/ilinq/ilinq.py", line 97, in
        single
            @staticmethod
        IndexError: This linq with condition is more long.
        """
        obj = self.where(cond_f)
        if obj.count() == 0:
            return default
        return obj.single()

    def last(self, cond_f=None):
        """
        Return the first element with cond_f(item)

        >>> Linq([3, 2, 5, 8]).last()
        8
        >>> Linq([3, 2, 5, 8]).last(lambda x: x % 4 == 1)
        5
        """
        return self.where(cond_f)[-1]

    def last_or_default(self, cond_f=None, default=None):
        """
        Return the last element with cond_f(item) and default value
        is default.

        >>> Linq([3, 2, 5, 8]).last_or_default()
        8
        >>> Linq([3, 2, 5, 8]).last_or_default(cond_f=lambda x: x % 2 == 1)
        5
        >>> Linq([3, 2, 5, 8]).last_or_default(
        ...     cond_f=lambda x: x > 100,
        ...     default=-100)
        -100
        """
        try:
            return self.where(cond_f).last()
        except IndexError:
            return default

    def element_at(self, ind):
        """
        Return the element at ind index.

        >>> Linq([3, 2, 5, 8]).element_at(2)
        5
        """
        list_ = self.take(ind + 1).to_list()
        if len(list_) == ind + 1:
            return list_[ind]
        raise IndexError("This linq doesn't have {} items.".format(ind))

    def element_at_or_default(self, num, default=None):
        """
        If there is num-th element, return this.
        Else return default value.

        >>> from ilinq.ilinq import Linq
        >>> linq = Linq([1, 2])
        >>> linq.element_at_or_default(0)
        1
        >>> linq.element_at_or_default(3)
        # None
        """
        try:
            return self.element_at(num)
        except IndexError:
            return default

    def min(self, key_f=None):
        """
        Return minimal value in this object.
        if key_f is defined, return minimal value by key_f(item).

        >>> Linq([-1, 2, 3, -4.3, 2]).min()
        -4.3
        >>> Linq([-1, 2, 3, -4.3, 2]).min(abs)
        -1
        """
        try:
            return min(
                self,
                key=lambda x: x if key_f is None else key_f(x))
        except ValueError:
            raise StopIteration('This linq is empty.')

    def min_all(self, key_f=None):
        """
        Return the Linq object which consists of minimal numbers
        computed by key_f.

        >>> linq = Linq(range(5)).concat(Linq(range(4)))
        >>> linq
        Linq<0, 1, 2, 3, 4, 0, 1, 2, 3>
        >>> linq.min_all()
        Linq<0, 0>
        >>> linq.min_all(key_f=lambda x: x % 4)
        Linq<0, 4, 0>
        """
        if self.count() == 0:
            return Linq()
        min_value = self.select(key_f).min()
        return self.where(
            cond_f=lambda item:
            (item if key_f is None else key_f(item)) == min_value)

    def max(self, key_f=None):
        """
        Return maximal value in this object.
        If key_fis defined, return minimal value by key_f(item).

        >>> Linq([-1, 2, 3, -4.3, 2]).max()
        3
        >>> Linq([-1, 2, 3, -4.3, 2]).max(abs)
        -4.3
        """
        try:
            return max(
                self,
                key=lambda x: x if key_f is None else key_f(x))
        except ValueError:
            raise StopIteration('This linq is empty.')

    def max_all(self, key_f=None):
        """
        Return the Linq object which consists of maximal numbers
        computed by key_f.

        >>> linq = Linq(range(5)).concat(Linq(range(5)))
        >>> linq
        Linq<0, 1, 2, 3, 4, 0, 1, 2, 3, 4>
        >>> linq.max_all()
        Linq<4, 4>
        >>> linq.max_all(key_f=lambda x: x % 3)
        Linq<2, 2>
        """
        if self.count() == 0:
            return Linq()

        max_value = self.max(key_f=key_f)
        return Linq([
            item for item in self if
            (
                item if key_f is None else
                key_f(item)
            ) == max_value])

    def sum(self, select_f=None):
        """
        Return total of select_f(item)

        >>> Linq(range(100 + 1)).sum()
        5050
        >>> persons = Linq([
        ...     {'name': 'yassu', 'age': 25},
        ...     {'name': 'person2', 'age': 3}
        ... ])
        >>> persons.sum(select_f=lambda x: x['age'])
        28
        """
        return sum(self.select(select_f))

    def average(self, select_f=None):
        """
        Return average of select_f(item)

        >>> Linq([1, 2, 3, 4, 5]).average()
        3.0
        >>> persons = Linq([
        ...     {'name': 'yassu', 'age': 25},
        ...     {'name': 'person2', 'age': 3}
        ... ])
        >>> persons.average(select_f=lambda x: x['age'])
        14.0
        """
        return self.select(select_f).sum() / float(self.count())

    def contains(self, item, key_f=None):
        """
        Return either item is in self or not.

        If key_f is setted, we compare by ``key_f`` function.

        >>> books = Linq([
        ...     {'name': 'book1', 'code': '23'},
        ...     {'name': 'book2', 'code': '32'}
        ... ])
        >>> books.contains(
        ...     {'name': 'undefined', 'code': '32'},
        ...     key_f=lambda b: b['code'])
        True
        """
        return (
            item if key_f is None else
            key_f(item)) in self.select(key_f)

    def all(self, cond_f):
        """
        if all of cond_f(item) is True, return True.
        Else return False.

        >>> numbers = Linq([14, 28, 35])
        >>> numbers.all(lambda n: n % 7 == 0)
        True
        >>> numbers.all(lambda n: n % 8 == 0)
        False
        """
        for item in self:
            if cond_f(item) is False:
                return False
        return True

    def any(self, cond_f=None):
        """
        If there exists item such that cond_f(item), return True.
        Else return false.

        >>> Linq([1, 2, 3, 4, 5]).any()
        True
        >>> Linq([1, 2, 3, 4, 5]).any(lambda n: n > 100)
        False
        >>> Linq([1, 2, 3, 4, 5]).any(lambda n: n == 3)
        True
        """
        return self.select(cond_f).contains(True)

    def group_by(self, grouping_f):
        """
        Group items by grouping_f.

        >>> foods = Linq([
        ...     {'name': 'tomato', 'kind': 'Vegetable'},
        ...     {'name': 'hormone', 'kind': 'Meat'},
        ...     {'name': 'butdock root', 'kind': 'Vegetable'},
        ...     {'name': 'pumpkin', 'kind': 'Vegetable'}
        ... ])

        >>> foods.group_by(lambda f: f['kind'])
        Linq<
            {Vegetable:
                Linq<{'name': 'tomato', 'kind': 'Vegetable'},
                {'name': 'butdock root', 'kind': 'Vegetable'},
                {'name': 'pumpkin', 'kind': 'Vegetable'}>
            },
            {Meat:
                Linq<{'name': 'hormone', 'kind': 'Meat'}>
            }
        >
        """
        from ilinq.igroup import IPair, IGroup
        group = IGroup()
        group_dict = defaultdict(lambda: Linq([]))
        for item in self[:]:
            group_dict[grouping_f(item)].append(item)

        for key, values in group_dict.items():
            group.append(IPair(key, values))
        return group

    def to_list(self):
        """
        Return the list of items.
        This is equivalent list(self)
        """
        return list(self)

    def copy(self):
        """
        Return shallow copied self
        """
        return Linq(self[:])

    def to_set(self):
        """
        Return the set of items.

        >>> Linq([3, 2, 5, 3, 8]).to_set()
        {8, 2, 3, 5}
        """
        return set(self)

    def to_dict(self, key_f=None, value_f=None):
        """
        Return dictionary consisted of [key_f(item), value_f(item)].

        >>> Linq(range(4)).to_dict(key_f=lambda x: x, value_f=lambda x: x * x)
        {0: 0, 1: 1, 2: 4, 3: 9}

        If key_f or value_f is Identity function, this keyword is omitted.

        >>> Linq(range(4)).to_dict(value_f=lambda x: x * x)
        {0: 0, 1: 1, 2: 4, 3: 9}
        """
        mat = Linq([
            [
                item if key_f is None else key_f(item),
                item if value_f is None else value_f(item)
            ] for item in self])
        if mat.distinct(key_f=lambda row: row[0]) == mat:
            return dict(mat)
        else:
            raise ValueError('key numbers are dupplicated.')

    def __getitem__(self, val):
        if isinstance(val, int):
            return super().__getitem__(val)
        elif isinstance(val, slice):
            return Linq(super().__getitem__(val))

    def __str__(self):
        s = 'Linq<'
        for item in self:
            s += str(item)
            s += ', '
        if self.count() > 0:
            s = s[:-2]
        return s + '>'

    def __repr__(self):
        return str(self)
