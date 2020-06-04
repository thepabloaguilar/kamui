import {
  CREATE_NEW_STREAM_FROM_STREAM_DATA_RECEIVED,
  CREATE_NEW_STREAM_FROM_STREAM_REQUEST_SENT,
  KSQL_STREAM_DETAIL_DATA_RECEIVED,
  KSQL_STREAM_DETAIL_REQUEST_SENT,
  KSQL_STREAM_LIST_DATA_RECEIVED,
  KSQL_STREAM_LIST_REQUEST_SENT
} from "./actionTypes";
import { createStream, getKSQLStreamDetail, getKSQLStreams } from "../../gateways/Streams";

export const streamListRequestSent = () => ({
  type: KSQL_STREAM_LIST_REQUEST_SENT,
})

export const ksqlStreamListDataReceived = (value) => ({
  type: KSQL_STREAM_LIST_DATA_RECEIVED,
  payload: value,
})

export const ksqlStreamDetailRequestSent = () => ({
  type: KSQL_STREAM_DETAIL_REQUEST_SENT,
})

export const ksqlStreamDetailDataReceived = (value) => ({
  type: KSQL_STREAM_DETAIL_DATA_RECEIVED,
  payload: value,
})

export const createNewStreamFromStreamRequestSent = () => ({
  type: CREATE_NEW_STREAM_FROM_STREAM_REQUEST_SENT,
})

export const createNewStreamFromStreamDataReceived = (value) => ({
  type: CREATE_NEW_STREAM_FROM_STREAM_DATA_RECEIVED,
  payload: value,
})

export function getStreamListAction() {
  return (dispatch) => {
    dispatch(streamListRequestSent())
    return getKSQLStreams()
      .then(({ data }) => {
        dispatch(ksqlStreamListDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}

export function getKSQLStreamDetailAction(streamName) {
  return (dispatch) => {
    dispatch(ksqlStreamDetailRequestSent())
    return getKSQLStreamDetail(streamName)
      .then(({ data }) => {
        dispatch(ksqlStreamDetailDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}

export function createStreamAction(payload) {
  return (dispatch) => {
    dispatch(createNewStreamFromStreamRequestSent())
    return createStream(payload)
      .then(({ data }) => {
        dispatch(createNewStreamFromStreamDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}