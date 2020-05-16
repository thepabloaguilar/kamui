import service from "./axios";

const headers = () => ({
  'content-type': 'application/json',
  'Accept': 'application/json',
})

export const getProjects = () =>
  service.axios.get('/projects', { headers: headers() })