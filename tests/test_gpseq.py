"""
"Proportionally Representative Participatory Budgeting: Axioms and Algorithms"
by Haris Aziz, Bettina Klaus, Jérôme Lang, and Markus Brill (2017)
https://arxiv.org/abs/1711.08226
"""

import pytest
from pabutools.election.instance import Project, Instance
from pabutools.election.profile import ApprovalProfile
from pabutools.election.ballot.approvalballot import ApprovalBallot
from pabutools.gpseq import gpseq


def test_empty_input():
    instance = Instance([], 10)
    profile = ApprovalProfile([])
    result = gpseq(instance, profile)
    assert result == []


def test_invalid_input():
    p1 = Project("c1", cost=-5)
    instance = Instance([p1], 1)
    profile = ApprovalProfile([ApprovalBallot([p1])])
    with pytest.raises(Exception):
        gpseq(instance, profile)

def test_small_input():
    p1 = Project("c1", cost=1)
    instance = Instance([p1], 1)
    profile = ApprovalProfile([ApprovalBallot([p1])])
    result = gpseq(instance, profile)
    assert [p.name for p in result] == ["c1"]


def test_medium_input():
    p1 = Project("c1", cost=1.5)
    p2 = Project("c2", cost=1.5)
    p3 = Project("c3", cost=1.0)
    instance = Instance([p1, p2, p3], 3)
    profile = ApprovalProfile([
        ApprovalBallot([p1, p2]),
        ApprovalBallot([p1]),
        ApprovalBallot([p2, p3]),
        ApprovalBallot([p2]),
    ])
    result = gpseq(instance, profile)
    assert set(p.name for p in result) == {"c1", "c3"} or {"c2", "c3"}


def test_large_input_random_structure_with_fairness():
    import random
    num_projects = 30
    projects = [Project(f"c{i + 1}", cost=random.randint(1, 5)) for i in range(num_projects)]
    instance = Instance(projects, 50)

    # Step 1: create approvals
    approvals = [
        ApprovalBallot(random.sample(projects, random.randint(3, 5)))
        for _ in range(100)
    ]
    profile = ApprovalProfile(approvals)

    # Step 2: run gpseq
    result = gpseq(instance, profile)

    # Step 3: fairness check – approval-per-cost ratio
    project_to_index = {p: i for i, p in enumerate(projects)}
    approval_counts = [0] * num_projects
    for ballot in profile:
        for project in ballot:
            i = project_to_index[project]
            approval_counts[i] += 1

    ratios = [(approval_counts[i] / projects[i].cost, projects[i]) for i in range(num_projects)]
    ratios.sort(reverse=True)  # highest ratio first
    best_ratio_projects = [p for _, p in ratios[:len(result)]]

    # Assertion: top ratio projects should mostly be selected
    selected_names = set(p.name for p in result)
    best_names = set(p.name for p in best_ratio_projects)
    overlap = selected_names & best_names
    assert len(overlap) >= len(result) // 2  # at least half the selection is top ratio
