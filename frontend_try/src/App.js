import React from "react";
import axios from "axios";
import Register from "./components/Register";
import Menu from "./components/Menu";
import {Route, Switch, BrowserRouter, Redirect} from 'react-router-dom';
import { Provider, connect } from "react-redux";
import { createStore, applyMiddleware } from "redux";


class App extends React.Component {
  render() {
    return (
      <div>
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Menu} />
            <Route exact path="/register" component={Register} />
          </Switch>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;