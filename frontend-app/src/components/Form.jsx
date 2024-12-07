import { ClipLoader } from "react-spinners"

function Form({handlePasswordChange, handleUsernameChange, handleSubmit, username, password, login, credentialsError, loading}) {
    // used to override the background color and position of the loader
    const ovveride ={
        backgroundColor: "white",
        position: "absolute",
        bottom: "25px",
        left: "200px",
      }
    
      // returning the JSX for the form containg the input fields and button
    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className='form'>
                <input 
                    type="text" 
                    placeholder="User Name" 
                    value={username}
                    onChange={handleUsernameChange}
                    className='username-input'
                    required
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password}
                    onChange={handlePasswordChange}
                    className='password-input'
                    required
                />
                {/* contidionally rendering the error messages */}
                {login && credentialsError && <p className='form-error-msg'>Incorrect Credentials</p>}
                {!login && credentialsError && <p className='form-error-msg'>Username already exists</p>}
                <button type="submit" className='submit-btn'>
                    {login ? "Login" : "Sign Up"}
                </button>
                {/* contidionally rendering the error messages */}
                {login && <p className='not-registered'><i>Not registered? </i><a href='/signup'><i>Sign Up</i></a></p>}
                {!login && <p className='not-registered'><i>Already registered? </i><a href='/login'><i>Login</i></a></p>}
            
                {/* conditionally rendering the loader */}
                {loading && <ClipLoader
                  color={"black"}
                  size={50}
                  className='loader'
                  cssOverride={ovveride}
                />
                }
            </form>
        </div>
    )
}

export default Form