const isLocalHost = ["localhost", "127.0.0.1"].includes(window.location.hostname);

window.CAF_CONFIG = window.CAF_CONFIG || {
  formEndpoint: isLocalHost
    ? "__LOCAL_FORM_ENDPOINT__"
    : "__PRODUCTION_FORM_ENDPOINT__",
};
