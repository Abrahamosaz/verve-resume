import React from "react";
import "./NavBar";
import "./NavBar.scss";

const NavBar = () => {
  return (
    <div className="navbar__container">
      <div className="navbar__content flex-box">
        <div className="navbar__left">VerveResume</div>
        <div className="navbar__right flex-box">
          <button className="navbar__resume__build navbar__button">
            Build My Resume
          </button>
          <button className="navbar__login navbar__button">Login</button>
        </div>
      </div>
    </div>
  );
};

export default NavBar;
