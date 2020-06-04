import React, { useEffect } from "react";
import SiteWrapper from "../../SiteWrapper";
import { bindActionCreators } from "redux";
import { getStreamsAction } from "./actions";
import { connect } from "react-redux";
import { Card, Grid, Page, Table, Text } from "tabler-react";

function Streams(props) {
  useEffect(() => {
    props.getStreamsAction();
  }, [props.getStreamsAction])

  return (
    <SiteWrapper>
      <Page.Content title="Streams" subTitle="You can manage all streams">
        <Grid.Row cards={true}>
          <Grid.Col width={12}>
            <Card title="All Streams">
              <Table
                  cards={true}
                  highlightRowOnHover={true}
                  responsive={true}
                  className="card-table table-vcenter text-nowrap"
                >
                <Table.Header>
                  <Table.Row>
                    <Table.ColHeader>ID</Table.ColHeader>
                    <Table.ColHeader>Name</Table.ColHeader>
                    <Table.ColHeader>Source Type</Table.ColHeader>
                    <Table.ColHeader>Source Name</Table.ColHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {props.streams.map((stream) =>
                    <Table.Row key={stream.stream_id}>
                      <Table.Col>
                        <Text RootComponent="span" muted>
                          {stream.stream_id.slice(0, 8)}
                        </Text>
                      </Table.Col>
                      <Table.Col>
                        <a href={`/streams/${stream.stream_id}`} className="text-inherit">
                          {stream.name}
                        </a>
                      </Table.Col>
                      <Table.Col>{stream.source_type}</Table.Col>
                      <Table.Col>{stream.source_name}</Table.Col>
                    </Table.Row>
                  )}
                </Table.Body>
              </Table>
            </Card>
          </Grid.Col>
        </Grid.Row>
      </Page.Content>
    </SiteWrapper>
  )
}

const mapStateToProps = state => ({
  streams: state.streamsState.streams,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getStreamsAction,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(Streams);