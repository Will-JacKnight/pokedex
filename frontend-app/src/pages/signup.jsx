import titleImg from '../images/signup-text.png';
import { useState } from 'react';
import Form from '../components/Form';
import {useNavigate} from 'react-router-dom';

function SignUp() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [credentialsError, setCredentialsError] = useState(false);

    const navigate = useNavigate();

    function handleUsernameChange(e) {
        setUsername(e.target.value);
    }

    function handlePasswordChange(e) {
        setPassword(e.target.value);
    }   

    async function handleSubmit(e) {
        e.preventDefault();
        const response = await fetch('http://127.0.0.1:5000/signup', {
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
            login={false}
            credentialsError={credentialsError}
        />
    </div>
    </>
    )
}

export default SignUp