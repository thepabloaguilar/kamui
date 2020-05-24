import service from "./axios";

const headers = () => ({
  'content-type': 'application/json',
  'Accept': 'application/json',
})

export const createStream = (payload) =>
  service.axios.post('/streams', payload, { headers: headers() })