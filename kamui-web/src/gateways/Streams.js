import service from "./axios";

const headers = () => ({
  'content-type': 'application/json',
  'Accept': 'application/json',
})

export const createStream = (payload) =>
  service.axios.post('/streams', payload, { headers: headers() })

export const getStreams = () =>
  service.axios.get('/streams', { headers: headers() })

export const getKSQLStreams = () =>
  service.axios.get('/ksql-streams', { headers: headers() })

export const getKSQLStreamDetail = (streamName) =>
  service.axios.get(`/ksql-streams/${streamName}`, { headers: headers() })