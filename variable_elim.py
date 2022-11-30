"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from __future__ import annotations
import pandas as pd
from pandas import DataFrame
import pandasql as ps
class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def execute_query(self):
        return lambda q: ps(q, globals())

    def factor_reduction(self, factor_a:DataFrame, variable:str) -> DataFrame:
        """

        Args:
            factor_a (DataFrame): [description]
            variable (str): [description]

        Returns:
            DataFrame: [description]
        """
        print(factor_a, variable)
        query = ""
        pass

    def factor_product(self, factor_a:DataFrame, factor_b:DataFrame) -> DataFrame:
        pass 

    def factor_marginalization(self, factor_a:DataFrame, factor_b:DataFrame, marginal_factor:DataFrame) -> DataFrame:
        pass


    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
