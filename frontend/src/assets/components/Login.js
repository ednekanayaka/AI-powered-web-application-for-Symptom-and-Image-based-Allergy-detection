import React from "react";
import "./Login.css";

/* ROUTER */
import { useNavigate } from "react-router-dom";

/* IMPORT LOGOS */
import facebookLogo from "../assets/facebook.png";
import googleLogo from "../assets/google.png";

function Login() {

  const navigate = useNavigate();

  /* LOGIN BUTTON FUNCTION */
  const handleLogin = () => {

    alert("Login button clicked"); // test message

    /* Navigate to dashboard */
    navigate("/dashboard");

  };

  return (
    <div className="login-container">

      {/* LEFT TEXT */}
      <div className="left-panel">

        <h1>WELCOME BACK</h1>

        <p>
          <b>
            Small steps every day lead to big changes.
            <br />
            Let’s continue towards a healthier you.
          </b>
        </p>

      </div>

      {/* RIGHT FORM */}
      <div className="right-panel">

        <h2>Login now</h2>

        {/* EMAIL */}
        <label>E-mail</label>
        <input
          type="email"
          placeholder="Enter your E-mail"
        />

        {/* PASSWORD */}
        <label>Password</label>
        <input
          type="password"
          placeholder="Enter password"
        />

        {/* LOGIN BUTTON */}
        <button
          className="login-btn"
          onClick={handleLogin}
        >
          LOGIN
        </button>

        {/* FORGOT PASSWORD */}
        <p className="forgot">
          Forget your password ?
        </p>

        {/* OR TEXT */}
        <p className="or">
          Or sign in with
        </p>

        {/* SOCIAL BUTTONS */}
        <div className="social-login">

          {/* FACEBOOK */}
          <button className="social-btn">

            <img
              src={facebookLogo}
              alt="Facebook"
              className="social-icon"
            />

            Facebook

          </button>

          {/* GOOGLE */}
          <button className="social-btn">

            <img
              src={googleLogo}
              alt="Google"
              className="social-icon"
            />

            Google

          </button>

        </div>

      </div>

    </div>
  );
}

export default Login;