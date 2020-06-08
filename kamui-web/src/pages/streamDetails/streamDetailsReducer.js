import { STREAM_DETAILS_DATA_RECEIVED, STREAM_DETAILS_REQUEST_SENT } from "./actionTypes";

const INITIAL_STATE = {
  streamDetails: null,
  waitingResponse: false,
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case STREAM_DETAILS_REQUEST_SENT:
      return { ...state, waitingResponse: true }
    case STREAM_DETAILS_DATA_RECEIVED:
      return { ...state, streamDetails: action.payload, waitingResponse: false }
    default:
      return state
  }
}