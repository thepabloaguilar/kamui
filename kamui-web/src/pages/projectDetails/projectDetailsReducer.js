import { PROJECT_DETAILS_DATA_RECEIVED, PROJECT_DETAILS_REQUEST_SENT } from "./actionTypes";

const INITIAL_STATE ={
  projectDetails: null,
  waitingResponse: false,
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case PROJECT_DETAILS_REQUEST_SENT:
      return { ...state, waitingResponse: true }
    case PROJECT_DETAILS_DATA_RECEIVED:
      return { ...state, projectDetails: action.payload, waitingResponse: false }
    default:
      return state
  }
}