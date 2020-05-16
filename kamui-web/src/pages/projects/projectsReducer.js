import {PROJECTS_DATA_RECEIVED} from "./actionTypes";

const INITIAL_STATE = {
  projects: [],
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case PROJECTS_DATA_RECEIVED:
      return { ...state, projects: action.payload }
    default:
      return state
  }
}