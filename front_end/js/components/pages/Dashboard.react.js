/*
* HomePage
*
* The Dashboard is only visible to logged in users
* Route: /dashboard
*
*/

import React, { Component } from 'react';
import { connect } from 'react-redux';
import {Bar as BarChart, Line as LineChart} from 'react-chartjs-2';
import R from 'ramda';

class Dashboard extends Component {
  getValidateSet() {
    const username = localStorage.getItem("username");
    const validateSet = localStorage.getItem("validateSet:" + username);
  
    return JSON.parse(validateSet) || [];
  }

  render() {
    const validateSet = this.getValidateSet();
    const username = localStorage.getItem("username");
    const confidenSet = JSON.parse(localStorage.getItem("rate:" + username)) || [];
    const isValid = confidenSet[confidenSet.length - 1] > 50? true : false;
    const rangeSize = confidenSet.length > 15? confidenSet.length : 15;
    let colorSet = [];
    for (const value of confidenSet) {
      if (value >= 50) {
        colorSet.push('rgb(0, 123, 120)');
      } else {
        colorSet.push('rgb(255, 51, 0)');
      }
    }
    const barChartData = {
      labels: R.range(0, rangeSize),
      datasets: [{
        label: "Confident Rate",
        backgroundColor: colorSet,
        data: confidenSet
      }]
    };

    const barChartOptions = {
      tooltip: {
        enabled: false,
      },
      legend: {
        display: false,
      }
    }

    const datasets = R.addIndex(R.map)((data, idx) => ({
      borderColor: confidenSet[idx] > 50 ? "rgb(0, 123, 120)": 'rgb(255, 51, 0)',
      pointBackgroundColor: confidenSet[idx] > 50 ? "rgb(0, 123, 120)": 'rgb(255, 51, 0)',
      label: idx,
      data,
      fill: false }), validateSet || []);
    if (R.isEmpty(datasets)) {
      datasets.push({
        label: "default",
        data: [],
        fill: false,
      });
    }

    const xRayNum = R.length(validateSet[0]) || 10;
    const lineChartData = {
      labels: R.range(0, xRayNum),
      datasets,
    };

    const detailChartOptions = {
      elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        }, 
      legend: {
        display: false,
      }
    };

    const validMessage = (function() {
      if (isValid) {
        return (
          <p> 
            <h2 style={{color: "rgb(0, 123, 120)",}}>This Login Attemp is VALID.</h2>
          </p>
        )
      } else {
        return (
             <p>
            <h2  style={{color: 'rgb(255, 51, 0)'}}>This Login Attemp is INVALID.</h2>
          </p>
        )
        
      }
    })()
  
    return (  
    
    <div className="dashboard_content">
      <div>
        {validMessage} 
      </div>
    <h2>Confident Rate</h2>
    <BarChart data={barChartData} options={barChartOptions} width="600" height="400" />
    <h2>Detail</h2>
    <LineChart data={lineChartData} options={detailChartOptions} width="600" height="400" />
    </div>
    );
  }
}

// Which props do we want to inject, given the global state?
function select(state) {
  return {
    data: state
  };
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(Dashboard);
