#pragma once

/// \file functions/{{ function.headerFileName }}
/// \ingroup gm_functions_linearAlgebra
///
/// Set scale on a transformation matrix.

#include <gm/gm.h>

{% for type in function.types -%}
{%- if not type.isScalar -%}
#include <gm/types/{{ type.headerFileName }}>
{%- endif %}
{% endfor %}

GM_NS_OPEN

{% for interface in function.interfaces %}
/// Set the scale \p {{ interface.ArgName("vector") }} onto the transformation matrix \p {{ interface.ArgName("matrix") }}.
/// \ingroup gm_functions_linearAlgebra
GM_HOST_DEVICE inline {{ interface.returnType }} {{ function.name }}( {{ interface.typedArgs }} )
{
{% for row in range(interface.ArgType("matrix").shape[0]) -%}
{% for col in range(interface.ArgType("matrix").shape[1]) -%}
{% if row == col and row + 1 < interface.ArgType("matrix").shape[0] -%}
    {{ interface.ArgName("matrix") }}( {{ row }}, {{ col }} ) = {{ interface.ArgName("vector") }}[ {{ row }} ];
{%- endif %}
{%- endfor -%}
{%- endfor -%}
}
{% endfor %}

GM_NS_CLOSE
