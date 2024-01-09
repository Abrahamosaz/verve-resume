import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryFunction,
} from "react-query";
import { request } from "../utils/axios-utils";

const loginRequest = async (formData: any) => {
  return request({
    url: "auth/login",
    method: "POST",
    data: formData,
  });
};

export const useLogin = (onError: any, onSuccess: any) => {
  return useMutation(loginRequest, {
    onError,
    onSuccess,
  });
};

const activateLinkRequest = async (formData: any) => {
  return request({
    url: "/auth/resendConfirmEmail",
    method: "POST",
    data: formData,
  });
};

export const useActivationLink = (onError: any, onSuccess: any) => {
  return useMutation(activateLinkRequest, {
    onError,
    onSuccess,
  });
};
