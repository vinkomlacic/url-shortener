# Changelog

# [next] - unreleased

# [0.2.9] - 2023-08-15
- Fix typo in STATIC_URL

# [0.2.8] - 2023-08-15
- Conform to newly defined staticfiles architecture

# [0.2.7] - 2023-08-13
- Separate static files by application name

# [0.2.6] - 2023-08-13
- Add support for CSRF in the production environment

# [0.2.5] - 2023-08-13
- Rename allowed hosts environment variable

# [0.2.4] - 2023-08-13
- Pin gunicorn version

# [0.2.3] - 2023-08-13
- Added missing gunicorn dependency to production requirements

# [0.2.2] - 2023-08-13
- Added missing settings

# [0.2.1] - 2023-08-13
- Added coverage and version badges to the README

# [0.2.0] - 2023-08-13
- Added authentication - login page, protected views, logout
- Added full CRUDLS interface
  - Update shortened URL
  - Delete shortened URL
  - Search for URLs
  - Pagination
- Switched to PostgreSQL, add .env support, and improve documentation
- Demo user support
- Added tests
- Add custom error views
- Setup GitHub workflow which runs unit tests on push

# [0.1.0] - 2023-08-12
- Initial release. Public URL shortener. Can list and add new URLs.
