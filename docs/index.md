# Introduction

This project idea was born when I was trying to create my graduation project, I wanted to create a data analysis
pipeline using [streams](https://en.wikipedia.org/wiki/Stream). For the first time, I thought to use
[Kafka Streams](https://kafka.apache.org/documentation/streams/) to achieve my goals. So I realized something,
Kafka Streams are good but I don't want this complexity for now!

After that the first idea came out:

> Why not create a tool/system to create those streams more easily to the users just worry about the data?

They don't need to worry about the programming language to use or the deployment environment.
They just want to ingest some data and transform them out.

I talked about my idea with a friend, he liked and presented another tool to create streams more easily. The tool is
[KSQL](https://docs.ksqldb.io/en/latest/), it's basically a wrapper above *Kafka Streams*. With it you really can
create streams more easily using its SQL specification, no secret to use it.

While I was reading *KSQL* documentation another idea came out:

> To interact with *KSQL* without using its REST API we have to use
> [Control Center](https://docs.confluent.io/current/control-center/index.html),
> it's a platform created by [Confluent](https://www.confluent.io).
> But users have to learn KSQL specifications to start stream creation!
>
> Why not create a system/platform to abstract that language to the users?

So, we're here now. This project is wrapper above KSQL and my graduation project!
