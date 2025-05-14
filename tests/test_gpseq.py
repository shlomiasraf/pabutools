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
    p1 = Project("c1", cost=1)
    instance = Instance([p1], 1)
    profile = ApprovalProfile([ApprovalBallot([5])])
    with pytest.raises(Exception):
        gpseq(instance, profile)


def test_small_input():
    p1 = Project("c1", cost=1)
    instance = Instance([p1], 1)
    profile = ApprovalProfile([ApprovalBallot([0])])
    result = gpseq(instance, profile)
    assert [p.name for p in result] == ["c1"]


def test_medium_input():
    p1 = Project("c1", cost=1.5)
    p2 = Project("c2", cost=1.5)
    p3 = Project("c3", cost=1.0)
    instance = Instance([p1, p2, p3], 3)
    profile = ApprovalProfile([
        ApprovalBallot([0, 1]),
        ApprovalBallot([0]),
        ApprovalBallot([1, 2]),
        ApprovalBallot([2]),
    ])
    result = gpseq(instance, profile)
    assert set(p.name for p in result) == {"c1", "c3"} or {"c2", "c3"}


def test_large_input_random_structure_with_fairness():
    import random
    from collections import defaultdict

    num_projects = 30
    num_voters = 100
    budget = 50

    # Step 1: Create 30 projects with random costs between 1 and 5
    projects = [Project(f"c{i+1}", cost=random.randint(1, 5)) for i in range(num_projects)]
    instance = Instance(projects, budget)

    # Step 2: Create approval ballots - each voter approves 3 to 5 random projects
    approvals = [
        ApprovalBallot(random.sample(range(num_projects), random.randint(3, 5)))
        for _ in range(num_voters)
    ]
    profile = ApprovalProfile(approvals)

    # Step 3: Run the GPseq algorithm
    result = gpseq(instance, profile)

    # Step 4: Basic validity checks
    assert sum(p.cost for p in result) <= budget  # total cost must not exceed the budget
    assert all(p in instance.projects for p in result)  # all selected projects must exist in the instance

    # Step 5: Fairness check – ensure that popular projects are represented
    project_approval_count = defaultdict(int)
    for ballot in profile:
        for project_index in ballot.approved_projects:
            project_approval_count[project_index] += 1

    # Define a project as "popular" if it is approved by at least 20 voters
    popular_threshold = 20
    popular_projects = {
        p for i, p in enumerate(instance.projects)
        if project_approval_count[i] >= popular_threshold
    }

    selected_set = set(result)
    num_represented = len(popular_projects & selected_set)

    # Ensure that at least one-third of the popular projects are selected
    assert num_represented >= max(1, len(popular_projects) // 3)
