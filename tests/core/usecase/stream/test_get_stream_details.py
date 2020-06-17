from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest
from returns.maybe import Nothing, Maybe
from returns.result import Failure, Result, Success

from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus
from kamui.core.entity.source import SourceType
from kamui.core.entity.stream import Stream, KSQLStreamDetailed
from kamui.core.use_case.failure import FailureDetails, BusinessFailureDetails
from kamui.core.use_case.stream import GetStreamByNameUseCase
from kamui.core.use_case.stream.get_stream_details import (
    FindStreamByStreamId,
    FindProjectsByStream,
    GetStreamDetailsUseCase,
    StreamDetails,
)


@pytest.fixture(scope="function")
def find_stream_by_stream_id() -> Mock:
    return Mock(spec=FindStreamByStreamId)


@pytest.fixture(scope="function")
def find_projects_by_stream() -> Mock:
    return Mock(spec=FindProjectsByStream)


@pytest.fixture(scope="function")
def get_stream_by_name() -> Mock:
    return Mock(spec=GetStreamByNameUseCase)


@pytest.fixture(scope="function")
def get_stream_details_use_case(
    find_stream_by_stream_id: Mock,
    find_projects_by_stream: Mock,
    get_stream_by_name: Mock,
) -> GetStreamDetailsUseCase:
    return GetStreamDetailsUseCase(
        find_stream_by_stream_id, find_projects_by_stream, get_stream_by_name
    )


def test_should_return_stream_details_correctly(
    get_stream_details_use_case: GetStreamDetailsUseCase,
    find_stream_by_stream_id: Mock,
    find_projects_by_stream: Mock,
    get_stream_by_name: Mock,
) -> None:
    stream_id = uuid4()
    stream = Stream(
        stream_id=stream_id,
        name="TEST_STREAM",
        source_type=SourceType.STREAM,
        source_name="OTHER_STREAM_TEST",
    )
    project_list = [
        Project(
            project_id=uuid4(),
            title="Project One",
            created_at=datetime.now(),
            status=ProjectStatus.ACTIVE,
        ),
        Project(
            project_id=uuid4(),
            title="Project Two",
            created_at=datetime.now(),
            status=ProjectStatus.INACTIVE,
        ),
    ]
    ksql_stream_detailed = KSQLStreamDetailed(
        name="TEST_STREAM",
        fields=[
            KSQLStreamDetailed.KSQLStreamField(
                name="field_one",
                schema=KSQLStreamDetailed.KSQLStreamField.KSQLStreamFieldSchema(
                    type="INT"
                ),
            )
        ],
        type="STREAM",
        format="JSON",
        topic="SOME_TOPIC",
    )
    stream_details = StreamDetails.build(stream, project_list, ksql_stream_detailed)

    find_stream_by_stream_id.return_value = Success(Maybe.from_value(stream))
    find_projects_by_stream.return_value = Success(project_list)
    get_stream_by_name.return_value = Success(ksql_stream_detailed)

    actual = get_stream_details_use_case(stream_id)

    get_stream_by_name.assert_called_once()
    get_stream_by_name.assert_called_with(stream.name)
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), StreamDetails)
    assert stream_details == actual.unwrap()


def test_should_return_failure_when_stream_not_found(
    get_stream_details_use_case: GetStreamDetailsUseCase, find_stream_by_stream_id: Mock
) -> None:
    stream_id = uuid4()
    stream = Nothing
    find_stream_by_stream_id.return_value = Success(stream)

    actual = get_stream_details_use_case(stream_id)

    find_stream_by_stream_id.assert_called_once()
    find_stream_by_stream_id.assert_called_with(stream_id)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NOT_FOUND" == actual.failure().reason


def test_should_return_failure_when_find_stream_by_stream_id_fails(
    get_stream_details_use_case: GetStreamDetailsUseCase, find_stream_by_stream_id: Mock
) -> None:
    stream_id = uuid4()
    failure = FailureDetails(reason="TEST_FIND_STREAM_FAILS")
    find_stream_by_stream_id.return_value = Failure(failure)

    actual = get_stream_details_use_case(stream_id)

    find_stream_by_stream_id.assert_called_once()
    find_stream_by_stream_id.assert_called_with(stream_id)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), FailureDetails)
    assert failure == actual.failure()


def test_should_return_failure_when_find_projects_by_stream_fails(
    get_stream_details_use_case: GetStreamDetailsUseCase,
    find_stream_by_stream_id: Mock,
    find_projects_by_stream: Mock,
) -> None:
    stream_id = uuid4()
    stream = Stream(
        stream_id=stream_id,
        name="TEST_STREAM",
        source_type=SourceType.STREAM,
        source_name="OTHER_STREAM_TEST",
    )
    failure = FailureDetails(reason="TEST_FIND_PROJECTS_FAILS")

    find_stream_by_stream_id.return_value = Success(Maybe.from_value(stream))
    find_projects_by_stream.return_value = Failure(failure)

    actual = get_stream_details_use_case(stream_id)

    find_projects_by_stream.assert_called_once()
    find_projects_by_stream.assert_called_with(stream)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), FailureDetails)
    assert failure == actual.failure()


def test_should_return_failure_when_get_stream_by_name_fails(
    get_stream_details_use_case: GetStreamDetailsUseCase,
    find_stream_by_stream_id: Mock,
    find_projects_by_stream: Mock,
    get_stream_by_name: Mock,
) -> None:
    stream_id = uuid4()
    stream = Stream(
        stream_id=stream_id,
        name="TEST_STREAM",
        source_type=SourceType.STREAM,
        source_name="OTHER_STREAM_TEST",
    )
    project_list = [
        Project(
            project_id=uuid4(),
            title="Project One",
            created_at=datetime.now(),
            status=ProjectStatus.ACTIVE,
        ),
        Project(
            project_id=uuid4(),
            title="Project Two",
            created_at=datetime.now(),
            status=ProjectStatus.INACTIVE,
        ),
    ]
    failure = FailureDetails(reason="TEST_FIND_STREAM_BY_NAME_FAILS")

    find_stream_by_stream_id.return_value = Success(Maybe.from_value(stream))
    find_projects_by_stream.return_value = Success(project_list)
    get_stream_by_name.return_value = Failure(failure)

    actual = get_stream_details_use_case(stream_id)

    get_stream_by_name.assert_called_once()
    get_stream_by_name.assert_called_with(stream.name)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), FailureDetails)
    assert failure == actual.failure()
