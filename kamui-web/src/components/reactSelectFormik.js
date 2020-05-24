import { useField } from "formik";
import Select from "react-select";
import React from "react";

const ReactSelectFormik = ({onChange = () => {}, ...props}) => {
  const [field, meta, helpers] = useField(props);

  const _onChange = (value) => {
    onChange(value);
    helpers.setValue(value);
  }

  return (
    <div>
      <Select
        onChange={_onChange}
        onBlur={helpers.setTouched}
        value={field.value}
        {...props}
      />
      {meta.touched && (meta.error && <p style={{color: "red", fontSize: "12px"}}>{meta.error}</p>)}
    </div>
  )
}

export default ReactSelectFormik;