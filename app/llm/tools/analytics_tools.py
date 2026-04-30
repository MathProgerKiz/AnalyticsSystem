from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

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


ANALYTICS_TOOLS: tuple[ToolDefinition, ...] = (
    ToolDefinition(
        name="get_sales_summary",
        description=(
            "Общая сводка по продажам: количество заказов, выручка и средний чек."
        ),
        method_name="get_sales_summary",
        optional_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_top_selling_products",
        description="Топ товаров по количеству проданных единиц за все время.",
        method_name="get_top_selling_products",
        optional_args=("limit",),
    ),
    ToolDefinition(
        name="get_sales_by_period",
        description="Продажи по товарам за указанный период.",
        method_name="get_sales_by_period",
        required_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_top_sales_by_period",
        description="Топ товаров по выручке за указанный период.",
        method_name="get_top_sales_by_period",
        required_args=("start_date", "end_date"),
        optional_args=("limit",),
    ),
    ToolDefinition(
        name="get_top_selling_products_by_brand",
        description="Топ брендов по количеству проданных единиц.",
        method_name="get_top_selling_products_by_brand",
        optional_args=("limit",),
    ),
    ToolDefinition(
        name="get_top_selling_products_by_type",
        description="Топ типов товаров по количеству проданных единиц.",
        method_name="get_top_selling_products_by_type",
        optional_args=("limit",),
    ),
    ToolDefinition(
        name="get_sales_brand_by_period",
        description="Продажи по брендам за указанный период.",
        method_name="get_sales_brand_by_period",
        required_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_sales_type_by_period",
        description="Продажи по типам товаров за указанный период.",
        method_name="get_sales_type_by_period",
        required_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_day",
        description="Динамика продаж по дням за указанный период.",
        method_name="get_sales_dynamics_by_day",
        required_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_week",
        description="Динамика продаж по неделям за указанный период.",
        method_name="get_sales_dynamics_by_week",
        required_args=("start_date", "end_date"),
    ),
    ToolDefinition(
        name="get_sales_dynamics_by_month",
        description="Динамика продаж по месяцам за указанный период.",
        method_name="get_sales_dynamics_by_month",
        required_args=("start_date", "end_date"),
    ),
)

_TOOLS_BY_NAME: dict[str, ToolDefinition] = {
    tool.name: tool for tool in ANALYTICS_TOOLS
}


def get_analytics_tool(name: str) -> ToolDefinition:
    try:
        return _TOOLS_BY_NAME[name]
    except KeyError as exc:
        raise ValueError(f"Unknown analytics tool: {name}") from exc


def get_analytics_tool_method(
    analytics_repository: AnalyticsRepository,
    name: str,
) -> Callable[..., Any]:
    tool = get_analytics_tool(name)
    return getattr(analytics_repository, tool.method_name)
