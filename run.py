"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from __future__ import annotations
from read_bayesnet import BayesNet
from variable_elim import VariableElimination


def fewest_dependent_variables_heuristic(variables:list[str], net:BayesNet) -> list[str]:
    var_parent = list(filter(lambda x: x[0] in variables, map(lambda x: (x[0], len(x[1])), [(k, v) for k, v in net.parents.items()])))
    ordered = sorted(
        var_parent, 
        key=lambda x: x[1]
    )
    return list(map(lambda x: x[0], ordered))

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
    #factors = [net.probabilities[node] for node in net.nodes]
    ve = VariableElimination(net)
    
    #print("Factor product test:")
    #print(ve.factor_product(factors[0], factors[2]))
    
    #print("Factor marginalization test:")
    #print(ve.factor_marginalization(factors[2], factors[0]))
    
    #print("Factor reduction test:")
    #print(ve.factor_reduction(factors[2], "Burglary", "True"))
    
    
    # Set the node to be queried as follows:
    query = ['Alarm', 'Earthquake']

    # The evidence is represented in the following way (can also be empty when there is no evidence): 
    evidence = {'Burglary': 'True'}

    # Determine your elimination ordering before you call the run function. The elimination ordering   
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # ordering can for example be set
    #  as follows:
    elim_order = fewest_dependent_variables_heuristic(list(filter(lambda x: x not in evidence and x not in query, net.nodes)), net)
  
    #THE LAST ONE NEED TO BE THE VARIABLE IN THE QUERY
    #elim_order.append(query)
    # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:   
    result = ve.run(query, evidence, elim_order)
