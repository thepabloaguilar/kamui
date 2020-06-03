import React, { useEffect } from "react";
import SiteWrapper from "../../SiteWrapper";
import { bindActionCreators } from "redux";
import { createStreamAction, getStreamDetailAction, getStreamListAction } from "./actions";
import { connect } from "react-redux";
import { Button, Card, Form, Grid, Page } from "tabler-react";
import Wizard from "../../components/wizard";
import * as Yup from "yup";
import CustomFormikField from "../../components/customFormikField";
import ReactSelectFormik from "../../components/reactSelectFormik";
import { FieldArray, useField, Form as FormikForm } from "formik";

const CustomFieldArray = ({fieldOptions, ...props }) => {
  const [field] = useField(props);

  const conditionsOptions = [
    { value: "=", label: "EQUAL" },
    { value: "!=", label: "DIFFERENT" },
    { value: ">", label: "GREATER THAN" },
    { value: ">=", label: "EQUAL OR GREATER THAN" },
    { value: "<", label: "LESS THAN" },
    { value: "<=", label: "EQUAL OR LESS THAN" }
  ]

  return (
    <FormikForm>
      <FieldArray
        {...field}
        render={arrayHelpers => (
          <div>
            {field.value && field.value.length > 0 ? (
              field.value.map((friend, index) => (
                <div key={index}>
                  <Grid.Row>
                    <Grid.Col width={4}>
                      <ReactSelectFormik
                        name={`${field.name}.${index}.field`}
                        options={fieldOptions}
                      />
                    </Grid.Col>
                    <Grid.Col width={3}>
                      <ReactSelectFormik
                        name={`${field.name}.${index}.condition`}
                        options={conditionsOptions}
                      />
                    </Grid.Col>
                    <Grid.Col width={3}>
                      <CustomFormikField RootComponent={Form.Input} name={`${field.name}.${index}.value`}/>
                    </Grid.Col>
                    <Grid.Col width={2}>
                      <Button.List>
                        <Button type='button' color='primary' onClick={() => arrayHelpers.remove(index)}
                                outline>-</Button>
                        <Button type='button' color='primary' onClick={() => arrayHelpers.insert(index + 1, '')}
                                outline>+</Button>
                      </Button.List>
                    </Grid.Col>
                  </Grid.Row>
                </div>
              ))
            ) : (
              <Button type='button' color='primary' onClick={() => arrayHelpers.push('')} outline>Add a filter</Button>
            )}
          </div>
        )}
      />
    </FormikForm>
  )
}

function CreateNewStreamFromStream(props) {
  useEffect(() =>{
    props.getStreamListAction()
  }, [props.getStreamListAction])

  const onSubmit = (values, actions) => {
    const { projectId } =  props.match.params;
    const payload = {
      "project_id": projectId,
      "stream_name": values.streamName,
      "fields": values.fields.map(field => ({ name: field.value.name, type: field.value.schema.type })),
      "source_name": values.sourceName.value.name,
      "filters": values.filters.map(
        filter => ({ field: filter.field.value.name, condition: filter.condition.value, value: filter.value })
      ),
      "source_type": "STREAM",
    }
    props.createStreamAction(payload);
    actions.setSubmitting(false);
  }

  const streamsOptions = props.streamList.map(stream => ({ value: stream, label: stream.name }))
  const fieldOptions = props.streamDetail
    ? props.streamDetail.fields.map(field => ({ value: { ...field, name: `${props.streamDetail.name}.${field.name}` }, label: `${props.streamDetail.name}.${field.name}` }))
    : []

  return (
    <SiteWrapper>
      <Page.Content title="Create your stream" subTitle="from an existing Stream">
        <Grid.Row cards>
          <Grid.Col width={12}>
            <Card>
              <Card.Body>
                <Wizard
                  initialValues={{
                    streamName: "",
                    sourceName: {},
                    fields: [],
                    filters: [],
                  }}
                  onSubmit={onSubmit}
                  finalizeButtonText="Create Stream"
                >
                  <Wizard.Page
                    validationSchema={
                      Yup.object({
                        streamName: Yup.string()
                          .matches(/^\S+$/, {message: 'Stream Name cannot contains white spaces'})
                          .required('Stream Name is required'),
                        sourceName: Yup.object()
                          .test(
                            'isSourceEmpty',
                            'Select the Origin Stream',
                            (value) => !(Object.keys(value).length === 0)),
                      })
                    }
                  >
                    <Form.Group label='Stream Name' isRequired>
                      <CustomFormikField
                        RootComponent={Form.Input}
                        id='streamName'
                        name='streamName'
                        type='text'
                        placeholder='Enter the stream name'
                      />
                    </Form.Group>
                    <Form.Group label='Origin Stream' isRequired>
                      <ReactSelectFormik
                        id='sourceName'
                        name='sourceName'
                        isDisabled={props.waitingStreamList || props.waitingStreamDetail}
                        isLoading={props.waitingStreamList || props.waitingStreamDetail}
                        options={streamsOptions}
                        onChange={(value) => props.getStreamDetailAction(value.label)}
                      />
                    </Form.Group>
                  </Wizard.Page>
                  <Wizard.Page
                    validationSchema={
                      Yup.object({
                        fields: Yup.array()
                          .of(
                            Yup.object().shape({
                              label: Yup.string(),
                              value: Yup.string(),
                            })
                          ).min(1, 'Select at least one field to continue')
                          .ensure()
                      })
                    }
                  >
                    <ReactSelectFormik
                      id='fields'
                      name='fields'
                      isMulti
                      closeMenuOnSelect={false}
                      options={fieldOptions}
                    />
                  </Wizard.Page>
                  <Wizard.Page
                    validationSchema={
                      Yup.object({
                        filters: Yup.array()
                          .of(
                            Yup.object().shape({
                              field: Yup.object().required('Select field'),
                              condition: Yup.object().required('Select condition'),
                              value: Yup.string()
                                .matches(/^[a-zA-Z0-9\s]+$/, {message: 'Value could not contain special characters'})
                            })
                          )
                      })
                    }
                  >
                    <Form.Group label='Filters'>
                      <CustomFieldArray fieldOptions={fieldOptions} name="filters"/>
                    </Form.Group>
                  </Wizard.Page>
                </Wizard>
              </Card.Body>
            </Card>
          </Grid.Col>
        </Grid.Row>
      </Page.Content>
    </SiteWrapper>
  );
}

const mapStateToProps = state => ({
  waitingStreamList: state.createNewStreamFromStreamState.waitingStreamList,
  streamList: state.createNewStreamFromStreamState.streamList,
  waitingStreamDetail: state.createNewStreamFromStreamState.waitingStreamDetail,
  streamDetail: state.createNewStreamFromStreamState.streamDetail,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getStreamListAction,
    getStreamDetailAction,
    createStreamAction,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(CreateNewStreamFromStream);