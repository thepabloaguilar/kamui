import {
  ERROR_ON_CREATING_PROJECT,
  CREATE_PROJECT_FORM_SENT,
  PROJECT_CREATED_SUCCESSFULLY, CLEAN_UP_STATE_CREATE_PROJECT
} from "./actionTypes";
import { createProject } from "../../gateways/Projects";

export const createProjectFormSent = () => ({
  type: CREATE_PROJECT_FORM_SENT,
})

export const projectCreatedSuccessfully = (value) => ({
  type: PROJECT_CREATED_SUCCESSFULLY,
  payload: value,
})

export const errorOnCreatingProject = (value) => ({
  type: ERROR_ON_CREATING_PROJECT,
  payload: value,
})

export const cleanUpStateCreateProject = () => ({
  type: CLEAN_UP_STATE_CREATE_PROJECT,
})

export function createProjectAction(payload) {
  return (dispatch) => {
    dispatch(createProjectFormSent())
    return createProject(payload)
      .then(({ data }) => {
        dispatch(projectCreatedSuccessfully(data))
      })
      .catch(err => {
        dispatch(errorOnCreatingProject(err))
      })
  }
}

export function cleanUpState() {
  return (dispatch) => {
    dispatch(cleanUpStateCreateProject())
  }
}
