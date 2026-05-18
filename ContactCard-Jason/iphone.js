const contact = {
  name: "Jason Mizrahi",
  company: "Champion Auto Finance",
  phoneDisplay: "+1(732)-618-2036",
  phoneUri: "+17326182036",
  email: "Jason@ChampionAutoFinance.com",
  website: "https://ChampionAutoFinance.com",
  vcardFile: "Jason-Mizrahi.vcf",
};

function buildVCard() {
  return [
    "BEGIN:VCARD",
    "VERSION:3.0",
    "N:Mizrahi;Jason;;;",
    `FN:${contact.name}`,
    `ORG:${contact.company}`,
    `TEL;TYPE=CELL:${contact.phoneDisplay}`,
    `EMAIL;TYPE=INTERNET:${contact.email}`,
    `URL:${contact.website}`,
    "NOTE:Champion Auto Finance is an auto finance service provider that helps independent dealers secure funding for used vehicles, while also assisting customers with lease buyouts and marketplace purchases-all with simple, reliable solutions.",
    "END:VCARD",
  ].join("\r\n");
}

function saveVCard() {
  const a = document.createElement("a");
  a.href = contact.vcardFile;
  a.download = contact.vcardFile;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function normalize(value) {
  const raw = value.trim();
  const phoneDigits = raw.replace(/\D/g, "");
  if (phoneDigits.length === 10) return `tel:+1${phoneDigits}`;
  if (phoneDigits.length === 11 && phoneDigits.startsWith("1")) return `tel:+${phoneDigits}`;
  if (raw.includes("@")) return `mailto:${raw}`;
  if (raw.startsWith("http")) return raw;
  return `https://${raw}`;
}

async function copy(button) {
  const text = normalize(button.dataset.copy || "");
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const temp = document.createElement("textarea");
    temp.value = text;
    temp.style.position = "absolute";
    temp.style.left = "-9999px";
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    temp.remove();
  }
  button.classList.add("is-copied");
  clearTimeout(button._timer);
  button._timer = setTimeout(() => button.classList.remove("is-copied"), 1200);
}

document.querySelectorAll(".row[data-copy]").forEach((button) => {
  button.addEventListener("click", () => copy(button));
});

document.getElementById("save-contact")?.addEventListener("click", saveVCard);
document.getElementById("save-contact-2")?.addEventListener("click", saveVCard);

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    if (action === "call") window.location.href = `tel:${contact.phoneUri}`;
    if (action === "text") window.location.href = `sms:${contact.phoneUri}`;
    if (action === "email") window.location.href = `mailto:${contact.email}`;
    if (action === "website") window.open(contact.website, "_blank", "noopener,noreferrer");
  });
});
