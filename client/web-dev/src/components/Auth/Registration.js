import { useState } from "react"
import { Link, useNavigate } from 'react-router-dom';
import { registration } from "../../utils/api";
export default function Registration() {
    let [userName, setUserName] = useState()
    let [fullName, setFullName] = useState()
    let [email, setEmail] = useState()
    let [password, setPassword] = useState()
    let [confirmPassword, setConfirmPassword] = useState()

    let [showErrorMessage, setShowErrorMessage] = useState(false)

    let navigate = useNavigate()

    const submit = async (event) => {
        event.preventDefault()
        if (confirmPassword == password) {
            let response = await registration(userName, fullName, email, password)
            if (response.status === "OK") {
                navigate('/login')
            }
            else {
                setShowErrorMessage(true)
            }
        }
        else {
            setShowErrorMessage(true)
        }
    }

    return (
        <div className="password-page">
            <div className="login-wrapper">
                <h3>Please Log In</h3>
                <form>
                    {showErrorMessage? <div>Here some Errors</div>: ""}
                    <label>
                        <p>Username</p>
                        <input type="text" onChange={e => setUserName(e.target.value)}/>
                    </label>
                    <label>
                        <p>Full Name</p>
                        <input type="text" onChange={e => setFullName(e.target.value)}/>
                    </label>
                    <label>
                        <p>Email</p>
                        <input type="text" onChange={e => setEmail(e.target.value)}/>
                    </label>
                    <label>
                        <p>Password</p>
                        <input type="password" onChange={e => setPassword(e.target.value)}/>
                    </label>
                    <label>
                        <p>Confirm password</p>
                        <input type="password" onChange={e => setConfirmPassword(e.target.value)}/>
                    </label>
                    <div>
                        <button type="submit" onClick={(event) => submit(event)}>Submit</button>
                        <Link to='/login'><button>Back to login</button></Link>
                    </div>
                </form>
            </div>
        </div>
    )
}