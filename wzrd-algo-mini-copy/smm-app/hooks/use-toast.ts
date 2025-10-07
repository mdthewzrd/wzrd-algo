import { toast } from "sonner";

export const useToast = () => {
  return {
    toast: {
      success: (message: string) => toast.success(message),
      error: (message: string) => toast.error(message),
      warning: (message: string) => toast.warning(message),
      info: (message: string) => toast.info(message),
    },
    dismiss: toast.dismiss,
  };
};