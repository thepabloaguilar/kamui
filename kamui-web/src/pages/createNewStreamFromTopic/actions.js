import {
  CREATE_NEW_STREAM_FROM_TOPIC_DATA_RECEIVED,
  CREATE_NEW_STREAM_FROM_TOPIC_REQUEST_SENT,
  TOPIC_LIST_DATA_RECEIVED,
  TOPIC_LIST_REQUEST_SENT,
  TOPIC_SCHEMA_DATA_RECEIVED,
  TOPIC_SCHEMA_REQUEST_SENT
} from "./actionTypes";
import { createStream } from "../../gateways/Streams";
import { getTopics, getTopicSchema } from "../../gateways/Topics";

export const topicListRequestSent = () => ({
  type: TOPIC_LIST_REQUEST_SENT,
})

export const topicListDataReceived = (value) => ({
  type: TOPIC_LIST_DATA_RECEIVED,
  payload: value,
})

export const topicSchemaRequestSent = () => ({
  type: TOPIC_SCHEMA_REQUEST_SENT,
})

export const topicSchemaDataReceived = (value) => ({
  type: TOPIC_SCHEMA_DATA_RECEIVED,
  payload: value,
})

export const createNewStreamFromTopicRequestSent = () => ({
  type: CREATE_NEW_STREAM_FROM_TOPIC_REQUEST_SENT,
})

export const createNewStreamFromTopicDataReceived = (value) => ({
  type: CREATE_NEW_STREAM_FROM_TOPIC_DATA_RECEIVED,
  payload: value,
})

export function getTopicList() {
  return (dispatch) => {
    dispatch(topicListRequestSent())
    return getTopics()
      .then(({ data }) => {
        dispatch(topicListDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}

export function getTopicSchemaAction(topicName) {
  return (dispatch) => {
    dispatch(topicSchemaRequestSent())
    return getTopicSchema(topicName)
      .then(({ data }) => {
        dispatch(topicSchemaDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}

export function createStreamAction(payload) {
  return (dispatch) => {
    dispatch(createNewStreamFromTopicRequestSent())
    return createStream(payload)
      .then(({ data }) => {
        dispatch(createNewStreamFromTopicDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}