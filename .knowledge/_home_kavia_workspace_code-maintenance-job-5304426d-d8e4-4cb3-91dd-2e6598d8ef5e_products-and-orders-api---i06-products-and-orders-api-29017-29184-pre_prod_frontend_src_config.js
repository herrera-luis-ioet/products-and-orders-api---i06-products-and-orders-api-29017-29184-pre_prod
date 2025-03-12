{"is_source_file": true, "format": "JavaScript", "description": "Configuration settings for the frontend application, including environmental configurations and API information.", "external_files": [], "external_methods": [], "published": ["API_BASE_URL", "API_VERSION", "API_URL", "API_ENDPOINTS", "APP_CONFIG"], "classes": [], "methods": [], "calls": [], "search-terms": ["frontend", "API configuration", "environment settings"], "state": 2, "file_id": 88, "knowledge_revision": 285, "git_revision": "", "ctags": [{"_type": "tag", "name": "API_BASE_URL", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http:\\/\\/localhost:8000';$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "API_ENDPOINTS", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^export const API_ENDPOINTS = {$/", "language": "JavaScript", "kind": "class"}, {"_type": "tag", "name": "API_URL", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^export const API_URL = `${API_BASE_URL}${API_VERSION}`;$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "API_VERSION", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^export const API_VERSION = '\\/api\\/v1';$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "APP_CONFIG", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^export const APP_CONFIG = {$/", "language": "JavaScript", "kind": "class"}, {"_type": "tag", "name": "defaultPageSize", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  defaultPageSize: 10,$/", "language": "JavaScript", "kind": "property", "scope": "APP_CONFIG", "scopeKind": "class"}, {"_type": "tag", "name": "health", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  health: `${API_BASE_URL}\\/health`,$/", "language": "JavaScript", "kind": "property", "scope": "API_ENDPOINTS", "scopeKind": "class"}, {"_type": "tag", "name": "name", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  name: 'Products and Orders',$/", "language": "JavaScript", "kind": "property", "scope": "APP_CONFIG", "scopeKind": "class"}, {"_type": "tag", "name": "orders", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  orders: `${API_URL}\\/orders`,$/", "language": "JavaScript", "kind": "property", "scope": "API_ENDPOINTS", "scopeKind": "class"}, {"_type": "tag", "name": "products", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  products: `${API_URL}\\/products`,$/", "language": "JavaScript", "kind": "property", "scope": "API_ENDPOINTS", "scopeKind": "class"}, {"_type": "tag", "name": "version", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "pattern": "/^  version: '1.0.0',$/", "language": "JavaScript", "kind": "property", "scope": "APP_CONFIG", "scopeKind": "class"}], "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/config.js", "hash": "82b1c77daed8f536ec9abe4ee3efc0f2", "format-version": 4, "code-base-name": "products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod", "fields": [{"name": "defaultPageSize: 10,", "scope": "APP_CONFIG", "scopeKind": "class", "description": "unavailable"}, {"name": "health: `${API_BASE_URL}\\/health`,", "scope": "API_ENDPOINTS", "scopeKind": "class", "description": "unavailable"}, {"name": "name: 'Products and Orders',", "scope": "APP_CONFIG", "scopeKind": "class", "description": "unavailable"}, {"name": "orders: `${API_URL}\\/orders`,", "scope": "API_ENDPOINTS", "scopeKind": "class", "description": "unavailable"}, {"name": "products: `${API_URL}\\/products`,", "scope": "API_ENDPOINTS", "scopeKind": "class", "description": "unavailable"}, {"name": "version: '1.0.0',", "scope": "APP_CONFIG", "scopeKind": "class", "description": "unavailable"}], "revision_history": [{"285": ""}]}