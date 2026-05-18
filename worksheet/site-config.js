const isLocalHost = ["localhost", "127.0.0.1"].includes(window.location.hostname);

window.CAF_CONFIG = window.CAF_CONFIG || {
  formEndpoint: isLocalHost
    ? "http://127.0.0.1:8788/api/worksheet-submit"
    : "https://zuuxpqaxbnliczpptpwb.supabase.co/functions/v1/worksheet-submit",
};
