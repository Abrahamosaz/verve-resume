import React, { createContext, useState } from "react";
import { Outlet } from "react-router";
import ResendModel from "../components/Modals/ResendModal";

export const ResendModelContex = createContext<any>(null);

function ModelContext(): JSX.Element {
  const [resendModalState, setResendModalState] = useState<boolean>(false);

  const setResendModalStateFunc = (state: boolean) => {
    setResendModalState(state);
  };

  return (
    <ResendModelContex.Provider value={{ setResendModalState }}>
      <Outlet />
      <ResendModel
        open={resendModalState}
        onClose={() => setResendModalStateFunc(false)}
      ></ResendModel>
    </ResendModelContex.Provider>
  );
}

export default ModelContext;
