import { refreshConfiguration } from "./gateways/axios";
import retrieveEnvConfig from "./gateways/helpers/retrieveEnvConfig";

require('dotenv').config()

const loadConfig = () => {
  const env = {
    NODE_ENV: 'production',
    API_PROTOCOL: 'http',
    API_HOSTNAME: process.env.REACT_APP_API_HOSTNAME,
  }
  Object.keys(env).forEach((key) => {
    console.log(env[key])
    window.localStorage.setItem(key, env[key])
  })
}
refreshConfiguration(retrieveEnvConfig())

export default loadConfig