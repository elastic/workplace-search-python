# Changelog

## 0.3.0 (2020-02-11)

- This release is compatible with Workplace Search v7.6
- Changed the package name to `elastic-workplace-search` to follow the product
  name change ([Announcement](https://www.elastic.co/blog/elastic-enterprise-search-updates-for-7-6-0))
- Changed API path from `/api/v1/ent/` to `/api/ws/v1/`. If previously
  using a custom API endpoint you may need to update accordingly.

## 0.2.0 (2019-10-17)

- Changed the `index_documents` and `delete_documents`
  API methods to be namespaced under `client.documents`.
  API calls will need to be updated accordingly.
- Added support for the Permissions API ([#20](https://github.com/elastic/workplace-search-python/pull/20))

## 0.1.0 (2019-08-19)

- Changed "Swiftype" references to "Elastic" in the README and code
- Changed the package name to `elastic-enterprise-search`
- Changed versioning to be pre-release again (0.1.0) since we are not yet GA
  similar to App Search
- Added analytics HTTP headers `Swiftype-X-Client` and `Swiftype-X-Client-Version`
- Added Circle CI
