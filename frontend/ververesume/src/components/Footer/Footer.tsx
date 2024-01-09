import React from "react";
import { FaLinkedin } from "react-icons/fa6";
import { IoLogoYoutube } from "react-icons/io5";
import { FaFacebook } from "react-icons/fa";
import { IoLogoTwitter } from "react-icons/io";
import { RiInstagramFill } from "react-icons/ri";
import "./Footer.scss";

const Footer = () => {
  return (
    <div className="footer__container">
      <div className="footer__content flex-box-column">
        <section className="footer__upper__section flex-box">
          <div className="footer__upper__left">VerveResume</div>
          <div className="footer__upper__right flex-box">
            <FaLinkedin className="footer__linkedin" />
            <RiInstagramFill className="footer__instagram" />
            <FaFacebook className="footer__facebook" />
            <IoLogoTwitter className="footer__twitter" />
            <IoLogoYoutube className="footer__youtube" />
          </div>
        </section>
        <hr />
        <section className="footer__lower__section flex-box">
          <div className="footer__lower__left">
            © 2024 Works Limited. All Rights Reserved.
          </div>
          <div className="footer__lower__right">
            reveResume.com is owned operated by Omorisiagbon Abraham
          </div>
        </section>
      </div>
    </div>
  );
};

export default Footer;
