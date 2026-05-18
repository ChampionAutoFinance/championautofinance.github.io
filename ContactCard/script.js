function normalizeCopiedValue(raw) {
  const value = raw.trim();
  if (value === "7326182036") return "tel:7326182036";
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
  openFile("Champion-Auto-Finance.vcf", "Champion-Auto-Finance.vcf");
});

document.getElementById("share-contact")?.addEventListener("click", async () => {
  const response = await fetch("Champion-Auto-Finance.vcf");
  const blob = await response.blob();
  const file = new File([blob], "Champion-Auto-Finance.vcf", {
    type: "text/vcard;charset=utf-8",
  });

  if (navigator.canShare && navigator.canShare({ files: [file] }) && navigator.share) {
    await navigator.share({
      title: "Champion Auto Finance",
      text: "Champion Auto Finance contact card",
      files: [file],
    });
    return;
  }

  openFile("Champion-Auto-Finance.vcf", "Champion-Auto-Finance.vcf");
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
