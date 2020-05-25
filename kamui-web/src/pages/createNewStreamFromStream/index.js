import React, { useEffect } from "react";
import SiteWrapper from "../../SiteWrapper";
import { bindActionCreators } from "redux";
import { createStreamAction, getStreamDetailAction, getStreamListAction } from "./actions";
import { connect } from "react-redux";
import { Card, Form, Grid, Page } from "tabler-react";
import Wizard from "../../components/wizard";
import * as Yup from "yup";
import CustomFormikField from "../../components/customFormikField";
import ReactSelectFormik from "../../components/reactSelectFormik";

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
      "source_type": "STREAM",
    }
    props.createStreamAction(payload);
    actions.setSubmitting(false);
  }

  const streamsOptions = props.streamList.map(stream => ({ value: stream, label: stream.name }))
  const fieldOptions = props.streamDetail ? props.streamDetail.fields.map(field => ({ value: field, label: field.name })) : []

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