import { useField } from "formik";
import React from "react";

const CustomFormikField = ({RootComponent, ...props}) => {
  const [field, meta] = useField(props);

  return (
    <RootComponent
      invalid={meta.touched && meta.error}
      feedback={meta.error}
      {...field}
      {...props}
    />
  )
}

export default CustomFormikField;