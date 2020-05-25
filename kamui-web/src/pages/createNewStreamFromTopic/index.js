import React, { useEffect } from "react";
import * as Yup from "yup";

import SiteWrapper from "../../SiteWrapper";
import { Card, Grid, Page } from "tabler-react";
import { Form } from "tabler-react";
import { bindActionCreators } from "redux";
import { createStreamAction, getTopicList, getTopicSchemaAction } from "./actions";
import { connect } from "react-redux";
import CustomFormikField from "../../components/customFormikField";
import ReactSelectFormik from "../../components/reactSelectFormik";
import Wizard from "../../components/wizard";

function CreateNewStreamFromTopic(props) {
  useEffect(() => {
    props.getTopicList();
  }, [props.getTopicList])

  const onSubmitForm = (values, actions) => {
    const { projectId } = props.match.params;
    const payload = {
      "project_id": projectId,
      "stream_name": values.streamName,
      "fields": values.fields.map(field => field.value),
      "source_name": values.sourceName.value,
      "source_type": "TOPIC",
    }
    props.createStreamAction(payload);
    actions.setSubmitting(false);
  }

  const topicOptions = props.topicList.map(topic => ({ value: topic, label: topic }))
  const fieldOptions = props.topicSchema ? props.topicSchema.fields.map(field => ({ value: field, label: field.name })) : [];

  return (
    <SiteWrapper>
      <Page.Content title="Create your stream" subTitle="from an existing Kafka Topic">
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
                  onSubmit={onSubmitForm}
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
                            'Select the Origin Topic',
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
                    <Form.Group label='Origin Topic' isRequired>
                      <ReactSelectFormik
                        id='sourceName'
                        name='sourceName'
                        isDisabled={props.waitingTopicList || props.waitingTopicSchema}
                        isLoading={props.waitingTopicList || props.waitingTopicSchema}
                        options={topicOptions}
                        onChange={(value) => props.getTopicSchemaAction(value.value)}
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
  waitingTopicList: state.createNewStreamFromTopicState.waitingTopicList,
  topicList: state.createNewStreamFromTopicState.topicList,
  waitingTopicSchema: state.createNewStreamFromTopicState.waitingTopicSchema,
  topicSchema: state.createNewStreamFromTopicState.topicSchema,
})

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getTopicList,
    getTopicSchemaAction,
    createStreamAction,
  }, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(CreateNewStreamFromTopic);