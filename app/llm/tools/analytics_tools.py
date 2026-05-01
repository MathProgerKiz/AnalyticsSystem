from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from app.analytics.analytics_repositories import AnalyticsRepository


AnalyticsToolName = Literal[
    "get_sales_summary",
    "get_top_selling_products",
    "get_sales_by_period",
    "get_top_sales_by_period",
    "get_top_selling_products_by_brand",
    "get_top_selling_products_by_type",
    "get_sales_brand_by_period",
    "get_sales_type_by_period",
    "get_sales_dynamics_by_day",
    "get_sales_dynamics_by_week",
    "get_sales_dynamics_by_month",
]


@dataclass(frozen=True)
class ToolDefinition:
    name: AnalyticsToolName
    description: str
    method_name: str
    required_args: tuple[str, ...] = ()
    optional_args: tuple[str, ...] = ()
    schema: dict[str, Any] | None = None


def _date_parameter(description: str) -> dict[str, Any]:
    return {
        "type": "string",
        "format": "date-time",
        "description": description,
    }


LIMIT_PARAMETER: dict[str, Any] = {
    "type": "integer",
    "minimum": 1,
    "default": 10,
    "description": "Максимальное количество строк в результате. По умолчанию 10.",
}

OPTIONAL_PERIOD_PARAMETERS: dict[str, dict[str, Any]] = {
    "start_date": _date_parameter(
        "Начало периода в ISO 8601, например 2026-04-01T00:00:00. "
        "Если не указано, нижняя граница не применяется."
    ),
    "end_date": _date_parameter(
        "Конец периода в ISO 8601, например 2026-04-30T23:59:59. "
        "Если не указано, верхняя граница не применяется."
    ),
}

REQUIRED_PERIOD_PARAMETERS: dict[str, dict[str, Any]] = {
    "start_date": _date_parameter(
        "Начало периода в ISO 8601, например 2026-04-01T00:00:00."
    ),
    "end_date": _date_parameter(
        "Конец периода в ISO 8601, например 2026-04-30T23:59:59."
    ),
}


def _function_schema(
    name: AnalyticsToolName,
    description: str,
    properties: dict[str, dict[str, Any]] | None = None,
    required: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties or {},
                "required": required or [],
                "additionalProperties": False,
            },
        },
    }


ANALYTICS_TOOLS: tuple[ToolDefinition, ...] = (
    ToolDefinition(
        name="get_sales_summary",
        description=(
            "Общая сводка по продажам: количество заказов, выручка и средний чек."
        ),
        method_name="get_sales_summary",
        optional_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_summary",
            "Возвращает сводку продаж: количество заказов, общую выручку и средний чек.",
            OPTIONAL_PERIOD_PARAMETERS,
        ),
    ),
    ToolDefinition(
        name="get_top_selling_products",
        description="Топ товаров по количеству проданных единиц за все время.",
        method_name="get_top_selling_products",
        optional_args=("limit",),
        schema=_function_schema(
            "get_top_selling_products",
            "Возвращает самые продаваемые товары за все время по количеству проданных единиц.",
            {"limit": LIMIT_PARAMETER},
        ),
    ),
    ToolDefinition(
        name="get_sales_by_period",
        description="Продажи по товарам за указанный период.",
        method_name="get_sales_by_period",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_by_period",
            "Возвращает продажи товаров за период с количеством проданных единиц и выручкой.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_top_sales_by_period",
        description="Топ товаров по выручке за указанный период.",
        method_name="get_top_sales_by_period",
        required_args=("start_date", "end_date"),
        optional_args=("limit",),
        schema=_function_schema(
            "get_top_sales_by_period",
            "Возвращает топ товаров за период, отсортированный по выручке.",
            {**REQUIRED_PERIOD_PARAMETERS, "limit": LIMIT_PARAMETER},
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_top_selling_products_by_brand",
        description="Топ брендов по количеству проданных единиц.",
        method_name="get_top_selling_products_by_brand",
        optional_args=("limit",),
        schema=_function_schema(
            "get_top_selling_products_by_brand",
            "Возвращает топ брендов по количеству проданных товаров за все время.",
            {"limit": LIMIT_PARAMETER},
        ),
    ),
    ToolDefinition(
        name="get_top_selling_products_by_type",
        description="Топ типов товаров по количеству проданных единиц.",
        method_name="get_top_selling_products_by_type",
        optional_args=("limit",),
        schema=_function_schema(
            "get_top_selling_products_by_type",
            "Возвращает топ типов товаров по количеству проданных товаров за все время.",
            {"limit": LIMIT_PARAMETER},
        ),
    ),
    ToolDefinition(
        name="get_sales_brand_by_period",
        description="Продажи по брендам за указанный период.",
        method_name="get_sales_brand_by_period",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_brand_by_period",
            "Возвращает продажи по брендам за период с количеством проданных единиц и выручкой.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_sales_type_by_period",
        description="Продажи по типам товаров за указанный период.",
        method_name="get_sales_type_by_period",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_type_by_period",
            "Возвращает продажи по типам товаров за период с количеством проданных единиц и выручкой.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_day",
        description="Динамика продаж по дням за указанный период.",
        method_name="get_sales_dynamics_by_day",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_dynamics_by_day",
            "Возвращает динамику продаж по дням за период.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_week",
        description="Динамика продаж по неделям за указанный период.",
        method_name="get_sales_dynamics_by_week",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_dynamics_by_week",
            "Возвращает динамику продаж по неделям за период.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_month",
        description="Динамика продаж по месяцам за указанный период.",
        method_name="get_sales_dynamics_by_month",
        required_args=("start_date", "end_date"),
        schema=_function_schema(
            "get_sales_dynamics_by_month",
            "Возвращает динамику продаж по месяцам за период.",
            REQUIRED_PERIOD_PARAMETERS,
            ["start_date", "end_date"],
        ),
    ),
)

TOOL_SCHEMA: dict[str, dict[str, Any]] = {
    tool.name: tool.schema for tool in ANALYTICS_TOOLS if tool.schema is not None
}

ANALYTICS_TOOL_SCHEMAS: tuple[dict[str, Any], ...] = tuple(TOOL_SCHEMA.values())

_TOOLS_BY_NAME: dict[str, ToolDefinition] = {
    tool.name: tool for tool in ANALYTICS_TOOLS
}


def get_analytics_tool(name: str) -> ToolDefinition:
    try:
        return _TOOLS_BY_NAME[name]
    except KeyError as exc:
        raise ValueError(f"Unknown analytics tool: {name}") from exc


def get_analytics_tool_method(
    analytics_repository: "AnalyticsRepository",
    name: str,
) -> Callable[..., Any]:
    tool = get_analytics_tool(name)

    if not hasattr(analytics_repository, tool.method_name):
        raise ValueError(f"Method {tool.method_name} not found in repository")

    return getattr(analytics_repository, tool.method_name)
