import {getProjects} from "../../gateways/Projects";
import {PROJECTS_DATA_RECEIVED, PROJECTS_REQUEST_SENT} from "./actionTypes";

export const getProjectsRequestSent = () => ({
  type: PROJECTS_REQUEST_SENT,
})

export const projectsDataReceived = value => ({
  type: PROJECTS_DATA_RECEIVED,
  payload: value,
})

export function getAllProjects() {
  return (dispatch) => {
    dispatch(getProjectsRequestSent())
    return getProjects()
      .then(({ data }) => {
        dispatch(projectsDataReceived(data))
      })
      .catch(err => {
        console.log(err)
      })
  }
}