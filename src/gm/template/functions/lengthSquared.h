#pragma once

/// \file functions/{{ function.headerFileName }}
///
/// Compute the length squared of a vector, defined as the <em>sum of the squares</em> of <em>each vector element</em>.
///
/// Can also be represented as the dot product (see \ref functions/dotProduct.h) of the vector with itself.

#include <gm/gm.h>

{% for vectorType in function.types -%}
#include <gm/types/{{ vectorType.headerFileName }}>
{% endfor %}

#include <gm/functions/dotProduct.h>

GM_NS_OPEN

{% for vectorType in function.types %}
/// Compute the length squared of the vector \p i_vector.
///
/// \return the length squared of the vector.
GM_HOST_DEVICE inline {{ vectorType.elementType.className }} {{ function.name }}(
    const {{ vectorType.className }}& i_vector )
{
    return DotProduct( i_vector, i_vector );
}
{% endfor %}

GM_NS_CLOSE
