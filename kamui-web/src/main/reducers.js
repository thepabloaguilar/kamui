import { combineReducers } from "redux";
import ProjectsReducer from '../pages/projects/projectsReducer';
import CreateProjectReducer from "../pages/create_project/createProjectReducer";
import ProjectDetailsReducer from "../pages/project_details/projectDetailsReducer";
import CreateNewStreamFromTopicReducer from "../pages/create_new_stream_from_topic/createNewStreamFromTopicReducer";

const rootReducer = combineReducers({
  projectsState: ProjectsReducer,
  createProjectState: CreateProjectReducer,
  projectDetailsState: ProjectDetailsReducer,
  createNewStreamFromTopicState: CreateNewStreamFromTopicReducer,
})

export default rootReducer