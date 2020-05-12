#pragma once

#include <cmath>
#include <cstring>
#include <sstream>

#include <gm/api.h>
#include <gm/tool/assert.h>

GM_NAMESPACE_BEGIN

/// \class Vec2i
class GM_API Vec2i final
{
public:
    using ElementType = int;

    /// Default constructor.
    Vec2i() = default;

    /// Destructor.
    ~Vec2i() = default;

    /// Element-wise constructor.
    explicit Vec2i( const int& i_element0, const int& i_element1 )
        : m_elements{i_element0, i_element1}
    {
        GM_ASSERT( !HasNans() );
    }

#ifdef GM_DEBUG
    /// Copy constructor.
    Vec2i( const Vec2i& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( int ) * 2 );
        GM_ASSERT( !HasNans() );
    }

    /// Copy assignment operator.
    Vec2i& operator=( const Vec2i& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( int ) * 2 );
        GM_ASSERT( !HasNans() );
        return *this;
    }
#endif

    /// Element-wise index read accessor.
    inline int& operator[]( size_t i_index )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 2 );
        return m_elements[ i_index ];
    }

    /// Element-wise index write accessor.
    inline const int& operator[]( size_t i_index ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 2 );
        return m_elements[ i_index ];
    }

    //
    // Arithmetic Operator Overloading.
    //

    inline Vec2i operator+( const Vec2i& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Vec2i( m_elements[ 0 ] + i_vector.m_elements[ 0 ], m_elements[ 1 ] + i_vector.m_elements[ 1 ] );
    }

    /// Addition assignment.
    inline Vec2i& operator+=( const Vec2i& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] += i_vector.m_elements[ 0 ];
        m_elements[ 1 ] += i_vector.m_elements[ 1 ];
        return *this;
    }

    /// Subtraction.
    inline Vec2i operator-( const Vec2i& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Vec2i( m_elements[ 0 ] - i_vector.m_elements[ 0 ], m_elements[ 1 ] - i_vector.m_elements[ 1 ] );
    }

    /// Unary negation.
    inline Vec2i operator-() const
    {
        GM_ASSERT( !HasNans() );
        return Vec2i( -m_elements[ 0 ], -m_elements[ 1 ] );
    }

    inline Vec2i& operator-=( const Vec2i& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] -= i_vector.m_elements[ 0 ];
        m_elements[ 1 ] -= i_vector.m_elements[ 1 ];
        return *this;
    }

    inline Vec2i& operator*=( const int& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] *= i_scalar;
        m_elements[ 1 ] *= i_scalar;
        return *this;
    }

    inline Vec2i operator/( const int& i_scalar ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0 );
        int reciprocal = 1.0 / i_scalar;
        return Vec2i( m_elements[ 0 ] * reciprocal, m_elements[ 1 ] * reciprocal );
    }

    inline Vec2i& operator/=( const int& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0 );
        int reciprocal = 1.0 / i_scalar;
        m_elements[ 0 ] *= reciprocal;
        m_elements[ 1 ] *= reciprocal;
        return *this;
    }
    inline int X() const
    {
        GM_ASSERT( !HasNans() );
        return m_elements[ 0 ];
    }
    inline int Y() const
    {
        GM_ASSERT( !HasNans() );
        return m_elements[ 1 ];
    }

    /// Comparison operator
    inline bool operator==( const Vec2i& i_vector ) const
    {
        return m_elements[ 0 ] == i_vector.m_elements[ 0 ] && m_elements[ 1 ] == i_vector.m_elements[ 1 ];
    }

    /// Not equal operator
    inline bool operator!=( const Vec2i& i_vector ) const
    {
        return !( ( *this ) == i_vector );
    }

    /// Get the number of elements in this vector.
    inline static size_t GetElementSize()
    {
        return 2;
    }

    /// Are any of the element values NaNs?
    inline bool HasNans() const
    {
        return std::isnan( m_elements[ 0 ] ) || std::isnan( m_elements[ 1 ] );
    }

    /// Get the string representation.  For debugging purposes.
    inline std::string ToString() const
    {
        std::stringstream ss;
        ss << "Vec2i( ";
        ss << m_elements[ 0 ];
        ss << ", ";
        ss << m_elements[ 1 ];
        ss << " )";
        return ss.str();
    }

private:
    int m_elements[ 2 ] = {0, 0};
};

inline Vec2i operator*( const Vec2i& i_vector, const int& i_scalar )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Vec2i( i_vector[ 0 ] * i_scalar, i_vector[ 1 ] * i_scalar );
}

inline Vec2i operator*( const int& i_scalar, const Vec2i& i_vector )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Vec2i( i_vector[ 0 ] * i_scalar, i_vector[ 1 ] * i_scalar );
}

GM_NAMESPACE_END