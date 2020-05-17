import * as React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "tabler-react/dist/Tabler.css";
import {Projects, CreateProject} from "./pages";

function App(props: Props) {
  return (
    <React.StrictMode>
      <Router>
        <Switch>
          <Route exact path="/" component={Projects} />
          <Route exact path="/projects" component={Projects} />
          <Route exact path="/projects/create" component={CreateProject} />
        </Switch>
      </Router>
    </React.StrictMode>
  );
}

export default App;
