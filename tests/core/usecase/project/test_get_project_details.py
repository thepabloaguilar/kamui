from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest
from returns.maybe import Maybe
from returns.result import Success, Result

from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus
from kamui.core.entity.source import SourceType
from kamui.core.entity.stream import StreamList, Stream
from kamui.core.usecase.failure import BusinessFailureDetails
from kamui.core.usecase.project.get_project_details import (
    FindProjectByProjectId,
    FindStreamsByProject,
    GetProjectDetailsUsecase,
)


@pytest.fixture(scope="function")
def find_project_by_project_id() -> Mock:
    return Mock(spec=FindProjectByProjectId)


@pytest.fixture(scope="function")
def find_streams_by_project() -> Mock:
    return Mock(spec=FindStreamsByProject)


@pytest.fixture(scope="function")
def get_project_details_usecase(
    find_project_by_project_id: Mock, find_streams_by_project: Mock
) -> GetProjectDetailsUsecase:
    return GetProjectDetailsUsecase(find_project_by_project_id, find_streams_by_project)


def test_should_return_failure_not_found_when_project_was_not_found(
    get_project_details_usecase: GetProjectDetailsUsecase,
    find_project_by_project_id: Mock,
) -> None:
    project_id = uuid4()
    project: Maybe[None] = Maybe.from_value(None)
    find_project_by_project_id.return_value = Success(project)

    actual = get_project_details_usecase(project_id)

    find_project_by_project_id.assert_called_once()
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NOT_FOUND" == actual.failure().reason


def test_should_return_projects_details_without_streams(
    get_project_details_usecase: GetProjectDetailsUsecase,
    find_project_by_project_id: Mock,
    find_streams_by_project: Mock,
) -> None:
    project_id = uuid4()
    project = Project(
        project_id=project_id,
        title="Test Project Title",
        created_at=datetime.now(),
        status=ProjectStatus.ACTIVE,
    )
    project_maybe: Maybe[Project] = Maybe.from_value(project)
    find_project_by_project_id.return_value = Success(project_maybe)
    find_streams_by_project.return_value = Success(StreamList([]))

    actual = get_project_details_usecase(project_id)

    find_project_by_project_id.assert_called_once()
    find_streams_by_project.assert_called_once()
    find_streams_by_project.assert_called_with(project)
    assert isinstance(actual, Result.success_type)
    assert project_id == actual.unwrap().project.project_id
    assert 0 == len(actual.unwrap().streams)


def test_should_return_projects_details_one_streams(
    get_project_details_usecase: GetProjectDetailsUsecase,
    find_project_by_project_id: Mock,
    find_streams_by_project: Mock,
) -> None:
    project_id = uuid4()
    project = Project(
        project_id=project_id,
        title="Test Project Title",
        created_at=datetime.now(),
        status=ProjectStatus.ACTIVE,
    )
    project_maybe: Maybe[Project] = Maybe.from_value(project)
    streams = [
        Stream(
            stream_id=uuid4(),
            name="Test Stream",
            source_type=SourceType.TOPIC,
            source_name="test_one_stream",
        ),
    ]
    find_project_by_project_id.return_value = Success(project_maybe)
    find_streams_by_project.return_value = Success(StreamList(streams))

    actual = get_project_details_usecase(project_id)

    find_project_by_project_id.assert_called_once()
    find_streams_by_project.assert_called_once()
    find_streams_by_project.assert_called_with(project)
    assert isinstance(actual, Result.success_type)
    assert project_id == actual.unwrap().project.project_id
    assert 1 == len(actual.unwrap().streams)
    assert streams == actual.unwrap().streams


def test_should_return_projects_details_two_streams(
    get_project_details_usecase: GetProjectDetailsUsecase,
    find_project_by_project_id: Mock,
    find_streams_by_project: Mock,
) -> None:
    project_id = uuid4()
    project = Project(
        project_id=project_id,
        title="Test Project Title",
        created_at=datetime.now(),
        status=ProjectStatus.ACTIVE,
    )
    project_maybe: Maybe[Project] = Maybe.from_value(project)
    streams = [
        Stream(
            stream_id=uuid4(),
            name="Test Stream One",
            source_type=SourceType.STREAM,
            source_name="test_two_stream",
        ),
        Stream(
            stream_id=uuid4(),
            name="Test Stream Two",
            source_type=SourceType.TOPIC,
            source_name="test_two_stream_detail",
        ),
    ]
    find_project_by_project_id.return_value = Success(project_maybe)
    find_streams_by_project.return_value = Success(StreamList(streams))

    actual = get_project_details_usecase(project_id)

    find_project_by_project_id.assert_called_once()
    find_streams_by_project.assert_called_once()
    find_streams_by_project.assert_called_with(project)
    assert isinstance(actual, Result.success_type)
    assert project_id == actual.unwrap().project.project_id
    assert 2 == len(actual.unwrap().streams)
    assert streams == actual.unwrap().streams
