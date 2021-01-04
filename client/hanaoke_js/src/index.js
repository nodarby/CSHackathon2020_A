import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from "./Home";
import Result from "./Result";

ReactDOM.render(
  <React.StrictMode>
      <Router>
          <Route exact path="/" component={Home}/>
          <Route path="/result" component={Result}/>
      </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
