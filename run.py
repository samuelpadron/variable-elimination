"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
import itertools

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    
    # These are the variables read from the network that should be used for variable elimination
    #print("Nodes:")
    #print(net.nodes)
    #print("Values:")
    #print(net.values)
    #print("Parents:")
    #print(net.parents)
    #print("Probabilities:")
    #print(net.probabilities)

    # Make your variable elimination code in the seperate file: 'variable_elim'. 
    # You use this file as follows:
    factors = [net.probabilities[node] for node in net.nodes]
    ve = VariableElimination(net)
    
    #print("Factor product test:")
    #print(ve.factor_product(factors[0], factors[2]))
    
    #print("Factor marginalization test:")
    #print(ve.factor_marginalization(factors[2], factors[0]))
    
    #print("Factor reduction test:")
    #print(ve.factor_reduction(factors[2], "Burglary", "True"))
    
    #ve.factor_reduction(net.probabilities['Alarm'], net.probabilities['Alarm'].columns.values[1])
    #print(net.probabilities['Alarm'], "\n")
    ve.factor_reduction(net.probabilities['Alarm'], 'Earthquake', 'True')
    
    
    # Set the node to be queried as follows:
    query = 'Alarm'

    # The evidence is represented in the following way (can also be empty when there is no evidence): 
    evidence = {'Burglary': 'True'}

    # Determine your elimination ordering before you call the run function. The elimination ordering   
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # ordering can for example be set as follows:
    elim_order = net.nodes

    # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:   
    ve.run(query, evidence, elim_order)
