# TODO: Make register automatic
from punq import Container

from kamui.core.usecase.project.create_new_project import (
    CreateNewProjectUsecase,
    CreateNewProject,
)
from kamui.core.usecase.project.get_projects_list import (
    GetProjectsListUsecase,
    GetProjectsList,
)
from kamui.core.usecase.topic.get_available_topic_names import (
    GetAvailableTopicNamesUsecase,
    GetTopicNames,
)
from kamui.core.usecase.topic.get_topic_schema import (
    GetTopicSchemaUsecase,
    GetTopicSchema,
    GetTopicSchemaVersions,
)
from kamui.core.usecase.stream.create_new_stream_from_topic import (
    CreateNewStreamFromTopicUsecase,
    CreateStreamFromKafkaTopic,
)
from kamui.dataproviders.database.project.repository import (
    CreateNewProjectRepository,
    GetProjectsListRepository,
)
from kamui.dataproviders.rest.stream.repository import (
    CreateStreamFromKafkaTopicRepository,
)
from kamui.dataproviders.rest.topic.repository import (
    GetTopicNamesRepository,
    GetTopicSchemaRepository,
    GetTopicSchemaVersionsRepository,
)

di_container = Container()

# Dependencies
di_container.register(CreateNewProject, CreateNewProjectRepository)
di_container.register(GetProjectsList, GetProjectsListRepository)
di_container.register(GetTopicNames, GetTopicNamesRepository)
di_container.register(GetTopicSchema, GetTopicSchemaRepository)
di_container.register(GetTopicSchemaVersions, GetTopicSchemaVersionsRepository)
di_container.register(CreateStreamFromKafkaTopic, CreateStreamFromKafkaTopicRepository)

# Usecases
di_container.register(CreateNewProjectUsecase)
di_container.register(GetProjectsListUsecase)
di_container.register(GetAvailableTopicNamesUsecase)
di_container.register(GetTopicSchemaUsecase)
di_container.register(CreateNewStreamFromTopicUsecase)
