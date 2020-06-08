import React, { useEffect } from "react";
import SiteWrapper from "../../SiteWrapper";
import { Card, Dimmer, Grid, Header, Page, Table, Text } from "tabler-react";
import { Link } from "react-router-dom";
import { bindActionCreators } from "redux";
import { getStreamDetailsAction } from "./actions";
import { connect } from "react-redux";

const CardWithLoading = ({isLoading = false, className, HeaderType, header, text}) => {
  return (
    <Card>
      <Card.Body className={className}>
        {
          !isLoading
            ?
            <div>
              <HeaderType className="m-2">{header}</HeaderType>
              <Text color="muted" className="mb-4">{text}</Text>
            </div>
            :
            <Dimmer active loader>
              <HeaderType className="m-2">HEADER</HeaderType>
              <Text color="muted" className="mb-4">Lorem_ipsum_dolor_sit</Text>
            </Dimmer>
        }
      </Card.Body>
    </Card>
  )
}

function StreamDetails(props) {
  const { streamId } = props.match.params;
  const { streamDetails, waitingResponse } = props;

  useEffect(() => {
    props.getStreamDetailsAction(streamId)
  }, [props.getStreamDetailsAction])

  let streamName = '';
  let sourceName = '';
  let sourceType = '';
  let format = '';

  if (streamDetails) {
    streamName = streamDetails.stream.name;
    sourceName = streamDetails.stream.source_name;
    sourceType = streamDetails.stream.source_type;
    format = streamDetails.ksql_stream_detailed.format;
  }

  return (
    <SiteWrapper>
      <Page.Content title={streamName} subTitle="Stream details">
        <Grid.Row cards>
          <Grid.Col width={6} lg={3}>
            <CardWithLoading
              isLoading={!streamDetails && waitingResponse}
              className="p-4 text-center"
              HeaderType={Header.H4}
              header={streamName}
              text="Stream Name"
            />
          </Grid.Col>
          <Grid.Col width={6} lg={3}>
            <CardWithLoading
              isLoading={!streamDetails && waitingResponse}
              className="p-4 text-center"
              HeaderType={Header.H4}
              header={sourceName}
              text="Source Name"
            />
          </Grid.Col>
          <Grid.Col width={6} lg={3}>
            <CardWithLoading
              isLoading={!streamDetails && waitingResponse}
              className="p-3 text-center"
              HeaderType={Header.H3}
              header={sourceType}
              text="Source Type"
            />
          </Grid.Col>
          <Grid.Col width={6} lg={3}>
            <CardWithLoading
              isLoading={!streamDetails && waitingResponse}
              className="p-3 text-center"
              HeaderType={Header.H3}
              header={format}
              text="Format"
            />
          </Grid.Col>
        </Grid.Row>
        <Grid.Row cards={true}>
          <Grid.Col width={6}>
            <Card title="Stream Schema / From Schema Registry">
              <Table
                  cards={true}
                  striped
                  responsive={true}
                  className="card-table table-vcenter text-nowrap"
                >
                <Table.Header>
                  <Table.Row>
                    <Table.ColHeader>Field Name</Table.ColHeader>
                    <Table.ColHeader>Field Type</Table.ColHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {
                    streamDetails
                      ?
                      streamDetails.ksql_stream_detailed.fields.map(field =>
                        <Table.Row key={field.name}>
                          <Table.Col>
                            {field.name}
                          </Table.Col>
                          <Table.Col>
                            {field.schema.type}
                          </Table.Col>
                        </Table.Row>
                      )
                      :
                      null
                  }
                </Table.Body>
              </Table>
            </Card>
          </Grid.Col>
          <Grid.Col width={6}>
            <Card title="Projects using this stream">
              <Table
                  cards={true}
                  striped
                  responsive={true}
                  className="card-table table-vcenter text-nowrap"
                >
                <Table.Header>
                  <Table.Row>
                    <Table.ColHeader>Title</Table.ColHeader>
                    <Table.ColHeader>Status</Table.ColHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {
                    streamDetails
                      ?
                      streamDetails.projects.map(project =>
                        <Table.Row key={project.project_id}>
                          <Table.Col>
                            <Link to={`/projects/${project.project_id}`}>
                              {project.title}
                            </Link>
                          </Table.Col>
                          <Table.Col>
                            <span className="status-icon bg-success"/> {project.status}
                          </Table.Col>
                        </Table.Row>
                      )
                      :
                      null
                  }
                </Table.Body>
              </Table>
            </Card>
          </Grid.Col>
        </Grid.Row>
      </Page.Content>
    </SiteWrapper>
  );
}

const mapStateToProps = state => ({
  streamDetails: state.streamDetailsState.streamDetails,
  waitingResponse: state.streamDetailsState.waitingResponse,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getStreamDetailsAction,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(StreamDetails);