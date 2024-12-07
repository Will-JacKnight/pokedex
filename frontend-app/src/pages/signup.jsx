import titleImg from '../images/signup-text.png';
import { useState } from 'react';
import Form from '../components/Form';
import {useNavigate} from 'react-router-dom';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


function SignUp() {
    const [username, setUsername] = useState(""); // state to store username
    const [password, setPassword] = useState(""); // state to store password
    const [credentialsError, setCredentialsError] = useState(false); // state to store credentials error (default false)
    const [loading, setLoading] = useState(false); // state to store loading status (defualt false)


    const navigate = useNavigate(); // useNavigate to navigate to other pages

    // function to handle username change and update state
    function handleUsernameChange(e) {
        setUsername(e.target.value);
    }

    // function to handle password change and update state
    function handlePasswordChange(e) {
        setPassword(e.target.value);
    }   

    // function to handle form submission
    async function handleSubmit(e) {
        e.preventDefault(); // prevents default form submission
        setLoading(true);
        // submit post request to backend with username and password
        const response = await fetch(`${API_BASE_URL}/signup`, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });
        const data = await response.json();
        setLoading(false);
        // if response is successful, set credentialsError to false and navigate to home page
        if(data.success) {
            setCredentialsError(false);
            sessionStorage.setItem('access_token', data.access_token);
            navigate('/');
        // if response is not successful, set credentialsError to true
        } else {
            setCredentialsError(true);
        }
        console.log(data);

    }

    // return the JSX for the signup page
    return(
    <>
    <div className="container">
        <img src={titleImg} alt='title' className='title-img'/>
        <Form 
            handlePasswordChange={handlePasswordChange} 
            handleUsernameChange={handleUsernameChange} 
            handleSubmit={handleSubmit} username={username} 
            password={password}
            login={false}
            credentialsError={credentialsError}
            loading={loading}
        />
    </div>
    </>
    )
}

export default SignUp