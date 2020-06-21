# Create stream from stream

To create a new stream you have to follow the steps described below.

## Basic Information

* **Stream Name**: The stream name should be unique or you'll get some errors
* **Origin Topic**: Select the Kafka Topic that you want from the dropdown list

[![Basic Information Step](images/streams/from_stream/basic_information_step.png)](images/streams/from_stream/basic_information_step.png)


## Desired Fields

* **Fields**: Select the desired fields to your stream from the dropdown list, you have to select at least one field to
continue

[![Desired Fields Step](images/streams/from_stream/fields_step.png)](images/streams/from_stream/fields_step.png)

## Filters

In this step, you can create the stream filter.

You can create the stream without any filter:

[![Filters Step without created filter](images/streams/from_stream/filters_step_without_created_filter.png)](images/streams/from_stream/filters_step_without_created_filter.png)

Or create some filters to your stream:

[![Filters Step with created filter](images/streams/from_stream/filters_step_with_created_filter.png)](images/streams/from_stream/filters_step_with_created_filter.png)

!!! warning
    So far, we don't support the choice among *AND*, *OR* and *NOT* operators, all applied filters will be *"connected"*
    using *AND* operator!

---

Finally, click on the ***Create Stream*** button!
