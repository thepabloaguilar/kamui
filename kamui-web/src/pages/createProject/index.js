import React, { useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from 'yup';

import SiteWrapper from "../../SiteWrapper";
import { Alert, Button, Card, Form, Grid, Page } from "tabler-react";
import { Link } from "react-router-dom";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { cleanUpState, createProjectAction } from "./actions";


function CreateProject(props) {
  useEffect(() => {
    props.cleanUpState()
  }, [props.cleanUpState])
  const { history, wasFormSent, successPayload, hasError } = props;

  if (successPayload)
    history.push(`/projects/${successPayload.project_id}`)

  const projectForm = useFormik({
    initialValues: {
      title: '',
    },
    validationSchema: Yup.object({
      title: Yup.string()
        .required('Required')
    }),
    onSubmit: values => {
      console.log(values)
      props.createProjectAction(values)
    }
  })

  return (
    <SiteWrapper>
      <Page.Content title='Create your project'>
        <Grid.Row cards>
          <Grid.Col width={12}>
            <Card>
              <Card.Body>
                {
                  hasError
                  ?
                  <Alert type="danger" icon="alert-triangle">
                    An error occurred.
                  </Alert>
                  :
                  null
                }
                <Form onSubmit={projectForm.handleSubmit}>
                  <Form.Group label='Project Title' isRequired>
                    <Form.Input
                      id='title'
                      name='title'
                      type='text'
                      placeholder='Enter the project title'
                      value={projectForm.values.title}
                      onChange={projectForm.handleChange}
                      feedback='Project title is required'
                      invalid={projectForm.touched.title && projectForm.errors.title}
                    />
                  </Form.Group>
                  <Button.List className="mt-4" align="right">
                    <Button RootComponent={Link} to='/projects' color='secondary'>Cancel</Button>
                    {
                      wasFormSent
                      ?
                        <Button loading color='primary' className='ml-auto'>Create Project</Button>
                      :
                      <Button type='submit' color='primary' className='ml-auto' outline>
                        Create Project
                      </Button>
                    }
                  </Button.List>
                </Form>
              </Card.Body>
            </Card>
          </Grid.Col>
        </Grid.Row>
      </Page.Content>
    </SiteWrapper>
  )
}

const mapStateToProps = state => ({
  wasFormSent: state.createProjectState.wasFormSent,
  successPayload: state.createProjectState.successPayload,
  hasError: state.createProjectState.hasError,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    createProjectAction,
    cleanUpState,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(CreateProject);