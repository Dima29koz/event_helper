import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { checkLogin } from '../../utils/api';
export default function Login({logIn}) {
    let [userName, setUserName] = useState()
    let [password, setPassword] = useState()

    let [showError, setShowError] = useState(false)

    let navigate = useNavigate()

    const submit = async (event) => {
        event.preventDefault()
        let response = await checkLogin(userName, password)
        if (response.status === "OK") {
            logIn(response.data.token)
        }
        else {
            setShowError(true)
        }
    }

    return (
        <div className="password-page">
            <div className="login-wrapper">
                <h3>Please Log In</h3>
                <form>
                    {showError? <div>Here some Errors</div>: ""}
                    <label>
                        <p>Username</p>
                        <input type="text" onChange={e => setUserName(e.target.value)}/>
                    </label>
                    <label>
                        <p>Password</p>
                        <input type="password" onChange={e => setPassword(e.target.value)}/>
                    </label>
                    <div>
                        <button type="submit" onClick={(event) => submit(event)}>Submit</button>
                    </div>
                    <div>Laboris in proident eiusmod magna cupidatat <Link to='/registration'>registration</Link> duis qui nostrud aliqua minim ipsum.</div>
                </form>
            </div>
        </div>
    )
}