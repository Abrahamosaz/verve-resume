import React from "react";
import { Link } from "react-router-dom";
import { Formik } from "formik";
import "./ResetPassword.scss";

const ResetPassword = () => {
  return (
    <div className="resetPassword__container flex-box">
      <div className="resetPassword__content flex-box">
        <div className="resetPassword__text__section flex-box-column">
          <section className="resetPassword__header">VerveResume</section>
          <div>Reset Password</div>

          <Formik
            initialValues={{ password: "", confirmPassword: "" }}
            onSubmit={(values) => {}}
          >
            {({
              values,
              errors,
              touched,
              handleChange,
              handleSubmit,
              handleBlur,
            }) => (
              <form onSubmit={handleSubmit} className="flex-box-column">
                <div className="resetPassword__footer flex-box-column">
                  <input
                    value={values.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    type="password"
                    name="password"
                    placeholder="New Password"
                  />
                  <input
                    value={values.confirmPassword}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    type="password"
                    name="confirmPassword"
                    placeholder="ConfirmPassword"
                  />
                </div>

                <button type="submit">RESET PASSWORD</button>
              </form>
            )}
          </Formik>

          <Link to="/forgotPassword">forgot Password?</Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
