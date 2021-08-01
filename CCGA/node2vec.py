# -*- coding: utf-8 -*- 
# Time : 2021/7/31 14:29 
# Author : Kristina 
# File : node2vec.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-


import random


class Node2Vec:
    def __init__(self, G, emb_size=128, p=4, q=1, length_walk=50, num_walks=10, window_size=10, num_iters=2):
        self.G = G
        self.emb_size = emb_size
        self.length_walk = length_walk
        self.num_walks = num_walks
        self.window_size = window_size
        self.num_iters = num_iters
        self.p = p
        self.q = q

    def walk_step(self, t, v):
        nbs = list(self.G.neighbors(v))
        if len(nbs) == 0:
            return False

        weights = [1] * len(nbs)
        for i, x in enumerate(nbs):
            if t == x:
                weights[i] = 1 / self.p
            elif not self.G.has_edge(t, x):
                weights[i] = 1 / self.q

        return random.choices(nbs, weights=weights, k=1)[0]

    def random_walk(self):
        # random walk with every node as start point
        walks = []
        for node in self.G.nodes():
            walk = [node]
            nbs = list(self.G.neighbors(node))
            if len(nbs) > 0:
                walk.append(random.choice(nbs))
                for i in range(2, self.length_walk):
                    v = self.walk_step(walk[-1], walk[-2])
                    if not v:
                        break
                    walk.append(v)
            walk = [str(x) for x in walk]
            walks.append(walk)
        # print(walks)
        return walks

    def sentenses(self):
        sts = []
        for _ in range(self.num_walks):
            sts.extend(self.random_walk())
        print(sts)

        return sts
