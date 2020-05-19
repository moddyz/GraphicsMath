#include <catch2/catch.hpp>

#include <gm/functions/{{ function.headerFileName }}>

// This test is auto-generated! Please do not modify directly

{% for vectorType in function.types %}
TEST_CASE( "{{ function.name }}_{{ vectorType.className }}" )
{
    gm::{{ vectorType.className }} {{ vectorType.variablePrefix }}(
{% for index in range(vectorType.elementSize) -%}
    {{ vectorType.GetCppNumber(index * 2) }}
{%- if index + 1 < vectorType.elementSize -%}
        ,
{%- endif -%}
{%- endfor %}
    );
    CHECK( gm::{{ function.name }}( {{ vectorType.variablePrefix }} )
{% if vectorType.elementSize == 2 -%}
           == Approx( {{ vectorType.GetCppNumber(math.sqrt(4.0)) }} )
{% elif vectorType.elementSize == 3 -%}
           == Approx( {{ vectorType.GetCppNumber(math.sqrt(20.0)) }} )
{% elif vectorType.elementSize == 4 -%}
           == Approx( {{ vectorType.GetCppNumber(math.sqrt(56)) }} )
{%- endif -%}
    );
}
{% endfor %}