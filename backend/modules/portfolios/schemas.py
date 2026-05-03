from pydantic import BaseModel


class FAQsSchema(BaseModel):
    question: str
    answer: str


class RequirementsSchema(BaseModel):
    requirement: str
    is_required: bool


class PortfoliosSchema(BaseModel):
    title: str
    category: str
    subcategory: str
    initial_status: str
    tags: list[str]

    pricing_mode: str
    price_basic: str
    price_standard: str | None
    price_premium: str | None

    package_name_basic: str
    package_name_standard: str | None
    package_name_premium: str | None

    description_basic: str
    description_standard: str | None
    description_premium: str | None

    delivery_basic: str
    delivery_standard: str | None
    delivery_premium: str | None

    revisions_basic: str
    revisions_standard: str | None
    revisions_premium: str | None

    description: str

    faqs: list[FAQsSchema]
    requirements: list[RequirementsSchema]

    images: list[str | None]


class PortfoliosCreateSchema(PortfoliosSchema):
    user_id: int


class PortfoliosUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
