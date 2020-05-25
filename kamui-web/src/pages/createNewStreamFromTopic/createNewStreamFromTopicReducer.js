import {
  CREATE_NEW_STREAM_FROM_TOPIC_DATA_RECEIVED,
  CREATE_NEW_STREAM_FROM_TOPIC_REQUEST_SENT,
  TOPIC_LIST_DATA_RECEIVED,
  TOPIC_LIST_REQUEST_SENT,
  TOPIC_SCHEMA_DATA_RECEIVED,
  TOPIC_SCHEMA_REQUEST_SENT
} from "./actionTypes";

const INITIAL_STATE = {
  waitingTopicList: false,
  topicList: [],
  waitingTopicSchema: false,
  topicSchema: null,
  waitingSubmitFormResponse: false,
  submitFormResponse: null,
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case TOPIC_LIST_REQUEST_SENT:
      return { ...state, waitingTopicList: true }
    case TOPIC_LIST_DATA_RECEIVED:
      return { ...state, topicList: action.payload, waitingTopicList: false }
    case TOPIC_SCHEMA_REQUEST_SENT:
      return { ...state, waitingTopicSchema: true}
    case TOPIC_SCHEMA_DATA_RECEIVED:
      return { ...state, topicSchema: action.payload, waitingTopicSchema: false }
    case CREATE_NEW_STREAM_FROM_TOPIC_REQUEST_SENT:
      return { ...state, waitingSubmitFormResponse: true }
    case CREATE_NEW_STREAM_FROM_TOPIC_DATA_RECEIVED:
      return { ...state, submitFormResponse: action.payload, waitingSubmitFormResponse: false }
    default:
      return state
  }
}