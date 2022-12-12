"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from __future__ import annotations
import pandas as pd
from pandas import DataFrame
from functools import reduce
import itertools
import numpy as np
class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network
        self.factors = [network.probabilities[node] for node in network.nodes]


    def factor_reduction(self, factor:DataFrame, column_observed:str, value_observed:str) -> DataFrame:
        """reduce factor by filtering rows containing only the observed value

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
        return self.multiply_on_columns(common_columns, factor_a, factor_b)
        

    def factor_marginalization(self, factor:DataFrame, variable: str) -> DataFrame:
        """compute factor by marginalizing over a variable

        Args:
            factor (DataFrame): _description_
            marginal_factor (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        columns = [x for x in factor.columns.values if x != 'prob' and x != variable]
        return factor.groupby(columns, axis=0, as_index=False).sum(numeric_only=True)
        
        
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
            new_pd = new_pd.drop(columns=['prob_x', 'prob_y'])
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
        print("The query variable is: {query}".format(query=query))
        
        print("The observed values are: {observed}".format(observed=observed))
    
        print("The elimination order is: {order}".format(order=elim_order))
        
        print("----------------------------------")
        # discard observed values
        filtered_factors = []
        for (column_observed, value_observed) in [(key,observed[key]) for key in observed]:
            for factor in self.factors:
                if column_observed in factor.columns:
                    filtered_factors.append(self.factor_reduction(factor, column_observed, value_observed))
                else:
                    filtered_factors.append(factor)
        self.factors = filtered_factors

        while len(elim_order) > 0:
            #update variable Z to be next in ordering
            next_variable = elim_order.pop(0) 
                
            #find which factors have Z
            factors_including_variable = [factor for factor in self.factors if next_variable in factor.columns.values]
            
            if len(factors_including_variable) > 0: #do we need this?

                print("The next variable to eliminate is " + next_variable)
            
                #get product of factors
                product = reduce(lambda i, j: self.factor_product(i, j), factors_including_variable)

                #sum out the variable
                result = self.factor_marginalization(product, next_variable)

                #see what the old factors are
                print("The old factors are:")
                for f in self.factors:
                    print(f)

                #remove factors that have Z from the formula
                self.factors = list(filter(lambda factor: next_variable not in factor.columns.values[:-1].tolist(), self.factors))

                #add new factor to list of factors
                self.factors.append(result)

                #check if the factors were correctly updated
                print("The resulting factors are:")
                for f in self.factors:
                    print(f)

                print("----------------------------------")
                print("Variables left to eliminate:")
                print(elim_order)

        #TODO normalize resulting factor
        # divide all the elements in the factor by the sum of the factor resulting by the marginalization of 
        #the varibable we have in the queue.
        print("resulting factor is:")
        print(self.factors)
            
            
            
        
        
        
        
