const urlBuilder = ({ protocol = 'http', hostname, port, version }, endpointVersion) => {
  let baseUrl = `${protocol}://${hostname}`

  if (port) baseUrl += `:${port}/`

  let pathName = version ? `v${version}/` : ''

  if (endpointVersion === 'none')
    pathName = ''
  else if (endpointVersion)
    pathName = `v${endpointVersion}/`

  return baseUrl + pathName
}

export default urlBuilder