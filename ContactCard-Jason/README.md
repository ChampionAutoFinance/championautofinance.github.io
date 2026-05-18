# Contact Card | Jason Mizrahi

## Upload to GoDaddy cPanel

1. Open cPanel File Manager.
2. Upload the contents of this folder into the target location.
3. Make sure `index.html` is in the root of the folder you want to serve.
4. If you are using a subdomain, point the subdomain document root at this folder.
5. If you are using a subfolder, upload the files into that folder and use the folder URL.

## Where it can live

- `ContactCard.championautofinance.com`
- `championautofinance.com/ContactCard`

Both work because the page uses relative asset paths.

## Editing contact info later

Open:

- `index.html` for visible text
- `script.js` for the downloadable vCard details

Update the name, phone, email, and website in both files so the on-page text and the saved contact match.

## Replacing the logo later

- Replace the SVG in `assets/favicon.svg`
- Replace the SVG preview in `assets/og-image.svg`
- If you want a different top mark, edit the inline SVG in `index.html`

## Notes

- The Save Contact button downloads a `.vcf` file that works on iPhone and Android.
- No build tools, frameworks, or backend code are required.
