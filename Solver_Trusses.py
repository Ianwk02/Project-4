#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:34:19 2021

@author: kendrick
"""

import numpy as np

# compute unknown displacements 
def ComputeDisplacements(K, F, n_unknowns):
    # extract submatrix of unknowns
    K11 = K[0:n_unknowns,0:n_unknowns]
    F1 = F[0:n_unknowns]
    
    d = np.linalg.solve(K11,F1)
    
    return d

# postprocess the forces at known displacement nodes
def PostprocessReactions(K, d, F, n_unknowns, nodes):
    # These are computed net forces and do not
    # take into account external loads applied
    # at these nodes
    F = np.matmul(K[n_unknowns:,0:n_unknowns], d)
    
    # Postprocess the reactions
    for node in nodes:
        if node.xidx >= n_unknowns:
            node.AddReactionXForce(F[node.xidx-n_unknowns][0] - node.xforce_external)
        if node.yidx >= n_unknowns:
            node.AddReactionYForce(F[node.yidx-n_unknowns][0] - node.yforce_external)
        
    return F

# determine internal member loads
def ComputeMemberForces(bars):
    # COMPLETE THIS FUNCTION
    # Compute member forces for all bars using equation 14-23 
    for bar in bars:
        E=bar.E
        A=bar.A
        L=bar.Length()
        lambdax=bar.LambdaTerms()[0]
        lambday=bar.LambdaTerms()[1]
        Near=bar.init_node
        Far=bar.end_node
        Dx_Near=Near.xdisp
        Dy_Near=Near.ydisp
        Dx_Far=Far.xdisp
        Dy_Far=Far.ydisp
        
        B= np.array([[-1*lambdax,-1*lambday,lambdax,lambday]])
        C=np.array([Dx_Near,Dy_Near,Dx_Far,Dy_Far]).reshape(4,1)
        bar.axial_load= ((E*A)/L)*(B@C)
    pass
    
# compute the normal stresses
def ComputeNormalStresses(bars):
    # COMPLETE THIS FUNCTION
    # Compute normal stress for all bars
    for bar in bars:
        bar.normal_stress=(bar.axial_load/bar.A)
    pass

# compute the critical buckling load of a member
def ComputeBucklingLoad(bars):
    # COMPLETE THIS FUNCTION
    # Compute critical buckling load for all bars
    for bar in bars:
        E=bar.E
        L=bar.Length()
        I=bar.It
        
        bar.buckling_load=(((np.pi**2)*E*I)/(L**2))
        
    pass
