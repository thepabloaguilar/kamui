import {
  CREATE_NEW_STREAM_FROM_STREAM_DATA_RECEIVED,
  CREATE_NEW_STREAM_FROM_STREAM_REQUEST_SENT,
  KSQL_STREAM_DETAIL_DATA_RECEIVED,
  KSQL_STREAM_DETAIL_REQUEST_SENT,
  KSQL_STREAM_LIST_DATA_RECEIVED,
  KSQL_STREAM_LIST_REQUEST_SENT
} from "./actionTypes";

const INITIAL_STATE = {
  waitingStreamList: false,
  streamList: [],
  waitingStreamDetail: false,
  streamDetail: null,
  waitingSubmitFormResponse: false,
  submitFormResponse: null,
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case KSQL_STREAM_LIST_REQUEST_SENT:
      return { ...state, waitingStreamList: true }
    case KSQL_STREAM_LIST_DATA_RECEIVED:
      return { ...state, streamList: action.payload, waitingStreamList: false }
    case KSQL_STREAM_DETAIL_REQUEST_SENT:
      return { ...state, waitingStreamDetail: true }
    case KSQL_STREAM_DETAIL_DATA_RECEIVED:
      return { ...state, streamDetail: action.payload, waitingStreamDetail: false }
    case CREATE_NEW_STREAM_FROM_STREAM_REQUEST_SENT:
      return { ...state, waitingSubmitFormResponse: true }
    case CREATE_NEW_STREAM_FROM_STREAM_DATA_RECEIVED:
      return { ...state, submitFormResponse: action.payload, waitingSubmitFormResponse: false }
    default:
      return state
  }
}