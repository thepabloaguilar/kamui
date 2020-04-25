from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest

from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus
from kamui.core.usecase.project.create_new_project import (
    CreateNewProjectUsecase,
    CreateNewProject,
)


@pytest.fixture(scope="function")
def create_new_project() -> Mock:
    return Mock(spec=CreateNewProject)


@pytest.fixture(scope="function")
def create_new_project_usecase(create_new_project: Mock) -> CreateNewProjectUsecase:
    return CreateNewProjectUsecase(create_new_project)


def test_create_new_project(
    create_new_project_usecase: CreateNewProjectUsecase, create_new_project: Mock
) -> None:
    project_title = "Test Project Title"
    expected_project = Project(
        project_id=uuid4(),
        title="Test Project Title",
        created_at=datetime.now(),
        status=ProjectStatus.ACTIVE,
    )

    create_new_project.return_value = expected_project
    actual_project = create_new_project_usecase(project_title)

    create_new_project.assert_called_once()
    create_new_project.assert_called_with(project_title)
    assert expected_project == actual_project
