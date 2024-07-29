import datetime
from numpy import (add, argsort, array)

from mesp.utilities.mesp_data import MespData
from mesp.utilities.grad import (grad_fw as grad, grad_fix)
from mesp.utilities.matrix_computations import (generate_factorizations)
from mesp.approximation.localsearch import localsearch


def frankwolfe(C: MespData, s, varfix=False): 
    
    start = datetime.datetime.now()

    n, d = C.n, C.d
    # S0, S1 = C.S0, C.S1 # not used with shrinking technique 
    S0, S1 = [], []

    V, Vsquare, E = C.V, C.Vsquare, C.E # TODO: this should always work
    
    # if C.V != None:
    #     V, Vsquare, E = C.V, C.Vsquare, C.E
    # else:
    #     V, Vsquare, E = generate_factorizations(C.C, n, d)
    
    # run local search
    LB, x, ltime = localsearch(V, E, n, d, s, S1, S0)
    Obj_f = LB
    # print("The lower bound at current node is", Obj_f)
 
    gamma_t = 0.0  
    t = 0.0
    mindual = 1e+10
    dual_gap = 1 # duality gap
    Obj_f = 1 # primal value
    alpha = 1e-4 # target accuracy
    
    while(dual_gap/(Obj_f+dual_gap) > alpha):
        Obj_f, subgrad, y, dual_gap, w, v = grad(V, Vsquare, S1, S0, x, s, d, varfix)
        
        t = t + 1
        gamma_t = 1/(t+2) # step size
        
        x = [(1-gamma_t)*x_i for x_i in x] 
        y = [gamma_t*y_i for y_i in y]
        x = add(x,y).tolist() # update x
        mindual = min(mindual, Obj_f+dual_gap) # update the upper bound
        
        #print('primal value = ', Obj_f, ', duality gap = ', dual_gap)

        
    # supp = (n-x.count(0)) # size of support of output
    
    end = datetime.datetime.now()
    time = (end-start).total_seconds()

    if not varfix:
        return  mindual, x, time, w, v
    else:
        cut_gap = Obj_f + dual_gap - LB
        return cut_gap, v, w, x, LB


def alter_fw(V, Vsquare, E, fval, S1, S0, n, d, s): 
    
    # run local search
    Obj_f, x, ltime = localsearch(V, E, n, d, s, S1, S0)
    # print("The lower bound at current node is", Obj_f)
 
    gamma_t = 0.0  
    t = 0.0
    mindual = 1e+10
    dual_gap = 1 # duality gap
    Obj_f = 1 # primal value
    alpha = 1e-4 # target accuracy
    
    while(dual_gap/(Obj_f+dual_gap) > alpha):
        Obj_f, subgrad, y, dual_gap, fixzero, fixone = grad(V, Vsquare, S1, S0, x, s, d)
        
        t = t + 1
        gamma_t = 1/(t+2) # step size
        
        x = [(1-gamma_t)*x_i for x_i in x] 
        y = [gamma_t*y_i for y_i in y]
        x = add(x,y).tolist() # update x
        mindual = min(mindual, Obj_f+dual_gap) # update the upper bound
        
        #print('primal value = ', Obj_f, ', duality gap = ', dual_gap)
    cutgap = mindual-fval
    if dual_gap > cutgap + 1e-4:  #talpha: target accuracy
        alpha = 1e-5
        while(dual_gap/(Obj_f+dual_gap) > alpha):
            Obj_f, subgrad, y, dual_gap, fixzero, fixone = grad_fix(V, Vsquare, S1, S0, x, s, d)
            
            t = t + 1
            gamma_t = 1/(t+2) # step size
            
            x = [(1-gamma_t)*x_i for x_i in x] 
            y = [gamma_t*y_i for y_i in y]
            x = add(x,y).tolist() # update x
            mindual = min(mindual, Obj_f+dual_gap) # update the upper bound
            
    return  mindual-fval
