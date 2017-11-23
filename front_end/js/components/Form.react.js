/**
 * Form.react.js
 *
 * The form with a username and a password input field, both of which are
 * controlled via the application state.
 *
 */

import React, { Component } from 'react';
import { changeForm } from '../actions/AppActions';
import LoadingButton from './LoadingButton.react';
import ErrorMessage from './ErrorMessage.react';
import observe from '../utils/observer';
import R from 'ramda';
// Object.assign is not yet fully supported in all browsers, so we fallback to
// a polyfill
const assign = Object.assign || require('object.assign');

class LoginForm extends Component {
  _recordKeyInterval(index, isNegative, evt) {
    if (!this.passwordFieldRecords) {
      this.passwordFieldRecords = [];
    }

    if (!this.negativePasswordFieldRecords) {
      this.negativePasswordFieldRecords = [];
    }
    
    if (isNegative) {
      if (!this.negativePasswordFieldRecords[index]) {
        this.negativePasswordFieldRecords[index] = observe.interval(evt.target);
      } else {
        this.negativePasswordFieldRecords[index].length = 0;
      }
    } else {
      if (!this.passwordFieldRecords[index]) {
        this.passwordFieldRecords[index] = observe.interval(evt.target);
      } else {
        this.passwordFieldRecords[index].length = 0;
      }
    }
  }

  isPrintable(keycode) {
    const valid = 
        (keycode > 47 && keycode < 58)   || // number keys
        keycode == 32 || keycode == 13   || // spacebar & return key(s) (if you want to allow carriage returns)
        (keycode > 64 && keycode < 91)   || // letter keys
        (keycode > 95 && keycode < 112)  || // numpad keys
        (keycode > 185 && keycode < 193) || // ;=,-./` (in order)
        (keycode > 218 && keycode < 223);   // [\]' (in order)

    return valid;
  }

  _updateRecord(index) {
    let keysPressedRecords  = this.passwordFieldRecords[index] || [];
    keysPressedRecords = R.filter(x => this.isPrintable(x.keyCode), keysPressedRecords);

    const sortedRecords = R.sortBy(R.prop("start"))(keysPressedRecords);

    const intervals = [];
    for (let i = 1; i < R.length(sortedRecords); i ++) {
      intervals.push(sortedRecords[i].start - sortedRecords[i - 1].end);
    }

    console.info(intervals);

    const newIntervals = R.clone(this.props.data.intervals) || [];
    newIntervals[index] = intervals;
    var newState = this._mergeWithCurrentState({
      intervals: newIntervals 
    });

    this._emitChange(newState);
  }

  _updateRecordNegative(index) {
    let keysPressedRecords  = this.negativePasswordFieldRecords[index] || [];
    keysPressedRecords = R.filter(x => this.isPrintable(x.keyCode), keysPressedRecords);

    const sortedRecords = R.sortBy(R.prop("start"))(keysPressedRecords);

    const intervals = [];
    for (let i = 1; i < R.length(sortedRecords); i ++) {
      intervals.push(sortedRecords[i].start - sortedRecords[i - 1].end);
    }

    console.info(intervals);

    const newIntervals = R.clone(this.props.data.intervals1) || [];
    newIntervals[index] = intervals;
    var newState = this._mergeWithCurrentState({
      intervals1: newIntervals 
    });

    this._emitChange(newState);
  }

  renderPasswordFields = () => {
    const { passwordRepeat } = this.props;
    const {passwords = []} = this.props.data;

    const passwordFields = [];
    for (let i = 0; i < passwordRepeat + 1; i ++) {
      passwordFields.push(      
        <input className="form__field-input" 
          onFocus={this._recordKeyInterval.bind(this, i, false)}
          onKeyUp={this._updateRecord.bind(this, i)}
          id={"password_" + i}
          type={this.props.hidePassword? "password":"text"}
          value={passwords[i]}
          placeholder="" 
          onChange={this._changePassword.bind(this, i, false)} />
      );
    }

    return passwordFields;
  }

  renderNegativePasswordFields() {
    const { negativePasswordRepeat } = this.props;
    const {negativePasswords = []} = this.props.data;

    const negativePasswordFields = [];
    for (let i = 0; i < negativePasswordRepeat + 1; i ++) {
      negativePasswordFields.push(      
        <input className="form__field-input" 
          onFocus={this._recordKeyInterval.bind(this, i, true)}
          onKeyUp={this._updateRecordNegative.bind(this, i)}
          id={"ngetive_password_" + i}
          type="text"
          value={negativePasswordFields[i]}
          placeholder="" 
          onChange={this._changePassword.bind(this, i, true)} />
      );
    }

    return negativePasswordFields;
  }

  render() {
    return(
      <form className="form" onSubmit={this._onSubmit.bind(this)}>
        <ErrorMessage />
        <div className="form__field-wrapper">
          <div><span className="form__field-label">Username</span></div>
          <input className="form__field-input" type="text" id="username" value={this.props.data.username} placeholder="frank.underwood" onChange={this._changeUsername.bind(this)} autoCorrect="off" autoCapitalize="off" spellCheck="false" />
        </div>
        <div className="form__field-wrapper">
          <div className="form__password-wrapper">
            <div><span className="form__field-label">Password</span></div>
            {this.renderPasswordFields()}
          </div>
          {!!this.props.showNegativePasswordInputs &&
          <div className="form__password-wrapper">
            <div><span className="form__field-label">Negative</span></div>
            {this.renderNegativePasswordFields()}
          </div>}
        </div>
        <div className="form__submit-btn-wrapper">
          {this.props.currentlySending ? (
            <LoadingButton />
          ) : (
            <button className="form__submit-btn" type="submit">{this.props.btnText}</button>
          )}
        </div>
      </form>
    );
  }

  // Change the username in the app state
  _changeUsername(evt) {
    var newState = this._mergeWithCurrentState({
      username: evt.target.value
    });

    this._emitChange(newState);
  }

  // Change the password in the app state
  _changePassword(i, isNegative, evt) {
    const passwords = isNegative ? this.props.data.passwords1 : this.props.data.passwords;
    const newPasswords = R.clone(passwords) || [];

    if (R.length(evt.target.value) == 1) {
      if (isNegative) {
        this.negativePasswordFieldRecords[i].length = 0;
      } else {
        this.passwordFieldRecords[i].length = 0;
      }
    }

    newPasswords[i] = evt.target.value;

    var changed = isNegative ? {
      passwords1: newPasswords
    } : {
      passwords: newPasswords
    }
    var newState = this._mergeWithCurrentState(changed);

    this._emitChange(newState);
  }

  // Merges the current state with a change
  _mergeWithCurrentState(change) {
    return assign(this.props.data, change);
  }

  // Emits a change of the form state to the application state
  _emitChange(newState) {
    this.props.dispatch(changeForm(newState));
  }

  // onSubmit call the passed onSubmit function
  _onSubmit(evt) {
    evt.preventDefault();
    this.props.onSubmit(this.props.data);
  }
}

LoginForm.defaultProps = {
  passwordRepeat: 0,
  showNegativePasswordInputs: false,
  negativePasswordRepeat: 0,
  hidePassword: false,
}

LoginForm.propTypes = {
  onSubmit: React.PropTypes.func.isRequired,
  btnText: React.PropTypes.string.isRequired,
  data: React.PropTypes.object.isRequired,
  passwordRepeat: React.PropTypes.number,
  showNegativePasswordInputs: React.PropTypes.bool,
  negativePasswordRepeat: React.PropTypes.number,
  hidePassword: React.PropTypes.bool,
}

export default LoginForm;
