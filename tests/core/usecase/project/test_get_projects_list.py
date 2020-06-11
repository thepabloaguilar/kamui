from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest

from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus
from kamui.core.usecase.project.get_projects_list import (
    GetProjectsListUsecase,
    GetProjectsList,
)


@pytest.fixture(scope="function")
def get_projects_list() -> Mock:
    return Mock(spec=GetProjectsList)


@pytest.fixture(scope="function")
def get_projects_list_usecase(get_projects_list: Mock) -> GetProjectsListUsecase:
    return GetProjectsListUsecase(get_projects_list)


def test_get_projects_details(
    get_projects_list_usecase: GetProjectsListUsecase, get_projects_list: Mock
) -> None:
    expected_projects_list = [
        Project(
            project_id=uuid4(),
            title="Test Project Title",
            created_at=datetime.now(),
            status=ProjectStatus.ACTIVE,
        ),
        Project(
            project_id=uuid4(),
            title="Test Super Project Title",
            created_at=datetime.now() - timedelta(days=10),
            status=ProjectStatus.INACTIVE,
        ),
    ]
    get_projects_list.return_value = expected_projects_list

    actual_projects_list = get_projects_list_usecase()

    get_projects_list.assert_called_once()
    assert expected_projects_list == actual_projects_list
