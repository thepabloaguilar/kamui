import { combineReducers } from "redux";
import ProjectsReducer from '../pages/projects/projectsReducer';

const rootReducer = combineReducers({
  projectsState: ProjectsReducer,
})

export default rootReducer