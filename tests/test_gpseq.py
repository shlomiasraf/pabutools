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


def test_large_input_random_structure():
    import random
    projects = [Project(f"c{i+1}", cost=random.randint(1, 5)) for i in range(30)]
    instance = Instance(projects, 50)
    approvals = [
        ApprovalBallot(random.sample(range(30), random.randint(3, 5)))
        for _ in range(100)
    ]
    profile = ApprovalProfile(approvals)
    result = gpseq(instance, profile)
    assert sum(p.cost for p in result) <= 50
    assert all(p in instance.projects for p in result)
