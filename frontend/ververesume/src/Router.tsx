import {
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import Home from "./Home";
import Login from "./pages/Login/Login";
import Templates from "./pages/Templates/Templates";
import ForgotPassword from "./pages/ForgotPassword/ForgotPassword";
import ResetPassword from "./pages/ResetPassword/ResetPassword";
import Wrapper from "./components/HomeWrapper/Wrapper";
import ModelContext from "./contexts/ModelContext";
import ConfirmEmail from "./pages/ConfirmEmail/ConfirmEmail";

function Router() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route element={<ModelContext />}>
        <Route path="/" element={<Home />}>
          <Route path="forgotPassword" element={<ForgotPassword />} />
          <Route path="resetPassword" element={<ResetPassword />} />
          <Route path="confirmEmail/:token" element={<ConfirmEmail />} />
          <Route path="login" element={<Login />} />
          <Route index element={<Wrapper />}></Route>
          <Route path="templates" element={<Templates />} />
        </Route>
      </Route>
    )
  );

  return <RouterProvider router={router} />;
}

export default Router;
