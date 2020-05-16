import * as React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "tabler-react/dist/Tabler.css";
import Projects from "./pages/projects";

function App(props: Props) {
  return (
    <React.StrictMode>
      <Router>
        <Switch>
          <Route exact path="/" component={Projects} />
          <Route exact path="/projects" component={Projects} />
        </Switch>
      </Router>
    </React.StrictMode>
  );
}

export default App;
