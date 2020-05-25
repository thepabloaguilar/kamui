import {
  CREATE_NEW_STREAM_FROM_STREAM_DATA_RECEIVED,
  CREATE_NEW_STREAM_FROM_STREAM_REQUEST_SENT,
  STREAM_DETAIL_DATA_RECEIVED,
  STREAM_DETAIL_REQUEST_SENT,
  STREAM_LIST_DATA_RECEIVED,
  STREAM_LIST_REQUEST_SENT
} from "./actionTypes";
import { createStream, getStreamDetail, getStreams } from "../../gateways/Streams";

export const streamListRequestSent = () => ({
  type: STREAM_LIST_REQUEST_SENT,
})

export const streamListDataReceived = (value) => ({
  type: STREAM_LIST_DATA_RECEIVED,
  payload: value,
})

export const streamDetailRequestSent = () => ({
  type: STREAM_DETAIL_REQUEST_SENT,
})

export const streamDetailDataReceived = (value) => ({
  type: STREAM_DETAIL_DATA_RECEIVED,
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
    return getStreams()
      .then(({ data }) => {
        dispatch(streamListDataReceived(data))
      })
      .catch(err => {
        console.log(err);
      })
  }
}

export function getStreamDetailAction(streamName) {
  return (dispatch) => {
    dispatch(streamDetailRequestSent())
    return getStreamDetail(streamName)
      .then(({ data }) => {
        dispatch(streamDetailDataReceived(data))
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