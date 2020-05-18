import { PROJECT_DETAILS_DATA_RECEIVED, PROJECT_DETAILS_REQUEST_SENT } from "./actionTypes";
import { getProjectDetails } from "../../gateways/Projects";

export const projectDetailsRequestSent = () => ({
  type: PROJECT_DETAILS_REQUEST_SENT,
})

export const projectDetailsDataReceived = (value) => ({
  type: PROJECT_DETAILS_DATA_RECEIVED,
  payload: value,
})

export function getProjectDetailsAction(projectId) {
  return (dispatch) => {
    dispatch(projectDetailsRequestSent())
    return getProjectDetails(projectId)
      .then(({ data }) => {
        dispatch(projectDetailsDataReceived(data))
      })
      .catch(err => {
        console.log(err)
      })
  }
}