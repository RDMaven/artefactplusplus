import { toast } from "react-toastify";

export function newToast(success: boolean, message: string) {
  if (success) {
    toast.success(message , {
      position: "top-right",
      autoClose: 3000,
      hideProgressBar: false,
    });
  } else {
    toast.error(message, {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
      });
  }
}
