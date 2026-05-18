function normalizeCopiedValue(raw) {
  const value = raw.trim();
  const phoneDigits = value.replace(/\D/g, "");
  if (phoneDigits.length === 10) return `tel:+1${phoneDigits}`;
  if (phoneDigits.length === 11 && phoneDigits.startsWith("1")) return `tel:+${phoneDigits}`;
  if (value.includes("@")) return `mailto:${value}`;
  if (value.startsWith("http")) return value;
  return `https://${value}`;
}

function openFile(filename, downloadName) {
  const link = document.createElement("a");
  link.href = filename;
  link.download = downloadName;
  document.body.appendChild(link);
  link.click();
  link.remove();
}

document.getElementById("save-contact")?.addEventListener("click", () => {
  openFile("Joe-Mizrahi.vcf", "Joe-Mizrahi.vcf");
});

document.getElementById("share-contact")?.addEventListener("click", async () => {
  const response = await fetch("Joe-Mizrahi.vcf");
  const blob = await response.blob();
  const file = new File([blob], "Joe-Mizrahi.vcf", {
    type: "text/vcard;charset=utf-8",
  });

  if (navigator.canShare && navigator.canShare({ files: [file] }) && navigator.share) {
    await navigator.share({
      title: "Joe Mizrahi",
      text: "Joe Mizrahi contact card for Champion Auto Finance",
      files: [file],
    });
    return;
  }

  openFile("Joe-Mizrahi.vcf", "Joe-Mizrahi.vcf");
});

async function copyContactValue(button) {
  const value = normalizeCopiedValue(button.dataset.copy || "");
  if (!value) return;

  try {
    await navigator.clipboard.writeText(value);
    button.classList.add("is-copied");
    window.clearTimeout(button._copyTimer);
    button._copyTimer = window.setTimeout(() => {
      button.classList.remove("is-copied");
    }, 1400);
  } catch {
    const temp = document.createElement("textarea");
    temp.value = value;
    temp.setAttribute("readonly", "");
    temp.style.position = "absolute";
    temp.style.left = "-9999px";
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    temp.remove();
    button.classList.add("is-copied");
    window.clearTimeout(button._copyTimer);
    button._copyTimer = window.setTimeout(() => {
      button.classList.remove("is-copied");
    }, 1400);
  }
}

document.querySelectorAll(".contact-item[data-copy]").forEach((button) => {
  button.addEventListener("click", () => copyContactValue(button));
});

function closeCallTextMenus() {
  document.querySelectorAll("[data-call-text]").forEach((button) => {
    button.setAttribute("aria-expanded", "false");
    button.nextElementSibling.hidden = true;
  });
}

document.querySelectorAll("[data-call-text]").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    const menu = button.nextElementSibling;
    const willOpen = menu.hidden;
    closeCallTextMenus();
    button.setAttribute("aria-expanded", String(willOpen));
    menu.hidden = !willOpen;
  });
});

document.addEventListener("click", closeCallTextMenus);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeCallTextMenus();
});
