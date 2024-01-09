import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Formik } from "formik";
import "./ForgotPassword.scss";
import * as Yup from "yup";

const ForgotPassword = () => {
  const validattionSchema = Yup.object().shape({
    email: Yup.string()
      .email("Invalid email address")
      .required("Email is required")
      .max(50, "Email must be less than 50 characters")
      .matches(
        /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/,
        "Invalid email address"
      ),
  });

  return (
    <div className="forgotPassword__container flex-box">
      <div className="forgotPassword__content flex-box">
        <div className="forgotPassword__text__section flex-box-column">
          <section className="forgotPassword__header">VerveResume</section>
          <section className="forgotPassword__info flex-box-column">
            <div>Forgot your password?</div>
            <div>
              <p>
                Don't worry Resetting your password is easy, just type in the
                email you registered to ververesume
              </p>
            </div>
          </section>

          <section className="forgotPassword__email ">
            <Formik
              initialValues={{ email: "" }}
              validationSchema={validattionSchema}
              onSubmit={(email) => {
                console.log("EMAIL", email);
              }}
            >
              {({ values, errors, touched, handleChange, handleSubmit }) => (
                <form
                  onSubmit={handleSubmit}
                  className="forgotPassword__email__form flex-box-column"
                >
                  <div className="input__section flex-box-column">
                    <label>Email</label>
                    <input
                      id="email"
                      name="email"
                      value={values.email}
                      onChange={handleChange}
                      placeholder="Enter your email address"
                    />
                    {errors.email && touched.email ? (
                      <div style={{ color: "red" }} className="error-message">
                        {errors.email}
                      </div>
                    ) : null}
                  </div>
                  <button type="submit">SEND</button>
                </form>
              )}
            </Formik>
          </section>

          <section className="forgotPassword__footer">
            Did you remembered your password?
            <Link to="/login" className="forgotPassword__span">
              Try logging in
            </Link>
          </section>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
