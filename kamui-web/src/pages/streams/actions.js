import { getStreams } from "../../gateways/Streams";
import { STREAM_LIST_DATA_RECEIVED, STREAM_LIST_REQUEST_SENT } from "./actionTypes";

export const streamsListRequestSent = () => ({
  type: STREAM_LIST_REQUEST_SENT,
})

export const streamListDataReceived = value => ({
  type: STREAM_LIST_DATA_RECEIVED,
  payload: value,
})

export function getStreamsAction() {
  return (dispatch) => {
    dispatch(streamsListRequestSent())
    return getStreams()
      .then(({ data }) => {
        dispatch(streamListDataReceived(data))
      })
      .catch(err => {
        console.log(err)
      })
  }
}