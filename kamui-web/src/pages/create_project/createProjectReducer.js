import {
  CLEAN_UP_STATE_CREATE_PROJECT,
  CREATE_PROJECT_FORM_SENT,
  ERROR_ON_CREATING_PROJECT,
  PROJECT_CREATED_SUCCESSFULLY
} from "./actionTypes";

const INITIAL_STATE = {
  wasFormSent: false,
  successPayload: null,
  hasError: false,
}

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case CREATE_PROJECT_FORM_SENT:
      return { ...state, wasFormSent: true }
    case PROJECT_CREATED_SUCCESSFULLY:
      return {
        ...state,
        wasFormSent: false,
        successPayload: action.payload,
        hasError: false,
      }
    case ERROR_ON_CREATING_PROJECT:
      return {
        ...state,
        wasFormSent: false,
        hasError: true,
      }
    case CLEAN_UP_STATE_CREATE_PROJECT:
      return INITIAL_STATE
    default:
      return state
  }
}