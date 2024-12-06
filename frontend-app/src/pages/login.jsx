import titleImg from '../images/login-text.png';
import { useState } from 'react';
import {useNavigate} from 'react-router-dom'
import Form from '../components/Form';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [credentialsError, setCredentialsError] = useState(false);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    function handleUsernameChange(e) {
        setUsername(e.target.value);
    }

    function handlePasswordChange(e) {
        setPassword(e.target.value);
    }   

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/login`, {
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
        if(data.success) {
            setCredentialsError(false);
            sessionStorage.setItem('access_token', data.access_token);
            navigate('/');
        } else {
            setCredentialsError(true);
        }   
        console.log(data); 
    }

    return(
    <>
    <div className="container">
        <img src={titleImg} alt='title' className='title-img'/>
        <Form 
            handlePasswordChange={handlePasswordChange} 
            handleUsernameChange={handleUsernameChange} 
            handleSubmit={handleSubmit} username={username} 
            password={password}
            login={true}
            credentialsError={credentialsError}
            loading={loading}
        />

    </div>
    </>
    )
}

export default Login