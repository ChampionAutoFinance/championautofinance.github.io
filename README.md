# Champion Auto Finance GitHub Pages

Static GitHub Pages build of the public Champion Auto Finance site.

The original backup is a WordPress/cPanel hosting backup. WordPress uses PHP plus MySQL, so the raw files under `public_html/championautofinance.com` cannot run on GitHub Pages. This repo publishes the rendered public pages and required static assets instead.

Included:
- Home
- `how-it-works/`
- `about-us/`
- `faqs/`
- `dealer-partners/`
- `contact-us/`
- `privacy-policy/`
- Existing static tools: `worksheet/`, `structure/`, `dealertools/`, `ContactCard/`, `ContactCard-Jason/`, `ContactCard-Joe/`

Excluded:
- `wp-config.php`
- WordPress PHP runtime entry points
- SSL keys and certificates
- Logs, cPanel data, and private server files
- MySQL dump files

Forms that depend on WordPress/Gravity Forms PHP endpoints may need a separate hosted backend if they should submit from GitHub Pages.
