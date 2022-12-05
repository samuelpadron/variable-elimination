"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from __future__ import annotations
import pandas as pd
from pandas import DataFrame
class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network


    def factor_reduction(self, factor:DataFrame, column_observed:str, value_observed:str) -> DataFrame:
        """_summary_

        Args:
            factor_a (DataFrame): _description_
            value_observed (str): _description_

        Returns:
            DataFrame: _description_
        """
        
        return factor[factor[column_observed] == value_observed].drop(columns=[column_observed])
        

    

    def factor_product(self, factor_a:DataFrame, factor_b:DataFrame) -> DataFrame:
        common_columns = set(factor_a.columns.values).intersection(set(factor_b.columns.values))
        common_columns.remove('prob')
        print(common_columns)
        return self.multiply_on_columns(common_columns, factor_a, factor_b)
        

    def factor_marginalization(self, factor:DataFrame, variable:DataFrame) -> DataFrame:
        """compute factor by marginalizing over a variable

        Args:
            factor (DataFrame): _description_
            marginal_factor (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        columns = [x for x in factor.columns.values if x != 'prob' and x != variable.columns.values[0]]
        return factor.groupby(columns, axis=0, as_index=False).sum()
        
        

    def multiply_on_columns(self, columns:list[str], factor_a:DataFrame, factor_b:DataFrame) -> DataFrame:
        """

        Args:
            columns (list[str]): _description_
            factor_a (DataFrame): _description_
            factor_b (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        new_pd = factor_a.copy()
        for column in columns:
            new_pd = new_pd.merge(factor_b, on=column)
            new_pd['prob'] = new_pd['prob_x'] * new_pd['prob_y']
            new_pd = new_pd.drop(columns=['prob_x', 'prob_y', column])
        return new_pd

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
