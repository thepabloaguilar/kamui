import service from "./axios";

const headers = () => ({
  'content-type': 'application/json',
  'Accept': 'application/json',
})

export const createStream = (payload) =>
  service.axios.post('/streams', payload, { headers: headers() })

export const getStreams = () =>
  service.axios.get('/streams', { headers: headers() })

export const getStreamDetail = (streamName) =>
  service.axios.get(`/streams/${streamName}`, { headers: headers() })