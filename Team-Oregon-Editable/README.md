# Team Oregon poster

Open this whole folder in VS Code, with Marp for VS Code installed. The included workspace settings load poster.css as the Oregon theme and enable HTML. Open poster.marp.md and its Marp preview. Opening only the Markdown without this folder can prevent the custom theme from loading.

## Where to edit

- **poster.marp.md**: readable HTML blocks containing the text and layout. Search for a member or heading to find its section.
- **poster.css**: readable CSS for typography, spacing, logo sizes and panels. The theme imports Marp’s default styles; keep that import for Marp export. The browser preview ignores that unavailable import and uses the explicit poster styles.
- **images/**: original logo files used on the current poster. Paths in the Markdown are relative, with no embedded image data.
- **index.html**: matching standalone browser preview, sharing the same CSS and images.
- **CONTRIBUTING.md**: specific content still needed from teammates.

## Updating the browser preview

The Marp file is the text/layout source. index.html is a matching snapshot. After editing text in one, copy the outer `<div class="poster"> ... </div>` block into the other to keep them in sync. CSS edits affect both immediately. Refresh the browser after saving.

## Export

Use Marp’s export command for PDF, with this folder open and the custom theme loaded. CLI alternative if installed: `marp poster.marp.md --theme poster.css --html --allow-local-files --pdf`. PDF scales text and vector artwork cleanly; raster logo/photo quality depends on original resolution. Ordinary Marp PowerPoint exports contain slide images; editable export is experimental and can change the layout.

## Sharing

Commit this folder as a unit so the CSS and images remain beside the source. No repository or remote is configured here. Use your usual GitHub Desktop or Git workflow to publish to the team repository. If this folder is inside a larger Git repository, only stage these poster files. No old drafts or full private document exports are included.

Names and professional bios are included; photos are placeholders. Confirm the remaining member details, Marko’s/William’s roles and event branding before final submission.
