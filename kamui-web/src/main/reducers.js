import { combineReducers } from "redux";
import ProjectsReducer from '../pages/projects/projectsReducer';
import CreateProjectReducer from "../pages/createProject/createProjectReducer";
import ProjectDetailsReducer from "../pages/projectDetails/projectDetailsReducer";
import CreateNewStreamFromTopicReducer from "../pages/createNewStreamFromTopic/createNewStreamFromTopicReducer";
import CreateNewStreamFromStreamReducer from "../pages/createNewStreamFromStream/createNewStreamFromStreamReducer";
import StreamsReducer from "../pages/streams/streamsReducer";

const rootReducer = combineReducers({
  projectsState: ProjectsReducer,
  createProjectState: CreateProjectReducer,
  projectDetailsState: ProjectDetailsReducer,
  createNewStreamFromTopicState: CreateNewStreamFromTopicReducer,
  createNewStreamFromStreamState: CreateNewStreamFromStreamReducer,
  streamsState: StreamsReducer,
})

export default rootReducer