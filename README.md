# MESPpy
This repository provides a declarative language for formulating, approximating, solving, and experimenting with the **maximum entropy sampling problem** (MESP).


## IMPORTANT NOTE 6/28
This is my updated version of Quill's MESP repo.  Many of the attributes remain the same.
In terms of testing, I have gone through several matrices of data from Li's collection of data... some of which still cannot be handled by this code.
I am having problems with the variable fixing in general.  I added a False return if there are too many variables fixed or the matrix becomes empty.  However, I think this is just a band-aid to a deeper root issue :(

## maximum entropy sampling problem

The Maximum entropy sampling problem aims to select a principle submatrix from a given covariance matrix that possesses the max log
determinant (ldet is derived from the mathematical definition of entropy). 

```math
\begin{align*}
\text{maximize} \; \left\{\textbf{ldet} \, C_{S, S} : S \subseteq [n], \left| S \right| = s \right\}.
\end{align*}
```

It is important to note that this problem is nonconvex by nature.  

    

**Contributors.**
This codebase is a newer version of Quill Healey's MESPpy worked on by Emily Wright under Dr. Weijun Xie
Yongchun is responsible for the approximation and bounding algorithms [codebase](https://github.com/yongchunli-13/Approximation-Algorithms-for-MESP)
Quill is responsible for the creation of this declarative language driven repository, the branch and bound framework, and the related experimentation features.
I, Emily, have continued working on experimentation with this codebase with different datasets and subproblem sizes.  I have made alterations to some of the code to bypass some of the variable fixing and mathematical errors.  I also have worked on the code hygiene, deleting uncalled functions and adding explanations where needed.


## References
<a id="1">[1]</a>: Maximum-Entropy Sampling Algorithms and Application, Fampa and Lee.

<a id="2">[2]</a> : Convex Optimization, Vandenberghe and Boyd

<a id="3">[3]</a> : Best Best Principal Submatrix Selection for the Maximum Entropy Sampling Problem: Scalable Algorithms and Performance Guarantees, Li and Xie

<a id="4">[4]</a> : Efficient Solution of Maximum-Entropy Sampling Problems, Anstreicher

