{"is_source_file": true, "format": "JavaScript (JSX)", "description": "A React component that displays the details of a specific product, including fetching product data by ID from a product context and rendering the UI with appropriate loading and error states.", "external_files": ["../components/Layout", "../context/ProductContext"], "external_methods": ["getProductById"], "published": ["ProductDetailPage"], "classes": [], "methods": [{"name": "fetchProduct", "description": "An asynchronous function that fetches product data based on the product ID, handles loading states, errors and updates the product state."}, {"name": "handleGoBack", "description": "A function to navigate back to the products list."}], "calls": ["useNavigate", "useParams", "useProductContext"], "search-terms": ["ProductDetailPage", "fetchProduct", "handleGoBack"], "state": 2, "file_id": 86, "knowledge_revision": 294, "git_revision": "e21f1a9302570a3a65097869419abef22b847dd9", "revision_history": [{"269": ""}, {"282": ""}, {"294": "e21f1a9302570a3a65097869419abef22b847dd9"}], "ctags": [{"_type": "tag", "name": "ProductDetailPage", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^const ProductDetailPage = () => {$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "handleGoBack", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^          onClick={handleGoBack}$/", "language": "JavaScript", "kind": "field", "scope": "onClick", "scopeKind": "class"}, {"_type": "tag", "name": "handleGoBack", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^  const handleGoBack = () => {$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "navigate", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^  const navigate = useNavigate();$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "setError", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^  const [error, setError] = useState(null);$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "setLoading", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^  const [loading, setLoading] = useState(true);$/", "language": "JavaScript", "kind": "constant"}, {"_type": "tag", "name": "setProduct", "path": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "pattern": "/^  const [product, setProduct] = useState(null);$/", "language": "JavaScript", "kind": "constant"}], "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/frontend/src/pages/ProductDetailPage.jsx", "hash": "7d28e546a3e761826e923bafb156b07e", "format-version": 4, "code-base-name": "products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod", "fields": [{"name": "onClick={handleGoBack}", "scope": "onClick", "scopeKind": "class", "description": "unavailable"}]}