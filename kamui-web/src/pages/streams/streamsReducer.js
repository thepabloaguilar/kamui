import { STREAM_LIST_DATA_RECEIVED } from "./actionTypes";

const INITIAL_STATE = {
  streams: [],
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case STREAM_LIST_DATA_RECEIVED:
      return { ...state, streams: action.payload }
    default:
      return state
  }
}