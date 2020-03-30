from punq import Container

from kamui.core.usecase.project.create_new_project import (
    CreateNewProjectUsecase,
    CreateNewProject,
)
from kamui.core.usecase.project.get_projects_list import (
    GetProjectsListUsecase,
    GetProjectsList,
)
from kamui.dataproviders.database.project.repository import (
    CreateNewProjectRepository,
    GetProjectsListRepository,
)

di_container = Container()

# Dependencies
di_container.register(CreateNewProject, CreateNewProjectRepository)
di_container.register(GetProjectsList, GetProjectsListRepository)

# Usecases
di_container.register(CreateNewProjectUsecase)
di_container.register(GetProjectsListUsecase)
