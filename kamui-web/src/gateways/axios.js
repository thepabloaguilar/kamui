import axios from 'axios'

import urlBuilder from "./helpers/UrlBuilder";

let service = { axios }

export const refreshConfiguration = (config) => {
  service.axios = axios.create({
    baseURL: urlBuilder(config)
  })
}

export default service