import service from "./axios";

const headers = () => ({
  'content-type': 'application/json',
  'Accept': 'application/json',
})

export const getTopics = () =>
  service.axios.get('/topics', {headers: headers()})

export const getTopicSchema = (topicName) =>
  service.axios.get(`/topics/${topicName}/schema`, {headers: headers()})