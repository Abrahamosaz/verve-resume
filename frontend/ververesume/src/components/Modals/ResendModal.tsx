import React, { useContext, useState, useEffect } from "react";
import { IoMdClose } from "react-icons/io";
import { AiOutlineDelete, AiOutlinePlus } from "react-icons/ai";
import { toast } from "react-hot-toast";
import { useActivationLink } from "../../hooks/useApiMethods";
import { IoIosArrowBack } from "react-icons/io";
import { ClipLoader } from "react-spinners";
import Mail from "../../assets/mail.jpg";
import "./Modal.scss";

interface ModalProps {
  open: boolean;
  onClose: () => void;
}

const ResendModal: React.FC<ModalProps> = ({ open, onClose }) => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  console.log("user", user.email);
  const onActivationLinkError = async (error: any) => {
    const message = error.response.data.message;
    toast.error(`Sending Unsuccessful! ${message}`);
  };

  const onActivationLinkSuccess = async () => {
    toast.success(
      `activation link sent Successful! Please check your email to confirm...`
    );
  };

  const {
    mutate: activationLink,
    isLoading: activationLinkLoading,
    isError: activationLinkError,
    isSuccess: activationLinkSuccess,
  } = useActivationLink(onActivationLinkError, onActivationLinkSuccess);

  if (!open) return null;

  return (
    <div className="resendModal__container">
      <div
        onClick={(e) => {
          e.stopPropagation();
        }}
        className="resendModal__content"
      >
        <div className="resendModal__modal flex-box-column">
          <div className="resendModal__header">
            <img src={Mail} alt="mail" />
          </div>
          <div className="resendModal__title">Check Email</div>
          <div className="resendModal__body">
            <p>
              please check your email inbox and click on the provided link to
              reset confirm your email. if don't receive email{" "}
              <a
                onClick={() => activationLink({ email: user.email })}
                style={{ color: "#020381", textDecoration: "underline" }}
              >
                click here to resend
              </a>
            </p>
          </div>

          <div onClick={onClose} className="resendModal__footer flex-box">
            <IoIosArrowBack />
            <span> Back to Login</span>
          </div>

          <div className="resendModal__loader">
            {activationLinkLoading && <ClipLoader loading />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResendModal;
