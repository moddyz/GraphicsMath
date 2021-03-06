#include <pybind11/pybind11.h>

#include <gm/functions/{{ function.headerFileName }}>

// Python bindings for {{ function.name }}.

GM_NS_USING

void Bind{{ function.name }}( pybind11::module& o_module )
{
    {% for interface in function.interfaces -%}
    o_module.def( "{{ function.name }}",
        []( {{ interface.typedArgs }} )
        {
            {%- if interface.returnType -%}
            return{{ " " }}
            {%- endif -%}
            {{ function.name }}( {{ interface.namedArgs }} );
        }
    );
    {% endfor %}
}
