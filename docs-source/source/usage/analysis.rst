Analysis
========

We also provide tools to analyse the outcome --- the budget allocation. They are mostly collected
in the :py:mod:`~pabutools.analysis` module.

Justified Representation
------------------------

See :py:mod:`~pabutools.analysis.justifiedrepresentation`.

Priceability
------------

Pabutools enables searching for price systems that support a given budget allocation.
This allows users to to verify whether an allocation is priceable / stable-priceable.

To achieve this, the :py:func:`~pabutools.analysis.priceability.priceable` function is used.
It returns a :py:class:`~pabutools.analysis.priceability.PriceableResult`, which includes the allocation and a corresponding price system, among other details.

.. code-block:: python

    from pabutools.election import Instance, Project, ApprovalProfile, ApprovalBallot
    from pabutools.analysis.priceability import priceable

    p1 = Project('p1', cost=50)
    p2 = Project('p2', cost=150)
    p3 = Project('p3', cost=300)
    p4 = Project('p4', cost=250)
    p5 = Project('p5', cost=250)
    instance = Instance([p1, p2, p3, p4, p5], budget_limit=500)

    b1 = ApprovalBallot({p1, p2, p3, p4})
    b2 = ApprovalBallot({p1, p2, p3, p4})
    b3 = ApprovalBallot({p1, p2, p3, p4, p5})
    b4 = ApprovalBallot({p1, p2, p3, p5})
    b5 = ApprovalBallot({p1, p2, p3, p5})
    profile = ApprovalProfile([b1, b2, b3, b4, b5])

    allocation = [p4, p5]

    result = priceable(instance, profile, allocation)
    result.validate()       # Check if allocation is priceable - returns True
    result.voter_budget     # Result contains the supporting price system
    result.payment_functions

    result = priceable(instance, profile, allocation, stable=True)
    result.validate()       # Check if allocation is stable-priceable - returns False


Additionally, it is possible to search for ready-made budget allocations that satisfy priceability / stable-priceability.
To do this, simply omit the allocation parameter.

.. code-block:: python

    result = priceable(instance, profile, stable=True)
    result.allocation       # returns [p1, p2, p3]


.. note::
    The concept of the (stable) priceability axiom is tied to Linear Programming.

    Determining whether an allocation is (stable) priceable requires solving a Linear Program.
    Searching for allocations that are (stable) priceable requires solving an Integer Linear Program.

    The implementation uses the `python-mip` package which provides flexibility in choosing an ILP solver.

    For smaller instances the default ILP solver should suffice. However, for larger instances (in particular real life instances from `pabulib <http://pabulib.org>`_), `Gurobi solver <https://www.gurobi.com/>`_ performs significantly better.

    If you have access to a Gurobi license (e.g. as an academic or graduate student), it is highly recommended to use it.


Stable-Priceability Relaxations
-------------------------------

Since stable-priceability is not always satisfiable, several relaxations of the stability condition have been implemented.

By using a :py:class:`~pabutools.analysis.priceability_relaxation.Relaxation` class instance with :py:func:`~pabutools.analysis.priceability.priceable`, it is possible to measure how close an allocation is to satisfying the stability condition.
This, in turn, gives the ability to compare allocations based on their stability.

.. code-block:: python

    from pabutools.analysis.priceability_relaxation import MinMul

    allocation_1 = [p1, p2, p5]
    allocation_2 = [p4, p5]

    result_1 = priceable(instance, profile, allocation_1, stable=True, relaxation=MinMul(instance, profile))
    result_1.relaxation_beta

    result_2 = priceable(instance, profile, allocation_2, stable=True, relaxation=MinMul(instance, profile))
    result_2.relaxation_beta

    if result_1.relaxation_beta < result_2.relaxation_beta:
        print("allocation_1 is considered more stable")
    else:
        print("allocation_2 is considered more stable")


For details about the implemented relaxations see :py:mod:`~pabutools.analysis.priceability_relaxation`.
