#include <catch2/catch.hpp>

#include <gm/functions/{{ function.headerFileName }}>

{% for interface in function.interfaces %}
TEST_CASE( "{{ function.name }}_{{ interface.ArgClass("vector") }}" )
{
    gm::{{ interface.ArgClass("vector") }} {{ interface.ArgVariable("vector") }}(
{% for index in range(interface.Arg("vector").type.elementSize) -%}
    {{ interface.Arg("vector").type.CppNumber(index * 2) }}
{%- if index + 1 < interface.Arg("vector").type.elementSize -%}
        ,
{%- endif -%}
{%- endfor %}
    );
    CHECK( gm::{{ function.name }}( {{ interface.ArgVariable("vector") }} )
{% if interface.Arg("vector").type.elementSize == 2 -%}
           == Approx( {{ interface.Arg("vector").type.CppNumber(math.sqrt(4.0)) }} )
{% elif interface.Arg("vector").type.elementSize == 3 -%}
           == Approx( {{ interface.Arg("vector").type.CppNumber(math.sqrt(20.0)) }} )
{% elif interface.Arg("vector").type.elementSize == 4 -%}
           == Approx( {{ interface.Arg("vector").type.CppNumber(math.sqrt(56)) }} )
{%- endif -%}
    );
}
{% endfor %}
