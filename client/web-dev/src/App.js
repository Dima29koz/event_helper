import './App.css';
import { useState } from 'react';
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import Login from './components/Auth/Login';
import Home from './components/Home/Home';
import Registration from './components/Auth/Registration';
import { getCurrentUser, removeCurrentUser, setCurrentUser } from './utils/localStorageUtils';
import { checkLogOut } from './utils/api';

function App() {
  let [token, setToken] = useState(getCurrentUser())

  let navigate = useNavigate()

  const logOut = () => {
    checkLogOut(token)
    removeCurrentUser();
    setToken(null);
    navigate('/')
  };

  const logIn = (token) => {
    setCurrentUser(token)
    setToken(token)
    navigate('/')
  }

  return (
    <div className="App">
      <Routes>
        {token? (
          <>
            <Route path='/' element={<Navigate to='/home' />} />
            <Route path="/home" element={<Home exit={logOut} token={token}/>} />

            <Route path='*' element={<Navigate to='/' />} />
          </>
        ): (
          <>
            <Route path='/' element={<Navigate to='/login' />} />
            <Route path='/login' element={<Login logIn={logIn}/>} />
            <Route path='/registration' element={<Registration />} />
            
            <Route path='*' element={<Navigate to='/' />} />
          </>
        )}
      </Routes>
    </div>
  );
}

export default App;
