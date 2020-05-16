import * as React from "react";
import { NavLink, withRouter } from "react-router-dom";

import {
  Site,
  Grid,
  List,
  RouterContextProvider,
} from "tabler-react";

const navBarItems = [
  {
    value: "Projects",
    to: "/projects",
    icon: "briefcase",
    LinkComponent: withRouter(NavLink),
    useExact: true,
  },
  {
    value: "Streams",
    icon: "box",
    subItems: [
      {
        value: "Streams",
        to: "/streams",
        LinkComponent: withRouter(NavLink),
      },
    ],
  },
];

class SiteWrapper extends React.Component {
  render() {
    return (
      <Site.Wrapper
        headerProps={{
          href: "/",
          alt: "Kamui",
          imageURL: "/images/kamui_logo.png",
        }}
        navProps={{ itemsObjects: navBarItems }}
        routerContextComponentType={withRouter(RouterContextProvider)}
        footerProps={{
          copyright: (
            <React.Fragment>
              Copyright © 2020
              <a href="https://github.com/thepabloaguilar/kamui/"> Kamui</a>. Theme by
              <a
                href="https://codecalm.net"
                target="_blank"
                rel="noopener noreferrer"
              >
                {" "}
                codecalm.net
              </a>{" "}
              All rights reserved.
            </React.Fragment>
          ),
          nav: (
            <React.Fragment>
              <Grid.Col auto={true}>
                <List className="list-inline list-inline-dots mb-0">
                  <List.Item className="list-inline-item">
                    <a href="https://github.com/thepabloaguilar/kamui/">Documentation</a>
                  </List.Item>
                </List>
              </Grid.Col>
            </React.Fragment>
          ),
        }}
      >
        {this.props.children}
      </Site.Wrapper>
    );
  }
}

export default SiteWrapper;