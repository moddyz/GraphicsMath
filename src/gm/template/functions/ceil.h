{% extends "functions/functionBase.h" %}
{% import "functions/functionUtils.h" as functionUtils %}

{%- block fileDoc -%}
/// Round the input upwards to the nearest integral value greater than the input.
///
/// If the value type is a vector, the operation will be performed on each element.
{%- endblock %}

{% block includes %}
{{ functionUtils.typeIncludes(function) }}
#include <cmath>
{% endblock %}

{% block body %}
{% for interface in function.interfaces %}
{% set value = interface.ArgName("value") %}
{% set valueType = interface.ArgType("value") %}
/// Ceil the input \ref {{ interface.ArgClass("value") }} \p {{ value }},
/// rounding upwards to the nearest integral value.
/// \ingroup gm_functions_{{ function.category }}
///
/// \return The upward rounded input value.
{{- functionUtils.signature(function, interface) -}}
{
{% if valueType.isScalar -%}
    return std::ceil( {{ value }} );
{%- elif valueType.isVector -%}
    return {{ interface.ArgClass("value") }}(
{%- for index in range(valueType.elementSize) %}
        std::ceil( {{ value }}[ {{ index }} ] )
{%- if index + 1 < valueType.elementSize -%}
        ,
{%- endif -%}
{%- endfor %}
    );
{%- endif %}
}
{% endfor %}
{% endblock %}
