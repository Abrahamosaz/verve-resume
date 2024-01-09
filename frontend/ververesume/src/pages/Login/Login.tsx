import React, { useContext } from "react";
import { ResendModelContex } from "../../contexts/ModelContext";
import { FcGoogle } from "react-icons/fc";
import { FaFacebook } from "react-icons/fa";
import { Toaster, toast } from "react-hot-toast";
import "./Login.scss";
import { useLogin } from "../../hooks/useApiMethods";
import { useFormik } from "formik";
import * as Yup from "yup";
import { BeatLoader } from "react-spinners";
import { useNavigate, Link } from "react-router-dom";
import Cookies from "js-cookie";

interface LoginFormData {
  email: string;
  password: string;
}

const Login = () => {
  const { setResendModalState } = useContext(ResendModelContex);
  const navigate = useNavigate();
  const redirectUserPath = "/templates";
  const validationSchema = Yup.object().shape({
    email: Yup.string()
      .email("Invalid email address")
      .required("Email is required")
      .max(50, "Email must be less than 50 characters")
      .matches(
        /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/,
        "Invalid email address"
      ),

    password: Yup.string()
      .min(8, "Password must be at least 8 characters")
      .max(50, "Password must be less than 50 characters")

      .required("Password is required"),
  });
  const formik = useFormik({
    initialValues: { email: "", password: "" },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      handleSubmit(values);
    },
  });

  const onLoginError = (error: any) => {
    const message = error.response.data.error;
    toast.error(`Login Unsuccessful! ${message}`);
  };

  const onLoginSuccess = async (data: any) => {
    const user = data.data.user;
    const token = data.data.token;
    console.log("user", user);
    let expireTime = new Date().getTime() + 3 * 60 * 60 * 1000;

    if (user.emailConfirmed) {
      Cookies.set("jwt", token, { expires: expireTime });
      toast.success("Login successful!");
    }

    localStorage.setItem("user", JSON.stringify(user));

    if (user.emailConfirmed && !user.isAdmin) {
      navigate(redirectUserPath, { replace: true });
    } else {
      setResendModalState(true);
    }
  };

  const {
    mutate: login,
    isLoading: loginLoading,
    isError: loginError,
    isSuccess: loginSuccess,
  } = useLogin(onLoginError, onLoginSuccess);

  const handleSubmit = async (values: LoginFormData) => {
    console.log("Form data", values);
    try {
      login(values);
    } catch (err) {
      console.log("error", err);
    }
  };

  return (
    <div className="login-container flex-box">
      <div className="login-content flex-box-column">
        <div className="upper-section flex-box-column">
          <section className="nerve-logo">
            <h1>NerveResume</h1>
          </section>

          <section className="nerve-form">
            <h2>Sign-in to Your Account</h2>

            <form
              className="login-form flex-box-column"
              onSubmit={formik.handleSubmit}
            >
              <input
                type="text"
                id="email"
                name="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                placeholder="Email Address"
              />
              {formik.errors.email && formik.touched.email ? (
                <div className="error-message">{formik.errors.email}</div>
              ) : null}

              <input
                id="password"
                type="password"
                name="password"
                value={formik.values.password}
                onChange={formik.handleChange}
                placeholder="Password (must be between 6-16 characters)"
              />
              {formik.errors.password && formik.touched.password ? (
                <div className="error-message">{formik.errors.password}</div>
              ) : null}

              <section className="nerve-button flex-box">
                <button disabled={loginLoading} type="submit">
                  {loginLoading ? (
                    <BeatLoader size={10} color="white" loading />
                  ) : (
                    <span>SIGN IN</span>
                  )}
                </button>
              </section>
            </form>
          </section>

          <section className="login-section flex-box-column">
            <div className="google-login flex-box external-link">
              <FcGoogle />
              <h2>Sign in with Google</h2>
            </div>
            <div className="facebook-login flex-box external-link">
              <FaFacebook />
              <h2>Sign in with Facebook</h2>
            </div>
          </section>
        </div>
        <div className="lower-section flex-box-column">
          <div className="forget-password">
            <Link to="/forgotPassword">Forgot Password?</Link>
          </div>
          <div className="account-new">
            Don't have an account?{" "}
            <span className="login-button">
              <Link to="/signup">Sign Up</Link>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
