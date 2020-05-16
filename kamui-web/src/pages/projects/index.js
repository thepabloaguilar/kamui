import React, { useEffect } from "react";
import { connect } from 'react-redux';
import { bindActionCreators } from "redux";
import { getAllProjects } from "./actions";

import SiteWrapper from "../../SiteWrapper";
import {Grid, Page, Table, Card, Text, Button} from "tabler-react";

function Projects(props) {
  useEffect(() => {
    props.getAllProjects();
  }, [props.getAllProjects])

  return (
    <SiteWrapper>
      <Page.Content title="Projects" subTitle="You can manage all projects">
        <Grid.Row cards={true}>
          <Grid.Col width={12}>
            <Card
              title="All Projects"
              options={
                <Button icon="plus" color="primary" outline>
                  Add new
                </Button>
              }
            >
              <Table
                  cards={true}
                  highlightRowOnHover={true}
                  responsive={true}
                  className="card-table table-vcenter text-nowrap"
                >
                <Table.Header>
                  <Table.Row>
                    <Table.ColHeader>ID</Table.ColHeader>
                    <Table.ColHeader>Title</Table.ColHeader>
                    <Table.ColHeader>Created At</Table.ColHeader>
                    <Table.ColHeader>Status</Table.ColHeader>
                  </Table.Row>
                </Table.Header>
                <Table.Body>
                  {props.projects.map((project) =>
                    <Table.Row key={project.project_id}>
                      <Table.Col>
                        <Text RootComponent="span" muted>
                          {project.project_id.slice(0, 8)}
                        </Text>
                      </Table.Col>
                      <Table.Col>
                        <a href={`/projects/${project.project_id}`} className="text-inherit">
                          {project.title}
                        </a>
                      </Table.Col>
                      <Table.Col>{project.created_at}</Table.Col>
                      <Table.Col>
                        <span className="status-icon bg-success" /> {project.status}
                      </Table.Col>
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
  projects: state.projectsState.projects,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getAllProjects,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
