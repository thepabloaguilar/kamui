import { combineReducers } from "redux";
import ProjectsReducer from '../pages/projects/projectsReducer';
import CreateProjectReducer from "../pages/create_project/createProjectReducer";
import ProjectDetailsReducer from "../pages/project_details/projectDetailsReducer";

const rootReducer = combineReducers({
  projectsState: ProjectsReducer,
  createProjectState: CreateProjectReducer,
  projectDetailsState: ProjectDetailsReducer,
})

export default rootReducer