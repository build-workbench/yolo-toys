## MODIFIED Requirements

### Requirement: GitHub Pages SHALL act as a landing surface
The published site SHALL introduce the project in Chinese with a clear value proposition, fast entry paths, and curated links into deeper documentation instead of duplicating the entire README verbatim. The site SHALL maintain only the Chinese (`docs/zh/`) documentation tree and SHALL NOT maintain a parallel English tree.

#### Scenario: New visitor lands on the site
- **WHEN** a user opens the GitHub Pages homepage
- **THEN** the page redirects into the Chinese site (`/zh/`) and explains what YOLO-Toys is, why it matters, how to try it quickly, and where to go next for architecture or operational details

#### Scenario: English documentation tree is not maintained
- **WHEN** a contributor or build process inspects the Pages source
- **THEN** no parallel English documentation tree (`docs/en/`) exists and no English locale is configured in the VitePress config

### Requirement: Public repository metadata SHALL be aligned
The GitHub repository description, homepage URL, and topic tags SHALL be aligned with the repository README and GitHub Pages positioning, presented in Chinese for the project's target audience.

#### Scenario: Viewing the repository summary card
- **WHEN** a user sees the repository on GitHub or in search results
- **THEN** the description, homepage, and topics accurately reflect the project's final Chinese positioning and point to the published site

### Requirement: Public content surfaces SHALL have distinct roles
The repository SHALL define distinct jobs for README, GitHub Pages, docs, changelog, and governance files so the same content is not duplicated across all surfaces. README SHALL be a single Chinese entry point with no language-switch link to a translated sibling.

#### Scenario: Finding project information
- **WHEN** a contributor or user navigates between README, site pages, docs, and changelog
- **THEN** each surface provides a different layer of information in Chinese and links to the correct deeper source instead of restating the same content or offering a parallel English surface

#### Scenario: README is the single Chinese entry point
- **WHEN** a visitor opens `README.md` on GitHub
- **THEN** the README is in Chinese, no `README.zh-CN.md` sibling exists, and no link switches to an English README
