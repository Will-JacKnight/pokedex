import { ClipLoader } from "react-spinners"
import { useNavigate } from 'react-router-dom';

function Form({handlePasswordChange, handleUsernameChange, handleSubmit, username, password, login, credentialsError, loading}) {
    const navigate = useNavigate(); // used to navigate to other pages
    // used to override the background color and position of the loader
    const ovveride ={
        backgroundColor: "white",
        position: "absolute",
        bottom: "25px",
        left: "200px",
      }

    // necessary to navigate() to signup/login page instead of using href in anchor tag because impaas does not allow redirecting to other routes
    // that are not in the backend through href
    // using navgiate() instead of href makes it possible
    function handleSignupClick(e) {
        e.preventDefault();
        navigate('/signup');
    }
    
    function handleLoginClick(e) {
        e.preventDefault();
        navigate('/login');
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
                {login && <p className='not-registered'><i>Already Registered? <span className="underline" onClick={handleSignupClick}>Sign Up</span></i></p>}
                {!login && <p className='not-registered'><i>Already Registered? <span className="underline" onClick={handleLoginClick}>Login</span></i></p>}
            
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