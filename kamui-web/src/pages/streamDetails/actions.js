import { STREAM_DETAILS_DATA_RECEIVED, STREAM_DETAILS_REQUEST_SENT } from "./actionTypes";
import { getStreamDetails } from "../../gateways/Streams";

export const streamDetailsRequestSent = () => ({
  type: STREAM_DETAILS_REQUEST_SENT,
})

export const streamDetailsDataReceived = (value) => ({
  type: STREAM_DETAILS_DATA_RECEIVED,
  payload: value,
})

export function getStreamDetailsAction(streamId) {
  return (dispatch) => {
    dispatch(streamDetailsRequestSent())
    return getStreamDetails(streamId)
      .then(({ data }) => {
        dispatch(streamDetailsDataReceived(data))
      })
      .catch(err => {
        console.log(err)
      })
  }
}