/*
 * HomePage
 *
 * This is the first thing users see of the app
 * Route: /
 *
 */

import React, { Component } from 'react';
import { Link } from 'react-router';
import Nav from '../Nav.react';
import { connect } from 'react-redux';

class HomePage extends Component {
	render() {
    const dispatch = this.props.dispatch;
    const { loggedIn } = this.props.data;

    return (
			<article>
				<div>
					<section className="text-section">
						{/* Change the copy based on the authentication status */}
						{loggedIn ? (
							<h1>Welcome to IAM+, you are logged in!</h1>
						) : (
							<h1>Welcome to IAM+!</h1>
						)}
						{loggedIn ? (
							<Link to="/dashboard" className="btn btn--dash">Dashboard</Link>
						) : (
							<div>
								
								<Link to="/login" className="btn btn--login">Login</Link>
								<Link to="/register" className="btn btn--register">Register</Link>
							</div>
						)}
						<img src="/img/Picture1.png" width="20%" style={{float: 'right'}}/>
					</section>
					<section className="text-section">
						<h2>Features</h2>
						<ul>
							<li>
								<p>IAM+ is the next generation of IAM, which utilizes Deep Learning to empower IAM to reach a balance between security and user experience. </p>
							</li>
							<li>
								<p>The main purpose of IAM+ is to choose the most suitable AA solution to offer the best user experience. For example, User Awareless IAM.</p>
							</li>
							<li>
								<p>The brain of IAM+ is a Deep Learning Core Module which will fetch multidimensional information and make a judgment based on it.</p>
							</li>
							<li>
								<p>In this demo, we will show how to use Neural Network, one of hottest areas of Deep Learning, to recognize if the use is himself or not by Bio Features. </p>
							</li>
						</ul>
					</section>
					{/*}
					<section className="text-section">
						<h2>Authentication</h2>
						<p>Authentication happens in <code>js/utils/auth.js</code>, using <code>fakeRequest.js</code> and <code>fakeServer.js</code>. <code>fakeRequest</code> is a fake XMLHttpRequest wrapper with a similar syntax to <code>request.js</code> which simulates network latency. <code>fakeServer</code> responds to the fake HTTP requests and pretends to be a real server, storing the current users in localStorage with the passwords encrypted using <code>bcrypt</code>.
						</p>
						<p>To change it to real authentication, you’d only have to import <code>request.js</code> instead of <code>fakeRequest.js</code> and have a server running somewhere.</p>
					</section>
					{*/}
				</div>
			</article>
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
export default connect(select)(HomePage);
