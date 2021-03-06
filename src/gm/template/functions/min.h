{% extends "functions/functionBase.h" %}
{% import "functions/functionUtils.h" as functionUtils %}

{%- block fileDoc -%}
/// Find the minimum of two input values.
///
/// If the value type is a vector, the operation will be performed on the corresponding elements.
{%- endblock %}

{% block includes %}
{{ functionUtils.typeIncludes(function) }}
#include <algorithm>
{% endblock %}

{% block body %}
{% for interface in function.interfaces %}
{% set valueA = interface.ArgName("valueA") %}
{% set valueB = interface.ArgName("valueB") %}
/// Find the minimum from the inputs \p {{ valueA }} and \p {{ valueB }}.
/// \ingroup gm_functions_{{ function.category }}
///
/// \param {{ valueA }} The first value to compare.
/// \param {{ valueB }} The second value to compare.
///
/// \return The minimum of the two inputs.
{{- functionUtils.signature(function, interface) -}}
{
{% if interface.Arg("valueA").type.isScalar -%}
    return std::min( {{ valueA }}, {{ valueB }} );
{%- elif interface.Arg("valueA").type.isVector -%}
    return {{ interface.ArgClass("valueA") }}(
{%- for index in range(interface.Arg("valueA").type.elementSize) %}
        std::min( {{ valueA }}[ {{ index }} ], {{ valueB }}[ {{ index }} ] )
{%- if index + 1 < interface.Arg("valueA").type.elementSize -%}
        ,
{%- endif -%}
{%- endfor %}
    );
{%- endif %}
}
{% endfor %}
{% endblock %}
