import * as React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "tabler-react/dist/Tabler.css";
import {
  Projects,
  CreateProject,
  ProjectDetails,
  CreateNewStreamFromTopic,
  CreateNewStreamFromStream,
  Streams,
} from "./pages";
import "./App.css"

function App(props: Props) {
  return (
    <React.StrictMode>
      <Router>
        <Switch>
          <Route exact path="/" component={Projects} />
          <Route exact path="/projects" component={Projects} />
          <Route exact path="/projects/create" component={CreateProject} />
          <Route exact path="/projects/:projectId/streams/create/from-topic" component={CreateNewStreamFromTopic} />
          <Route exact path="/projects/:projectId/streams/create/from-stream" component={CreateNewStreamFromStream} />
          <Route exact path="/projects/:projectId" component={ProjectDetails} />
          <Route exact path="/streams" component={Streams} />
        </Switch>
      </Router>
    </React.StrictMode>
  );
}

export default App;
