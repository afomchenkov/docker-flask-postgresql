import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import reportWebVitals from './reportWebVitals';

import UsersList from './components/UsersList';
import AddUser from './components/AddUser';

// process.env.REACT_APP_USERS_SERVICE_URL

const SERVICE_URL = 'http://127.0.0.1:5001';

const getUsers = (handler) => {
  return axios.get(`${SERVICE_URL}/users`)
    .then((res) => {
      handler(res.data.data.users);
    })
    .catch((err) => {
      console.log(err);
    });
}

const saveUser = (user) => {
  return axios.post(`${SERVICE_URL}/users`, user)
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
    });
}

const App = () => {
  const [users, setUsers] = useState([])
  const [username, setUsername] = useState('dow')
  const [email, setEmail] = useState('john.dow@test.com')

  useEffect(() => {
    getUsers(setUsers);
  }, [])

  const addUser = (event) => {
    event.preventDefault();

    const { username, email } = event.target
    console.log(username.value, email.value);

    saveUser({
      username: username.value,
      email: email.value,
    })
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-md-6">
          <br />
          <h1>All Users</h1>
          <hr /><br />
          <AddUser addUser={addUser} username={username} email={email} />
          <br />
          <UsersList users={users} />
        </div>
      </div>
    </div>
  )
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
