"""
Implementation of the GPseq algorithm from:

"Proportionally Representative Participatory Budgeting: Axioms and Algorithms"
by Haris Aziz, Bettina Klaus, Jérôme Lang, and Markus Brill (2017)
https://arxiv.org/abs/1711.08226

Programmer: <Shlomi Asraf>
Date: 2025-05-13
"""

from __future__ import annotations
from typing import List
from pabutools.election.instance import Instance, Project
from pabutools.election.profile import ApprovalProfile
from pabutools.election.ballot.approvalballot import ApprovalBallot
from pabutools.tiebreaking import TieBreakingRule, lexico_tie_breaking


def gpseq(
    instance: Instance,
    profile: ApprovalProfile,
    tie_breaking: TieBreakingRule = lexico_tie_breaking
) -> List[Project]:
    """
    Algorithm 6: GPseq - Greedy Phragmen Sequence algorithm.

    Selects a subset of projects to minimize the maximal load on any voter.

    Parameters
    ----------
    instance : Instance
        The instance including all projects and the total budget.
    profile : ApprovalProfile
        The approval profile of the voters.
    tie_breaking : TieBreakingRule, optional
        The rule to apply when multiple projects have equal impact.

    Returns
    -------
    List[Project]
        A list of selected projects.

    Examples
    --------
    Example 1:
      Algorithm 6: GPseq - Greedy Phragmen Sequence algorithm.

    Selects a subset of projects to minimize the maximal load on any voter.

    Parameters
    ----------
    instance : Instance
        The instance including all projects and the total budget.
    profile : ApprovalProfile
        The approval profile of the voters.
    tie_breaking : TieBreakingRule, optional
        The rule to apply when multiple projects have equal impact.

    Returns
    -------
    List[Project]
        A list of selected projects.

    Examples
    --------
    >>> p1 = Project("c1", cost=2)
    >>> p2 = Project("c2", cost=2)
    >>> p3 = Project("c3", cost=1)
    >>> instance = Instance([p1, p2, p3], 3)
    >>> profile = ApprovalProfile([ApprovalBallot([0]), ApprovalBallot([0]), ApprovalBallot([1]), ApprovalBallot([1])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c1', 'c3']

    >>> p1 = Project("c1", cost=1)
    >>> instance = Instance([p1], 1)
    >>> profile = ApprovalProfile([ApprovalBallot([0])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c1']

    >>> p1 = Project("c1", cost=1)
    >>> p2 = Project("c2", cost=2)
    >>> instance = Instance([p1, p2], 2)
    >>> profile = ApprovalProfile([ApprovalBallot([0]), ApprovalBallot([0]), ApprovalBallot([0]), ApprovalBallot([1])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c1']

    >>> p1 = Project("c1", cost=2)
    >>> p2 = Project("c2", cost=1.5)
    >>> p3 = Project("c3", cost=1.5)
    >>> instance = Instance([p1, p2, p3], 3)
    >>> profile = ApprovalProfile([ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([2]), ApprovalBallot([2])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c2', 'c3']

    >>> p1 = Project("c1", cost=2)
    >>> p2 = Project("c2", cost=2)
    >>> p3 = Project("c3", cost=0.8)
    >>> instance = Instance([p1, p2, p3], 2)
    >>> profile = ApprovalProfile([ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([0, 1]), ApprovalBallot([2]), ApprovalBallot([2])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c3']

    >>> p1 = Project("c1", cost=1.5)
    >>> p2 = Project("c2", cost=1.5)
    >>> p3 = Project("c3", cost=1.0)
    >>> instance = Instance([p1, p2, p3], 3)
    >>> profile = ApprovalProfile([ApprovalBallot([0, 1]), ApprovalBallot([0]), ApprovalBallot([1, 2]), ApprovalBallot([2])])
    >>> result = gpseq(instance, profile)
    >>> [p.name for p in result]
    ['c3', 'c1']
    """
    pass  # To be implemented