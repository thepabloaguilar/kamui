import React, { Component } from "react";
import { Formik } from "formik";
import { Button, Form } from "tabler-react";

class Wizard extends Component {
  static Page = ({ children }) => children;

  constructor(props) {
    super(props);
    this.state = {
      page: 0,
      values: props.initialValues,
      finalizeButtonText: props.finalizeButtonText || 'Submit'
    };
  }

  next = values =>
    this.setState(state => ({
      page: Math.min(state.page + 1, this.props.children.length - 1),
      values
    }));

  previous = () =>
    this.setState(state => ({
      page: Math.max(state.page - 1, 0)
    }));

  validate = values => {
    const activePage = React.Children.toArray(this.props.children)[
      this.state.page
      ];
    return activePage.props.validate ? activePage.props.validate(values) : {};
  };

  handleSubmit = (values, bag) => {
    const { children, onSubmit } = this.props;
    const { page } = this.state;
    const isLastPage = page === React.Children.count(children) - 1;
    if (isLastPage) {
      return onSubmit(values, bag);
    } else {
      this.next(values);
      bag.setSubmitting(false);
    }
  };

  render() {
    const { children } = this.props;
    const { page, values } = this.state;
    const activePage = React.Children.toArray(children)[page];
    const isLastPage = page === React.Children.count(children) - 1;
    const { validationSchema } = activePage.props;
    return (
      <Formik
        initialValues={values}
        enableReinitialize={false}
        validationSchema={validationSchema}
        validate={this.validate}
        onSubmit={this.handleSubmit}
        render={({handleSubmit, isSubmitting}) => (
          <Form onSubmit={handleSubmit}>
            {activePage}
            <Button.List className="mt-4" align="right">
              {page > 0 && (
                <Button type='button' onClick={this.previous} color='primary' className='ml-auto' outline>
                  Previous
                </Button>
              )}
              <Button loading={isSubmitting} color='primary' className='ml-auto' outline={!isSubmitting}>
                {isLastPage ? this.state.finalizeButtonText : 'Next'}
              </Button>
            </Button.List>
          </Form>
        )}
      />
    );
  }
}

export default Wizard;