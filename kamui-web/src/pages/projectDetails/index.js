import React, { Fragment, useEffect } from "react";
import DagreGraph from "dagre-d3-react";

import SiteWrapper from "../../SiteWrapper";
import {
  Button,
  Card,
  Container,
  Dimmer,
  Grid,
  Header,
  Page,
  Table,
} from "tabler-react";
import { bindActionCreators } from "redux";
import { getProjectDetailsAction } from "./actions";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

const createNode = (stream) => {
  return {
    id: stream.name,
    label:
      "<div class=streamBox>" +
      "<span class=status></span>" +
      `<span class=name>${stream.name}</span>` +
      "</div>",
    labelType: "html",
    class: stream.source_type.toLowerCase(),
    config: {
      rx: 5,
      ry: 5,
      padding: 0
    }
  }
}

const createLink = (stream) => {
  return {source: stream.source_name, target: stream.name}
}

function ProjectDetails(props) {
  const { projectId } = props.match.params;
  const { projectDetails, waitingResponse } = props;
  useEffect(() => {
    props.getProjectDetailsAction(projectId)
  }, [props.getProjectDetailsAction])

  let projectName = ''
  let nodes = []
  let links = []

  if (projectDetails) {
    let sourceNames = projectDetails.streams.map(stream => stream.name)

    projectName = projectDetails.project.title
    nodes = projectDetails.streams.map(createNode)
    links = projectDetails.streams
      .filter(stream => sourceNames.includes(stream.source_name))
      .map(createLink)
  }

  return (
    <SiteWrapper>
      <Page.Content title={projectName} subTitle="Your project details">
        <Container>
          <Grid.Row cards>
            <Grid.Col>
              <Card title="Project Information" isCollapsible isCollapsed>
                {
                  projectDetails && !waitingResponse
                    ?
                    <Card.Body>
                      <Fragment>
                        <Header.H6>Project ID</Header.H6>
                        <p>{projectDetails.project.project_id}</p>
                      </Fragment>
                      <Grid.Row>
                        <Grid.Col width={6}>
                          <Header.H6>Created At</Header.H6>
                          <p>{
                            new Date(projectDetails.project.created_at * 1000)
                              .toLocaleString("en-US")
                              .replace(',', '')
                          }</p>
                        </Grid.Col>
                        <Grid.Col width={6}>
                          <Header.H6>Status</Header.H6>
                          <p>{projectDetails.project.status}</p>
                        </Grid.Col>
                      </Grid.Row>
                    </Card.Body>
                    :
                    <Card.Body>
                      <Dimmer active loader>
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aperiam deleniti
                        fugit incidunt, iste, itaque minima neque pariatur perferendis sed
                        suscipit velit vitae voluptatem. A consequuntur, deserunt eaque error
                        nulla temporibus!
                      </Dimmer>
                    </Card.Body>
                }
              </Card>
            </Grid.Col>
          </Grid.Row>
          <Grid.Row cards>
            <Grid.Col width={12}>
              <Card
                title="Streams Graph"
                className="streamsGraph"
                options={
                  <Button RootComponent={Link} to={`/projects/${projectId}/streams/create`} icon="plus" color="primary" outline>
                    Add new stream
                  </Button>
                }
              >
                <DagreGraph
                  nodes={nodes}
                  links={links}
                  animate={500}
                  fitBoundaries
                  zoomable
                  config={{
                    nodesep: 70,
                    ranksep: 50,
                    rankdir: "LR",
                    marginx: 20,
                    marginy: 20,
                  }}
                />
              </Card>
              <Grid.Row cards>
                <Grid.Col width={12}>
                  <Card title="Project Streams" isCollapsible isCollapsed>
                    <Card.Body>
                      <Table
                        highlightRowOnHover={true}
                        responsive={true}
                        className="card-table table-vcenter text-nowrap"
                      >
                        <Table.Header>
                          <Table.Row>
                            <Table.ColHeader>Stream ID</Table.ColHeader>
                            <Table.ColHeader>Stream Name</Table.ColHeader>
                          </Table.Row>
                        </Table.Header>
                        <Table.Body>
                          {
                            projectDetails
                              ?
                              projectDetails.streams.map(stream =>
                                <Table.Row key={stream.stream_id}>
                                  <Table.Col>{stream.stream_id.slice(0, 8)}</Table.Col>
                                  <Table.Col>
                                    <Link to={`/streams/${stream.stream_id}`}>
                                      {stream.name}
                                    </Link>
                                  </Table.Col>
                                </Table.Row>
                              )
                              :
                              null
                          }
                        </Table.Body>
                      </Table>
                    </Card.Body>
                  </Card>
                </Grid.Col>
              </Grid.Row>
            </Grid.Col>
          </Grid.Row>
        </Container>
      </Page.Content>
    </SiteWrapper>
  )
}

const mapStateToProps = state => ({
  projectDetails: state.projectDetailsState.projectDetails,
  waitingResponse: state.projectDetailsState.waitingResponse,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getProjectDetailsAction,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(ProjectDetails);