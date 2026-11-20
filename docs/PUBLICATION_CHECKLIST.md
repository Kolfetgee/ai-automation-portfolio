# Publication checklist / next owner action

The new public GitHub repository **does not yet exist** at the time of this local package. Creating it is a separate user-controlled GitHub action because the current connector cannot create repositories.

## Create the clean repository

1. In GitHub, select **New repository** (`https://github.com/new`).
2. Owner: **Kolfetgee**. Repository name: **ai-automation-portfolio**.
3. Visibility: **Public** (only after reviewing content of this clean package).
4. **Enable "Add a README file"** to initialize the `main` branch. Leave `.gitignore` and license unchecked.
5. Send the new repository URL back to ChatGPT. The connected GitHub tools can then add the reviewed portfolio files to that existing repository. If you prefer to publish manually, use the commands below instead.

## Optional manual Git workflow

Clone the initialized repo, then copy the **contents** of the extracted portfolio folder into it (replacing the starter README):

```bash
git clone https://github.com/Kolfetgee/ai-automation-portfolio.git
cd ai-automation-portfolio
# Copy the contents of the prepared portfolio folder here.
python -W error::ResourceWarning -m unittest discover -s tests -v
git add .
git commit -m "Initial synthetic AI automation portfolio"
git push origin main
```

Run the test suite **before** the push:

```bash
python -W error::ResourceWarning -m unittest discover -s tests -v
```

## After publication

- Confirm every README link opens without authentication.
- Check GitHub Actions on `main`; the CI result is not assumed PASS until observed.
- Review `git ls-files` and scan new Git history for credentials, emails, `.env`, `.sqlite3`, backups, personal data, private links and copyrighted assets.
- Keep the original AUTO-SCOUT, ORION, MAI repositories **private**; do not change visibility or merge their unfinished PRs.
- Only after confirming the new public link, update the job application letter and CV to reference it.

## License decision

No public software license was chosen. If you want others to reuse the code, pick an appropriate license explicitly and consider the provenance of any dependencies/assets first. A public repository without a license is still viewable by prospective employers.
