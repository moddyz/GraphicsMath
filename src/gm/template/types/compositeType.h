#pragma once

/// \file {{ context.headerFileName }}

#include <sstream>

#include <gm/gm.h>

{% for element in context.elements -%}
{% if element.type.isVector or element.type.isComposite -%}
#include <gm/types/{{ element.type.headerFileName }}>
{%- endif %}
{% endfor %}

{% for include in context.extraIncludes -%}
#include {{ include }}
{% endfor %}

GM_NS_OPEN

/// \class {{ context.className }}
class {{ context.className }} final
{
public:
    /// Default constructor.
    {{ context.className }}()  = default;

    /// Destructor.
    ~{{ context.className }}() = default;

    /// Element-wise constructor.
    explicit {{ context.className }}(
{% for index in range(context.elementSize) -%}
        const {{ context.elements[ index ].type.className }}& i_{{ context.elements[ index ].name }}
{%- if index + 1 < context.elementSize -%}
        ,
{%- endif -%}
{%- endfor %}
    )
{% for index in range(context.elementSize) -%}
{%- if index + 1 < context.elementSize -%}
        :
{%- else -%}
        ,
{%- endif -%}
        m_{{ context.elements[ index ].name }}( i_{{ context.elements[ index ].name }} )
{%- endfor %}
    {
    }

{% for element in context.elements %}
    /// Const accessor for "{{ element.name }}".
    GM_HOST_DEVICE const {{ element.type.className }}& {{ element.name[0].upper() + element.name[1:] }}() const
    {
        return m_{{ element.name }};
    }

    /// Mutable accessor for "{{ element.name }}".
    GM_HOST_DEVICE {{ element.type.className }}& {{ element.name[0].upper() + element.name[1:] }}()
    {
        return m_{{ element.name }};
    }
{% endfor %}

    /// Get the string representation.  For debugging purposes.
    std::string GetString() const
    {
        std::stringstream ss;
        ss << "{{ context.className }}( ";
{%- for index in range(context.elementSize) -%}
{%- if context.elements[ index ].type.isVector or context.elements[ index ].type.isComposite %}
        ss << m_{{ context.elements[ index ].name }}.GetString();
{%- elif context.elements[ index ].type.isScalar %}
        ss << m_{{ context.elements[ index ].name }};
{%- endif %}
{%- if index + 1 < context.elementSize -%}
        ss << ", ";
{%- endif %}
{%- endfor %}
        ss << " )";
        return ss.str();
    }

private:
    /// Element members.
{% for element in context.elements -%}
    {{ element.type.className }} m_{{ element.name }}
{%- if element.defaultValue -%}
    = {{ element.defaultValue }}
{%- endif -%}
    ;
{%- endfor %}
};

GM_NS_CLOSE