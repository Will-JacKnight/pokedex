function Form({handlePasswordChange, handleUsernameChange, handleSubmit, username, password, login, credentialsError}) {
    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className='form'>
                <input 
                    type="text" 
                    placeholder="User Name" 
                    value={username}
                    onChange={handleUsernameChange}
                    className='username-input'
                />

                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password}
                    onChange={handlePasswordChange}
                    className='password-input'
                />
                {login && credentialsError && <p className='form-error-msg'>Incorrect Credentials</p>}
                {!login && credentialsError && <p className='form-error-msg'>Username already exists</p>}
                <button type="submit" className='submit-btn'>
                    {login ? "Login" : "Sign Up"}
                </button>
                {login && <p className='not-registered'><i>Not registered? </i><a href='/signup'><i>Sign Up</i></a></p>}
                {!login && <p className='not-registered'><i>Already registered? </i><a href='/login'><i>Login</i></a></p>}
            
            </form>
        </div>
    )
}

export default Form