#include <catch2/catch.hpp>

#include <gm/functions/{{ function.headerFileName }}>

{% for interface in function.interfaces %}
TEST_CASE( "{{ function.name }}_{{ interface.ArgClass("angle") }}" )
{
    {{ interface.ArgClass("angle") }} {{ interface.ArgType("angle").varName }} =
        {{ interface.Arg("angle").type.CppValue(95) }};
    {{ interface.ArgClass("angle") }} {{ interface.ArgType("angle").varName }}Radians =
        gm::{{ function.name }}( {{ interface.ArgType("angle").varName }} );
    CHECK( {{ interface.ArgType("angle").varName }}Radians
           == Approx( {{ interface.Arg("angle").type.CppValue( math.radians(95) ) }} ));
}
{% endfor %}
