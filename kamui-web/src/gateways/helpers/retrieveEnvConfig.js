const retrieveEnvConfig = () => {
  const urlEnv = window.localStorage

  const envProtocol = urlEnv.API_PROTOCOL

  const protocol = envProtocol === 'auto' //eslint-disable-next-line
    ? location.protocol.slice(0, -1)
    : envProtocol === 'http' || envProtocol === 'https'
      ? envProtocol
      : 'https'

  const hostname = urlEnv.API_HOSTNAME
  const version = urlEnv.API_VERSION

  return {
    protocol,
    hostname,
    version
  }
}

export default retrieveEnvConfig