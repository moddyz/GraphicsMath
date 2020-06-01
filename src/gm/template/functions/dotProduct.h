#pragma once

/// \file functions/{{ function.headerFileName }}
///
/// Dot product, or scalar product between two <em>equal-length</em> vectors.
///
/// The corresponding elements of the two vector(s) are multipled, and the products reduced via summation,
/// into a single value.
///
/// This operation can be geometrically represented as the magnitudes between the vectors and the cosine of
/// the angle between them.

#include <gm/gm.h>

{% for type in function.types -%}
{%- if not type.isScalar -%}
#include <gm/types/{{ type.headerFileName }}>
{% endif -%}
{%- endfor %}

GM_NS_OPEN

{% for interface in function.interfaces %}
/// Compute the dot product of two \ref {{ interface.ArgClass("lhs") }}, \p i_lhs and \p i_rhs, and return the result.
///
/// \return computed dot product.
GM_HOST_DEVICE inline {{ interface.returnType }} {{ function.name }}( {{ interface.typedArgs }} )
{
    return
{% for index in range(interface.Arg("lhs").type.elementSize) -%}
    {{ interface.ArgName("lhs") }}[ {{ index }} ] * {{ interface.ArgName("rhs") }}[ {{ index }} ]
{%- if index + 1 < interface.Arg("lhs").type.elementSize -%}
        +
{%- endif -%}
{%- endfor -%}
    ;
}
{% endfor %}

GM_NS_CLOSE
