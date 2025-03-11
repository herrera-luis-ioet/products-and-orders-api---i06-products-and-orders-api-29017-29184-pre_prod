{"is_source_file": true, "format": "Python", "description": "This module provides Pydantic schemas for product validation and serialization.", "external_files": [], "external_methods": [], "published": ["ProductBase", "ProductCreate", "ProductUpdate", "ProductInDB", "ProductResponse", "ProductSummary"], "classes": [{"name": "ProductBase", "description": "Base schema for product data, defining common fields for all product-related schemas."}, {"name": "ProductCreate", "description": "Schema for creating a new product; used for validating product creation requests."}, {"name": "ProductUpdate", "description": "Schema for updating an existing product; used for validating product update requests with all fields optional."}, {"name": "ProductInDB", "description": "Schema for product data as stored in the database, includes database-specific fields like id and timestamps."}, {"name": "ProductResponse", "description": "Schema for product response; used for serializing product data in API responses."}, {"name": "ProductSummary", "description": "Schema for a summary of product data; designed for including product data in other responses."}], "methods": [], "calls": [], "search-terms": ["Pydantic", "product validation", "product serialization", "product schemas"], "state": 2, "file_id": 13, "knowledge_revision": 28, "git_revision": "", "ctags": [{"_type": "tag", "name": "ProductBase", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductBase(BaseModel):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "ProductCreate", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductCreate(ProductBase):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "ProductInDB", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductInDB(ProductBase):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "ProductResponse", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductResponse(ProductInDB):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "ProductSummary", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductSummary(BaseModel):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "ProductUpdate", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^class ProductUpdate(BaseModel):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "category", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    category: Optional[str] = Field(None, description=\"Product category\", max_length=100)$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "category", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    category: Optional[str] = Field(None, description=\"Product category\", max_length=100)$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "description", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    description: Optional[str] = Field(None, description=\"Detailed product description\")$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "description", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    description: Optional[str] = Field(None, description=\"Detailed product description\")$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "dimensions", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    dimensions: Optional[str] = Field(None, description=\"Dimensions (e.g., '10x20x30 cm')\", max_/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "dimensions", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    dimensions: Optional[str] = Field(None, description=\"Dimensions (e.g., '10x20x30 cm')\", max_/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "image_url", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    image_url: Optional[str] = Field(None, description=\"URL to product image\", max_length=255)$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "image_url", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    image_url: Optional[str] = Field(None, description=\"URL to product image\", max_length=255)$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "inventory_count", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    inventory_count: Optional[int] = Field(None, description=\"Number of items in inventory\", ge=/", "language": "Python", "typeref": "typename:Optional[int]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "inventory_count", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    inventory_count: int = Field(..., description=\"Number of items in inventory\", ge=0)$/", "language": "Python", "typeref": "typename:int", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "is_active", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    is_active: Optional[bool] = Field(None, description=\"Whether the product is active and can b/", "language": "Python", "typeref": "typename:Optional[bool]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "is_active", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    is_active: bool = Field(True, description=\"Whether the product is active and can be purchase/", "language": "Python", "typeref": "typename:bool", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    model_config = ConfigDict(from_attributes=True)$/", "language": "Python", "kind": "variable", "scope": "ProductInDB", "scopeKind": "class"}, {"_type": "tag", "name": "model_config", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    model_config = ConfigDict(from_attributes=True)/", "language": "Python", "kind": "variable", "scope": "ProductSummary", "scopeKind": "class"}, {"_type": "tag", "name": "name", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    name: Optional[str] = Field(None, description=\"Product name\", max_length=255)$/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "name", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    name: str = Field(..., description=\"Product name\", max_length=255)$/", "language": "Python", "typeref": "typename:str", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "price", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    price: Decimal = Field(..., description=\"Product price in USD\", ge=0)$/", "language": "Python", "typeref": "typename:Decimal", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "price", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    price: Optional[Decimal] = Field(None, description=\"Product price in USD\", ge=0)$/", "language": "Python", "typeref": "typename:Optional[Decimal]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "sku", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    sku: Optional[str] = Field(None, description=\"Stock Keeping Unit - unique identifier\", max_l/", "language": "Python", "typeref": "typename:Optional[str]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}, {"_type": "tag", "name": "sku", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    sku: str = Field(..., description=\"Stock Keeping Unit - unique identifier\", max_length=50)$/", "language": "Python", "typeref": "typename:str", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "weight", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    weight: Optional[int] = Field(None, description=\"Weight in grams\", ge=0)$/", "language": "Python", "typeref": "typename:Optional[int]", "kind": "variable", "scope": "ProductBase", "scopeKind": "class"}, {"_type": "tag", "name": "weight", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "pattern": "/^    weight: Optional[int] = Field(None, description=\"Weight in grams\", ge=0)$/", "language": "Python", "typeref": "typename:Optional[int]", "kind": "variable", "scope": "ProductUpdate", "scopeKind": "class"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/product.py", "hash": "4b5b0a43c9969d3907722b4594009193", "format-version": 4, "code-base-name": "default", "fields": [{"name": "Optional[str] category", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] description", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] dimensions", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] image_url", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[int] inventory_count", "scope": "ProductUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "int inventory_count", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[bool] is_active", "scope": "ProductUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "bool is_active", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "model_config = ConfigDict(from_attributes=True)", "scope": "ProductInDB", "scopeKind": "class", "description": "unavailable"}, {"name": "model_config = ConfigDict(from_attributes=True)/", "scope": "ProductSummary", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] name", "scope": "ProductUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "str name", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Decimal price", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[Decimal] price", "scope": "ProductUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[str] sku", "scope": "ProductUpdate", "scopeKind": "class", "description": "unavailable"}, {"name": "str sku", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}, {"name": "Optional[int] weight", "scope": "ProductBase", "scopeKind": "class", "description": "unavailable"}], "revision_history": [{"28": ""}]}