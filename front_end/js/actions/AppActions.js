/*
 * Actions change things in your application
 * Since this boilerplate uses a uni-directional data flow, specifically redux,
 * we have these actions which are the only way your application interacts with
 * your appliction state. This guarantees that your state is up to date and nobody
 * messes it up weirdly somewhere.
 *
 * To add a new Action:
 * 1) Import your constant
 * 2) Add a function like this:
 *    export function yourAction(var) {
 *        return { type: YOUR_ACTION_CONSTANT, var: var }
 *    }
 * 3) (optional) Add an async function like this:
 *    export function asyncYourAction(var) {
 *        return function(dispatch) {
 *             // Do async stuff here
 *             return dispatch(yourAction(var));
 *        }
 *    }
 *
 *    If you add an async function, remove the export from the function
 *    created in the second step
 */

require('es6-promise').polyfill();
import bcrypt from 'bcryptjs';
import R from 'ramda';
import { SET_AUTH, CHANGE_FORM, SENDING_REQUEST, SET_ERROR_MESSAGE } from '../constants/AppConstants';
import * as errorMessages  from '../constants/MessageConstants';
import auth from '../utils/auth';
import genSalt from '../utils/salt';
import { browserHistory } from 'react-router';
import fetch from 'isomorphic-fetch';

/**
 * Logs an user in
 * @param  {string} username The username of the user to be logged in
 * @param  {string} password The password of the user to be logged in
 */

const baseUrl = 'http://10.175.186.34:5000';

export function login(username, password, interval) {
  return (dispatch) => {
    // Show the loading indicator, hide the last error
    dispatch(sendingRequest(true));
    // If no username or password was specified, throw a field-missing error
    if (anyElementsEmpty({ username, password })) {
      dispatch(setErrorMessage(errorMessages.FIELD_MISSING));
      dispatch(sendingRequest(false));
      return;
    }

    if (!R.equals(R.length(interval), R.length(password) - 1)) {
      dispatch(setErrorMessage(errorMessages.PASSWORD_BREAK));
      dispatch(sendingRequest(false));
      return;
    }

    // Generate salt for password encryption
    const salt = genSalt(username);
    // Encrypt password
    bcrypt.hash(password, salt, (err, hash) => {
      // Something wrong while hashing
      if (err) {
        dispatch(setErrorMessage(errorMessages.GENERAL_ERROR));
        return;
      }
      // Use auth.js to fake a request
      
      auth.login(username, hash, async (success, err) => {
        if (success === true) {
          const reponse = fetch(`${baseUrl}/predict`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              userName: username,
              dataset: [ interval],
            })
          }).then(response => {
            if (response.status >= 200 && response.status < 300) {
              return response.json()
            }
          }).then(body => {
            const rateArray = JSON.parse(localStorage.getItem("rate:" + username)) || [];
            rateArray.push(parseInt(body.rate * 100) );
            localStorage.setItem("rate:" + username, JSON.stringify(rateArray));
            const key = "validateSet:" + username;
            const validateSet = JSON.parse(localStorage.getItem(key)) || [];
            validateSet.push(interval);
            localStorage.setItem("username", username);
            localStorage.setItem(key, JSON.stringify(validateSet));
            // When the request is finished, hide the loading indicator
            dispatch(sendingRequest(false));
            dispatch(setAuthState(success));
            
            // If the login worked, forward the user to the dashboard and clear the form
            forwardTo('/dashboard');
            dispatch(changeForm({
              username: "",
              password: ""
            }));    
        }).catch(e => {
          dispatch(sendingRequest(false));
          dispatch(setAuthState(false));
        });
      } else {
          switch (err.type) {
            case 'user-doesnt-exist':
              dispatch(setErrorMessage(errorMessages.USER_NOT_FOUND));
              return;
            case 'password-wrong':
              dispatch(setErrorMessage(errorMessages.WRONG_PASSWORD));
              return;
            default:
              dispatch(setErrorMessage(errorMessages.GENERAL_ERROR));
              return;
          }
        }
      });
    });
  }
}

/**
 * Logs the current user out
 */
export function logout() {
  return (dispatch) => {
    dispatch(sendingRequest(true));
    auth.logout((success, err) => {
      if (success === true) {
        dispatch(sendingRequest(false))
        dispatch(setAuthState(false));
        browserHistory.push("/");
      } else {
        dispatch(setErrorMessage(errorMessages.GENERAL_ERROR));
      }
    });
  }
}

/**
 * Registers a user
 * @param  {string} username The username of the new user
 * @param  {string} passwords The passwords of the new user
 */
export function register({username, passwords = [], intervals = [], passwords1 = [], intervals1 = []}) {
  return (dispatch) => {
    console.info("username:", username)
    console.info("passwords:", passwords)
    console.info("passwords1:", passwords1)
    console.info("intervals:", intervals)
    console.info("intervals1:", intervals1)
    
    // Show the loading indicator, hide the last error
    dispatch(sendingRequest(true));
    const allPasswords = R.concat(passwords, passwords1);
    const allIntervals = R.concat(intervals, intervals1);

    // If no username or password was specified, throw a field-missing error
    if (R.length(passwords) < 3 && anyElementsEmpty({username, passwords: allPasswords })) {
      dispatch(setErrorMessage(errorMessages.FIELD_MISSING));
      dispatch(sendingRequest(false));
      return;
    }

    if (R.length(R.uniq(allPasswords)) > 1) {
      dispatch(setErrorMessage(errorMessages.PASSWORD_INCONSISTENT));
      dispatch(sendingRequest(false));
      return;
    }

    for (const interval of allIntervals) {
      if (!R.equals(R.length(interval), R.length(passwords[0]) - 1)) {
        dispatch(setErrorMessage(errorMessages.PASSWORD_BREAK));
        dispatch(sendingRequest(false));
        return;
      }
    }

    localStorage.setItem("trainSet:" + username, JSON.stringify(intervals));
    localStorage.setItem("username", username);
    localStorage.setItem("validateSet:" + username, JSON.stringify([]));

    // Generate salt for password encryption
    const salt = genSalt(username);
    // Encrypt password
    bcrypt.hash(passwords[0], salt, (err, hash) => {
      // Something wrong while hashing
      if (err) {
        dispatch(setErrorMessage(errorMessages.GENERAL_ERROR));
        return;
      }
      // Use auth.js to fake a request
      auth.register(username, hash, (success, err) => {
        const reponse = fetch(`${baseUrl}/train`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userName: username,
            dataset: intervals,
            dataset2: intervals1,
          }),
        }).then(response => {
                  // When the request is finished, hide the loading indicator
          dispatch(sendingRequest(false));
          dispatch(setAuthState(success));
          if (success) {
            // If the register worked, forward the user to the homepage and clear the form
            forwardTo('/dashboard');
            dispatch(changeForm({
              username: "",
              passwords: [],
            }));
          } else {
            switch (err.type) {
              case 'username-exists':
                dispatch(setErrorMessage(errorMessages.USERNAME_TAKEN));
                return;
              default:
                dispatch(setErrorMessage(errorMessages.GENERAL_ERROR));
                return;
            }
          }
        }).catch(e => {
          dispatch(sendingRequest(false));
          dispatch(setAuthState(false));
        });       
      });
    });
  }
}

/**
 * Sets the authentication state of the application
 * @param {boolean} newState True means a user is logged in, false means no user is logged in
 */
export function setAuthState(newState) {
  return { type: SET_AUTH, newState };
}

/**
 * Sets the form state
 * @param  {object} newState          The new state of the form
 * @param  {string} newState.username The new text of the username input field of the form
 * @param  {string} newState.password The new text of the password input field of the form
 * @return {object}                   Formatted action for the reducer to handle
 */
export function changeForm(newState) {
  return { type: CHANGE_FORM, newState };
}

/**
 * Sets the requestSending state, which displays a loading indicator during requests
 * @param  {boolean} sending The new state the app should have
 * @return {object}          Formatted action for the reducer to handle
 */
export function sendingRequest(sending) {
  return { type: SENDING_REQUEST, sending };
}


/**
 * Sets the errorMessage state, which displays the ErrorMessage component when it is not empty
 * @param message
 */
function setErrorMessage(message) {
  return (dispatch) => {
    dispatch({ type: SET_ERROR_MESSAGE, message });

    const form = document.querySelector('.form-page__form-wrapper');
    if (form) {
      form.classList.add('js-form__err-animation');
      // Remove the animation class after the animation is finished, so it
      // can play again on the next error
      setTimeout(() => {
        form.classList.remove('js-form__err-animation');
      }, 150);

      // Remove the error message after 3 seconds
      setTimeout(() => {
        dispatch({ type: SET_ERROR_MESSAGE, message: '' });
      }, 3000);
    }
  }
}

/**
 * Forwards the user
 * @param {string} location The route the user should be forwarded to
 */
function forwardTo(location) {
  console.log('forwardTo(' + location + ')');
  browserHistory.push(location);
}


/**
 * Checks if any elements of a JSON object are empty
 * @param  {object} elements The object that should be checked
 * @return {boolean}         True if there are empty elements, false if there aren't
 */
function anyElementsEmpty(elements) {
  for (let element in elements) {
    if (!elements[element]) {
      return true;
    }
  }
  return false;
}
